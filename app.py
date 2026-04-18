'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit
'''

import re
import oracledb
import streamlit as st

# --- DATABASE SETUP ---
LIB_DIR = "client path" # Enter your Oracle Instant Client path here, e.g. r"C:\oracle\instantclient_11_2"
DB_USER = "user" #Enter your DB username here
DB_PASS = "password" #Enter your DB password here
DB_HOST = "host" #Enter your DB host here
DB_PORT = "port" #Enter your DB port here
DB_SERVICE = "service" #Enter your DB service name here
DB_DSN = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"



@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.error(f"Error initializing Oracle Client: {e}")


init_db()


def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)


def parse_numeric_range(value):
    digits = re.findall(r"\d+", value)
    if not digits:
        return None
    return int("".join(digits))


def run_query(sql, params=None):
    if params is None:
        params = []
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    cols = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return cols, rows


def show_results(cols, rows):
    """Display query results as a dataframe or a no records message."""
    if rows:
        st.dataframe([dict(zip(cols, row)) for row in rows], use_container_width=True)
    else:
        st.write("No records found.")


st.title("Crime Data Explorer")

menu = [
    "Search by victim range",
    "Filter demographic patterns",
    "Same agency offenses",
    "Victimology cases",
    "Geographic + demographic overlap",
]
choice = st.sidebar.selectbox("Choose an action", menu)

if choice == "Search by victim range":
    st.write("### Search by victim range")
    start = st.text_input("Start value (Victim_ID numeric proxy)")
    end = st.text_input("End value (Victim_ID numeric proxy)")
    st.caption(
        "Note: this schema does not contain an explicit date column, so the search uses Victim_ID numeric suffix values as a proxy."
    )

    if st.button("Run search"):
        start_num = parse_numeric_range(start)
        end_num = parse_numeric_range(end)
        if start_num is None or end_num is None:
            st.error("Enter both start and end values containing digits.")
        elif start_num > end_num:
            st.error("Start value must be less than or equal to end value.")
        else:
            sql = (
                "SELECT d.victim_id, d.age, d.gender, d.ethnicity, d.crim_rec, "
                "a.agency_name, g.city, g.state "
                "FROM Demographic d "
                "JOIN Agency a ON d.agency_id = a.agency_id "
                "JOIN Geographic g ON g.agency_id = a.agency_id "
                "WHERE TO_NUMBER(REGEXP_SUBSTR(d.victim_id, '[0-9]+')) BETWEEN :1 AND :2 "
                "ORDER BY TO_NUMBER(REGEXP_SUBSTR(d.victim_id, '[0-9]+'))"
            )
            cols, rows = run_query(sql, [start_num, end_num])
            show_results(cols, rows)

elif choice == "Filter demographic patterns":
    st.write("### Filter demographic patterns")

    filter_type = st.selectbox("Filter by", ["Gender", "Ethnicity", "Crime keyword"])

    if filter_type == "Gender":
        pattern = st.text_input("Enter gender (e.g. Male, Female, M, F)")

        if st.button("Filter", key="filter_gender"):
            if not pattern:
                st.error("Enter a gender to search for.")
            else:
                gender_map = {"male": "M", "female": "F"}
                gender_val = gender_map.get(pattern.strip().lower(), pattern.strip().upper())
                sql = (
                    "SELECT d.victim_id, d.age, d.gender, d.ethnicity, d.crim_rec, a.agency_name "
                    "FROM Demographic d "
                    "JOIN Agency a ON d.agency_id = a.agency_id "
                    "WHERE d.gender = :1 "
                    "ORDER BY d.victim_id"
                )
                cols, rows = run_query(sql, [gender_val])
                show_results(cols, rows)

    elif filter_type == "Ethnicity":
        pattern = st.text_input("Enter ethnicity")

        if st.button("Filter", key="filter_ethnicity"):
            if not pattern:
                st.error("Enter an ethnicity to search for.")
            else:
                sql = (
                    "SELECT d.victim_id, d.age, d.gender, d.ethnicity, d.crim_rec, a.agency_name "
                    "FROM Demographic d "
                    "JOIN Agency a ON d.agency_id = a.agency_id "
                    "WHERE LOWER(d.ethnicity) LIKE :1 "
                    "ORDER BY d.victim_id"
                )
                cols, rows = run_query(sql, [f"%{pattern.lower()}%"])
                show_results(cols, rows)

    else:  # Crime keyword
        pattern = st.text_input("Enter crime keyword")

        if st.button("Filter", key="filter_crime"):
            if not pattern:
                st.error("Enter a crime keyword to search for.")
            else:
                sql = (
                    "SELECT d.victim_id, d.age, d.gender, d.ethnicity, d.crim_rec, a.agency_name "
                    "FROM Demographic d "
                    "JOIN Agency a ON d.agency_id = a.agency_id "
                    "WHERE LOWER(d.crim_rec) LIKE :1 "
                    "ORDER BY d.victim_id"
                )
                cols, rows = run_query(sql, [f"%{pattern.lower()}%"])
                show_results(cols, rows)

elif choice == "Same agency offenses":
    st.write("### Show offenses under the same agency")
    agency = st.text_input("Agency name or partial name")

    if st.button("Show offenses"):
        if not agency:
            st.error("Enter an agency name or partial name.")
        else:
            sql = (
                "SELECT a.agency_name, a.agency_type, g.city, g.state, d.victim_id, d.crim_rec "
                "FROM Agency a "
                "JOIN Geographic g ON g.agency_id = a.agency_id "
                "JOIN Demographic d ON d.agency_id = a.agency_id "
                "WHERE LOWER(a.agency_name) LIKE :1 "
                "ORDER BY a.agency_name, d.victim_id"
            )
            cols, rows = run_query(sql, [f"%{agency.lower()}%"])
            show_results(cols, rows)

elif choice == "Victimology cases":
    st.write("### Show victimology cases")
    victimology = st.text_input("Victimology case type (e.g. Extortion)")

    if st.button("Search cases"):
        if not victimology:
            st.error("Enter a victimology case type.")
        else:
            sql = (
                "SELECT v.victim_id, v.offender_id, v.crim_rec, d.age, d.gender, d.ethnicity, a.agency_name "
                "FROM Victimology v "
                "JOIN Demographic d ON v.victim_id = d.victim_id "
                "JOIN Agency a ON d.agency_id = a.agency_id "
                "WHERE LOWER(v.crim_rec) LIKE :1 OR LOWER(d.crim_rec) LIKE :1 "
                "ORDER BY v.victim_id"
            )
            cols, rows = run_query(sql, [f"%{victimology.lower()}%"])
            show_results(cols, rows)

else:
    st.write("### Geographic and demographic overlap")
    if st.button("Show overlap"):
        sql = (
            "SELECT g.city, g.state, a.agency_name, d.victim_id, d.age, d.gender, d.ethnicity, d.crim_rec "
            "FROM Geographic g "
            "JOIN Agency a ON g.agency_id = a.agency_id "
            "JOIN Demographic d ON d.agency_id = a.agency_id "
            "ORDER BY g.state, g.city, d.victim_id"
        )
        cols, rows = run_query(sql)
        show_results(cols, rows)

# run using: streamlit run crime_app.py
