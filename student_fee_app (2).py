import streamlit as st
import urllib.parse
# ---------------------------------------
# READ STUDENT DATA FROM FILE
# ---------------------------------------

def load_students():

    students = []

    try:

        with open("/content/students.txt", "r") as file:

            for line in file:

                data = line.strip().split(",")

                students.append(data)

    except FileNotFoundError:

        students = []

        with open("students.txt", "w") as file:
          pass

    return students

# ---------------------------------------
# CALCULATE FEE SUMMARY
# ---------------------------------------

def calculate_fee_summary(students):

    total_students = len(students)

    total_fee = 0
    paid_fee = 0
    due_fee = 0

    for student in students:

        total_fee += int(student[4])
        paid_fee += int(student[5])

    due_fee = total_fee - paid_fee

    return total_students, total_fee, paid_fee, due_fee

def dashboard(students):

    # -----------------------------------------
    # PAGE CONFIGURATION
    # -----------------------------------------

    st.set_page_config(
        page_title="Student Fee Management",
        page_icon="🎓",
        layout="wide"
    )


  # -----------------------------------------
  # CUSTOM CSS
  # -----------------------------------------
    st.set_page_config(
        page_title="Student Fee Management",
        page_icon="🎓",
        layout="wide"
    )

    st.markdown("""
    <style>

    .main-header {
        background: linear-gradient(135deg, #3949AB, #5C6BC0);
        padding: 30px;
        border-radius: 18px;
        color: white;
        text-align: center;
    }

    .main-title {
        font-size: 34px;
        font-weight: bold;
    }

    .main-subtitle {
        font-size: 17px;
    }

    </style>
    """, unsafe_allow_html=True)


    st.markdown(
        """
        <div class="main-header">

        <div class="main-title">
            🎓 Student Fee Management System
        </div>

        <div class="main-subtitle">
            Student Records & Fee Management Dashboard
        </div>

        </div>
        """,
        unsafe_allow_html=True
      )


    # -----------------------------------------
    # SIDEBAR
    # -----------------------------------------

    st.sidebar.markdown(
        "## 📌"
    )

    st.sidebar.markdown("---")

    choice = st.sidebar.radio(
      "Select Menu",
      [
          "🏠 Dashboard",
          "➕ Add Student Fee",
          "✏️ Update Fee",
          "📋 Fee Records",
          "🔴 Due Fee Students",
      ]
    )

    st.sidebar.markdown("---")

    st.sidebar.write("🏫 **School / College Portal**")

    st.sidebar.caption(
      "Student Fee Management System"
    )

    return choice

    # -----------------------------------------
    # DASHBOARD
    # -----------------------------------------

def  show_dashboard(students):

    total_students, total_fee, paid_fee, due_fee = calculate_fee_summary(students)
    st.subheader("📊 Dashboard Overview")


    # Dashboard cards

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:

        st.metric(
            "💰 Total Fee",
            f"₹{total_fee:,}"
        )

    with col3:

        st.metric(
            "🟢 Fee Collected",
            f"₹{paid_fee:,}"
        )

    with col4:

        st.metric(
            "🔴 Fee Due",
            f"₹{due_fee:,}"
        )
    # -----------------------------------------
    # ABOUT SYSTEM
    # -----------------------------------------
    st.subheader("ℹ️ About the System")

    st.markdown("""
    ### 🎓 Student Fee Management System

    This system is designed to simplify student fee management
    and help institutions keep track of student payments.

    **Key Features:**

    - 👨‍🎓 Add and manage student details
    - 💰 Track total and paid fees
    - 🔴 Identify students with pending fees
    - 📊 View overall fee collection through the dashboard
    - 🟢 Generate personalized WhatsApp fee reminders
    - 📁 Store student records using file handling

    **Purpose:**

    The system reduces manual work, helps avoid calculation errors,
    and makes it easier to identify and follow up on pending fees.
    """)     


def display_fee_records(students):

    st.subheader("📋 Student Fee Records")

    table_data = []

    for student in students:

        student_id = student[0]
        name = student[1]
        parent = student[2]
        total_fee = int(student[4])
        paid_fee = int(student[5])

        due_fee = total_fee - paid_fee

        if due_fee == 0:
            status = "🟢 Paid"
        else:
            status = "🔴 Due"

        table_data.append({
            "Student ID": student_id,
            "Student Name": name,
            "Parent Name": parent,
            "Total Fee": f"₹{total_fee:,}",
            "Paid Fee": f"₹{paid_fee:,}",
            "Due Fee": f"₹{due_fee:,}",
            "Status": status
        })

    st.table(table_data)
