import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Attendance Monitor", layout="wide")
st.title("Student Attendance Monitoring System")

uploaded_file = st.file_uploader("Upload Attendance Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Clean column headers
    df.columns = [str(col).strip() for col in df.columns]

    st.success("File uploaded successfully!")

    # Ask for PRN
    prn_list = df['prn'].dropna().unique()
    selected_prn = st.selectbox("Select PRN", prn_list)

    # Filter data for selected PRN
    student_data = df[df['prn'] == selected_prn]

    if not student_data.empty:
        st.subheader("Raw Data for Selected Student")
        st.dataframe(student_data)

        # Select only numeric columns (attendance columns)
        attendance_data = student_data.select_dtypes(include='number').T
        attendance_data.columns = ['Attendance']
        attendance_data['Subject'] = attendance_data.index

        # Calculate total
        total_attendance = attendance_data['Attendance'].sum()
        st.metric(label="Total Attendance", value=int(total_attendance))

        # Plot
        st.subheader("Subject-wise Attendance")
        fig = px.bar(attendance_data, x='Subject', y='Attendance', text='Attendance', title="Attendance per Subject")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("PRN not found.")
