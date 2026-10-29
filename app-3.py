import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="School Management System", page_icon="🎓", layout="wide")

# Demo app: records are stored in Streamlit session memory and reset when the session restarts.
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame([
        {"Student ID": "S001", "Name": "Ayesha Khan", "Class": "8", "Guardian Contact": "03001234567"},
        {"Student ID": "S002", "Name": "Ali Ahmed", "Class": "9", "Guardian Contact": "03007654321"},
    ])
if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame(columns=["Date", "Student ID", "Student Name", "Status"])
if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=["Student ID", "Student Name", "Subject", "Marks", "Total Marks"])

st.title("🎓 School Management System")
st.caption("A beginner-friendly Python web app built with Streamlit")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Open section", ["Dashboard", "Students", "Attendance", "Results", "About"])

students = st.session_state.students

if page == "Dashboard":
    st.subheader("School Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", len(students))
    c2.metric("Attendance Records", len(st.session_state.attendance))
    c3.metric("Result Records", len(st.session_state.results))
    st.markdown("### Welcome")
    st.write("Use the sidebar to manage student records, mark attendance, and enter marks.")
    st.info("Demo note: this starter project keeps data in the current app session. For permanent storage, connect a database.")

elif page == "Students":
    st.subheader("Student Management")
    with st.form("add_student_form", clear_on_submit=True):
        st.markdown("#### Add a student")
        student_id = st.text_input("Student ID", placeholder="e.g. S003")
        name = st.text_input("Student name")
        class_name = st.selectbox("Class", [str(n) for n in range(1, 13)])
        contact = st.text_input("Guardian contact (optional)")
        submitted = st.form_submit_button("Add Student")
        if submitted:
            if not student_id.strip() or not name.strip():
                st.error("Please enter both Student ID and student name.")
            elif student_id.strip() in st.session_state.students["Student ID"].astype(str).tolist():
                st.error("That Student ID already exists.")
            else:
                new_row = pd.DataFrame([{
                    "Student ID": student_id.strip(),
                    "Name": name.strip(),
                    "Class": class_name,
                    "Guardian Contact": contact.strip()
                }])
                st.session_state.students = pd.concat([st.session_state.students, new_row], ignore_index=True)
                st.success(f"Added {name.strip()} successfully.")
                st.rerun()

    st.markdown("#### Student records")
    search = st.text_input("Search by name or student ID")
    current = st.session_state.students
    if search:
        mask = current.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
        current = current[mask]
    st.dataframe(current, use_container_width=True, hide_index=True)
    st.download_button("Download student records (CSV)",
        data=st.session_state.students.to_csv(index=False).encode("utf-8"),
        file_name="student_records.csv", mime="text/csv")

elif page == "Attendance":
    st.subheader("Attendance")
    current_students = st.session_state.students
    if current_students.empty:
        st.warning("Add students first.")
    else:
        student_ids = current_students["Student ID"].astype(str).tolist()
        selected_id = st.selectbox("Select student", student_ids,
            format_func=lambda sid: f"{sid} — {current_students.loc[current_students['Student ID'].astype(str) == sid, 'Name'].iloc[0]}")
        selected_name = current_students.loc[current_students["Student ID"].astype(str) == selected_id, "Name"].iloc[0]
        attendance_date = st.date_input("Attendance date", value=date.today())
        status = st.radio("Status", ["Present", "Absent", "Late"], horizontal=True)
        if st.button("Save attendance"):
            new_row = pd.DataFrame([{"Date": str(attendance_date), "Student ID": selected_id,
                                     "Student Name": selected_name, "Status": status}])
            st.session_state.attendance = pd.concat([st.session_state.attendance, new_row], ignore_index=True)
            st.success("Attendance saved.")
        st.markdown("#### Attendance history")
        st.dataframe(st.session_state.attendance, use_container_width=True, hide_index=True)
        st.download_button("Download attendance (CSV)",
            data=st.session_state.attendance.to_csv(index=False).encode("utf-8"),
            file_name="attendance.csv", mime="text/csv")

elif page == "Results":
    st.subheader("Student Results")
    current_students = st.session_state.students
    if current_students.empty:
        st.warning("Add students first.")
    else:
        student_ids = current_students["Student ID"].astype(str).tolist()
        selected_id = st.selectbox("Student", student_ids,
            format_func=lambda sid: f"{sid} — {current_students.loc[current_students['Student ID'].astype(str) == sid, 'Name'].iloc[0]}")
        selected_name = current_students.loc[current_students["Student ID"].astype(str) == selected_id, "Name"].iloc[0]
        with st.form("result_form", clear_on_submit=True):
            subject = st.text_input("Subject", placeholder="e.g. Mathematics")
            col1, col2 = st.columns(2)
            marks = col1.number_input("Marks obtained", min_value=0, max_value=100, value=0)
            total = col2.number_input("Total marks", min_value=1, max_value=100, value=100)
            save_result = st.form_submit_button("Save result")
            if save_result:
                if not subject.strip():
                    st.error("Please enter a subject.")
                elif marks > total:
                    st.error("Marks obtained cannot be greater than total marks.")
                else:
                    new_result = pd.DataFrame([{"Student ID": selected_id, "Student Name": selected_name,
                                                "Subject": subject.strip(), "Marks": int(marks),
                                                "Total Marks": int(total)}])
                    st.session_state.results = pd.concat([st.session_state.results, new_result], ignore_index=True)
                    st.success("Result saved.")
        st.markdown("#### Saved results")
        results = st.session_state.results.copy()
        if not results.empty:
            results["Percentage"] = (results["Marks"] / results["Total Marks"] * 100).round(1)
        st.dataframe(results, use_container_width=True, hide_index=True)
        st.download_button("Download results (CSV)",
            data=st.session_state.results.to_csv(index=False).encode("utf-8"),
            file_name="student_results.csv", mime="text/csv")

else:
    st.subheader("About this project")
    st.write("""
    **School Management System** is a sample educational project created with Python and Streamlit.

    Features:
    - Dashboard with simple statistics
    - Add and search student records
    - Record student attendance
    - Save marks and calculate percentages
    - Download records as CSV files

    **Technology:** Python, Streamlit, pandas

    **Important:** This is a learning/demo project, not a production school database. Do not enter real sensitive student information.
    """)