def add_student(students):

    st.subheader("➕ Add Student Fee")

    student_id = st.text_input("Student ID")
    name = st.text_input("Student Name")
    parent = st.text_input("Parent Name")
    phone = st.text_input("Phone Number")

    total_fee = st.number_input(
        "Total Fee",
        min_value=0,
        step=1000
    )

    paid_fee = st.number_input(
        "Paid Fee",
        min_value=0,
        step=1000
    )

    if st.button("💾 Save "):

        # Check paid fee
        if paid_fee > total_fee:

            st.error("Paid fee cannot be greater than total fee.")

        else:

            # Check duplicate ID
            exists = False

            for student in students:

                if student[0].lower() == student_id.lower():

                    exists = True
                    break

            if exists:

                st.error("Student ID already exists.")

            else:

                student = [
                    student_id,
                    name,
                    parent,
                    phone,
                    str(total_fee),
                    str(paid_fee)
                ]

                students.append(student)

                # Save to file
                with open("students.txt", "w") as file:

                    for student in students:

                        file.write(
                            ",".join(student) + "\n"
                        )

                st.success(
                    "Student fee details saved successfully!"
                )
def update_fee(students):

    st.subheader("✏️ Update Student Fee")

    student_id = st.text_input("Enter Student ID")

    new_payment = st.number_input(
        "Enter New Payment Amount",
        min_value=0,
        step=1000
    )

    if st.button("💾 Update Fee"):

        found = False

        for student in students:

            if student[0].lower() == student_id.lower():

                found = True

                total_fee = int(student[4])
                paid_fee = int(student[5])

                new_paid_fee = paid_fee + new_payment

                if new_paid_fee > total_fee:

                    st.error(
                        "Payment cannot be greater than total fee."
                    )

                else:

                    student[5] = str(new_paid_fee)

                    # Save updated data
                    with open("students.txt", "w") as file:

                        for record in students:

                            file.write(
                                ",".join(record) + "\n"
                            )

                    due_fee = total_fee - new_paid_fee

                    st.success(
                        f"Fee details updated successfully! "
                        f"Remaining due: ₹{due_fee:,}"
                    )

                break

        if not found:

            st.error("Student ID not found.")

# ---------------------------------------
# DUE FEE STUDENTS
# ---------------------------------------

def due_fee_students(students):

    st.subheader("🔴 Students With Due Fee")

    found = False

    for student in students:

        student_id = student[0]
        name = student[1]
        parent = student[2]
        phone = student[3]

        total_fee = int(student[4])
        paid_fee = int(student[5])

        due_fee = total_fee - paid_fee

        if due_fee > 0:

            found = True

            # --------------------------------
            # STUDENT DETAILS
            # --------------------------------

            st.markdown(f"### 👨‍🎓 {name}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.write(f"**ID:** {student_id}")

            with col2:
                st.write(f"**Parent:** {parent}")

            with col3:
                st.write(f"**Phone:** {phone}")

            with col4:
                st.write(f"**Due:** ₹{due_fee:,}")

            # --------------------------------
            # PHONE VALIDATION
            # --------------------------------

            if len(phone) != 10 or not phone.isdigit():

                st.error("❌ Invalid phone number.")

            else:

                # --------------------------------
                # CREATE WHATSAPP MESSAGE
                # --------------------------------

                message = (
                    f"Dear {parent},\n\n"
                    f"This is a reminder that "
                    f"₹{due_fee:,} is pending "
                    f"towards {name}'s fee.\n\n"
                    f"Kindly make the payment "
                    f"at your earliest convenience.\n\n"
                    f"Thank you."
                )

                # Convert message for URL
                encoded_message = urllib.parse.quote(message)

                # India country code +91
                whatsapp_number = "91" + phone

                whatsapp_url = (
                    f"https://wa.me/{whatsapp_number}"
                    f"?text={encoded_message}"
                )

                # --------------------------------
                # WHATSAPP BUTTON
                # --------------------------------

                st.markdown(
                    f"""
                    <a href="{whatsapp_url}" target="_blank">
                        <button style="
                            background-color:#25D366;
                            color:white;
                            border:none;
                            padding:10px 20px;
                            border-radius:8px;
                            font-size:16px;
                            cursor:pointer;
                        ">
                            🟢 WhatsApp Reminder
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

            st.divider()

    if not found:

        st.success(
            "🎉 No students have pending fees!"
        )
# ---------------------------------------
# MAIN FUNCTION
# ---------------------------------------

def main():

#  st.title("🎓 Student Fee Management System")

  students = load_students()
  choice = dashboard(students)

  if choice == "📋 Fee Records":

    display_fee_records(students)
  elif choice == "🏠 Dashboard":

    show_dashboard(students)
  elif choice == "➕ Add Student Fee":

    add_student(students)
  elif choice == "✏️ Update Fee":

    update_fee(students)
  elif choice == "🔴 Due Fee Students":

    due_fee_students(students)
  
# ---------------------------------------
# PROGRAM START
# ---------------------------------------

if  __name__ == "__main__":

  main()
