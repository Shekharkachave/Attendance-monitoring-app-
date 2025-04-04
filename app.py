# Clean attendance data safely
def clean_attendance(value):
    try:
        return float(str(value).replace('%', '').strip())
    except:
        return 0  # Default to 0 if conversion fails

if uploaded_file:
    df = pd.read_excel(uploaded_file, skiprows=5)
    df.columns.values[0:3] = ['Sr.No', 'PRN', 'Name']
    df.dropna(subset=['PRN', 'Name'], inplace=True)

    prn_input = st.text_input("Enter PRN or Student Name")

    if prn_input:
        student = df[df['PRN'].astype(str).str.lower() == prn_input.lower()]
        if student.empty:
            student = df[df['Name'].str.lower().str.contains(prn_input.lower(), na=False)]

        if student.empty:
            st.warning("Student not found.")
        else:
            student_data = student.iloc[0]
            st.success(f"Found: {student_data['Name']} (PRN: {student_data['PRN']})")

            attendance = student_data.filter(like='Per')
            attendance_clean = attendance.apply(clean_attendance)
            
            st.write("Subject-wise Attendance:")
            st.dataframe(attendance_clean)

            # Graph
            fig, ax = plt.subplots()
            attendance_clean.plot(kind='bar', ax=ax, color='skyblue')
            plt.ylim(0, 100)
            st.pyplot(fig)
