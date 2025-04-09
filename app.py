import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attendance Dashboard", layout="centered")
st.title("Student Attendance Dashboard")

uploaded_file = st.file_uploader("Upload your attendance Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Read the file and clean index
        df = pd.read_excel(uploaded_file, index_col=0)
        df.index = df.index.astype(str).str.strip()
        
        st.subheader("Raw Attendance Data")
        st.dataframe(df)

        # Check for 'Total' row
        if 'Total' in df.index:
            total_lectures = df.loc['Total']
            df = df.drop(index='Total')

            # Compute attendance percentage
            attendance_percent = (df / total_lectures) * 100
            attendance_percent = attendance_percent.round(2)

            # Dropdown to select a student
            student_names = attendance_percent.index.tolist()
            selected_student = st.selectbox("Select a student", student_names)

            if selected_student:
                st.subheader(f"Subject-wise Attendance for {selected_student}")
                
                # Show bar chart
                st.bar_chart(attendance_percent.loc[selected_student])

                # Pie chart of attendance vs absence
                attended = df.loc[selected_student].sum()
                total = total_lectures.sum()
                absent = total - attended

                fig, ax = plt.subplots()
                ax.pie(
                    [attended, absent],
                    labels=['Attended', 'Missed'],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=['green', 'red']
                )
                ax.axis('equal')
                st.pyplot(fig)

                # Show overall percentage
                overall = (attended / total) * 100
                st.success(f"**Overall Attendance: {overall:.2f}%**")

        else:
            st.error("The sheet must include a row labeled 'Total' to calculate percentages.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Upload your Excel file to begin.")
