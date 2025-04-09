import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attendance Monitor", layout="wide")
st.title("Student Attendance Monitoring")

uploaded_file = st.file_uploader("Upload Attendance Excel File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Load and clean data
        df = pd.read_excel(uploaded_file, index_col=0)
        df.index = df.index.astype(str).str.strip()  # Clean index
        st.subheader("Raw Attendance Data")
        st.dataframe(df)

        if 'Total' in df.index:
            total_lectures = df.loc['Total']
            df = df.drop(index='Total')

            # Attendance percentage per subject
            attendance_percent = (df / total_lectures) * 100
            attendance_percent = attendance_percent.round(2)

            # Dropdown to select student
            student_names = attendance_percent.index.tolist()
            selected_student = st.selectbox("Select a student to view details", student_names)

            if selected_student:
                st.subheader(f"Attendance for {selected_student}")

                # Subject-wise attendance bar chart
                st.markdown("**Subject-wise Attendance (%)**")
                st.bar_chart(attendance_percent.loc[selected_student])

                # Optional Pie chart
                st.markdown("**Overall Attendance vs Absence (Pie Chart)**")
                attended = df.loc[selected_student].sum()
                total = total_lectures.sum()
                absent = total - attended

                fig, ax = plt.subplots()
                ax.pie([attended, absent], labels=['Attended', 'Absent'], autopct='%1.1f%%', colors=['green', 'red'])
                ax.axis('equal')
                st.pyplot(fig)

        else:
            st.error("Could not find a row labeled 'Total'. Please make sure the last row has that label.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an Excel file to begin.")
