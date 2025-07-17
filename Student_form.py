from dotenv import load_dotenv
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

load_dotenv()  # load .env variables here
# Create a connection to the MySQL database
def create_database_connection():
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return mydb

# Create a database cursor
def create_database_cursor(mydb):
    return mydb.cursor(buffered=True)

# Create labels and entry fields for the student information
def create_label_entry_grid(frame, label_text, row, column):
    label = Label(frame, text=label_text, font=('times new roman', 18), bg='dark slate gray', fg='black')
    label.grid(row=row, column=column, padx=5, sticky='w')
    entry = Entry(frame, font=('times new roman', 18))
    entry.grid(row=row, column=column+1, sticky='w')
    return entry

# Function to add a new student
def add_student():
    # Create the database connection and the database cursor
    mydb = create_database_connection()
    cursor = create_database_cursor(mydb)

    add_window = Toplevel()
    add_window.title("Add Student")
    add_window.geometry('700x500')
    add_window.configure(bg="dark slate gray") 
    label3 = Label(add_window, text='Add New Student: ', font=('arial', 16, "bold"), bg='silver', fg='black', height=2, width=45)
    label3.grid(row=0, column=0, columnspan=2, pady=10)

    # function that saves the new students
    def save_students():
        # Get the input values from the user
        student_id = int(student_id_entry.get())
        student_name = student_name_entry.get()
        class_id = class_id_entry.get()
        gender = gender_entry.get()
        phone_number = phone_number_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        try:
            # SQL query to insert a new student into the 'student' table
            insert_query = "INSERT INTO student (student_id, student_name, class, gender, phone_number, " \
                                   "email, address) " \
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (student_id, student_name, class_id, gender, phone_number, email, address)

            # Execute the query
            cursor.execute(insert_query, values)

            # Commit the changes to the database
            mydb.commit()

            messagebox.showinfo("Add Student", "Student added successfully!")
            add_window.destroy()

        except mysql.connector.Error as error:
                    messagebox.showerror("Add Student", f"Failed to add student: {error}")
        cursor.close()
        mydb.close()

    student_id_entry = create_label_entry_grid(add_window, "Student ID:  ", 1, 0)
    student_name_entry = create_label_entry_grid(add_window, "Student Name:  ", 2, 0)
    class_id_entry = create_label_entry_grid(add_window, "Class:  ", 3, 0)
    gender_entry = create_label_entry_grid(add_window, "Gender:  ", 4, 0)
    phone_number_entry = create_label_entry_grid(add_window, "Phone Number:  ", 5, 0)
    email_entry = create_label_entry_grid(add_window, "Email:  ", 6, 0)
    address_entry = create_label_entry_grid(add_window, "Address:  ", 7, 0)

    # Create the student buttons
    save_student_button = Button(add_window, text="Save", command=save_students, font=('Arial', 15), bg='silver')
    save_student_button.grid(row=8, column=1, padx=5, pady=10)
    back_button = Button(add_window, text='Close', font=('Arial', 15), bg='silver', fg='black', command=add_window.destroy)
    back_button.grid(row=8, column=0, padx=5, pady=10)

# Function to delete a student information
def delete_student():
    # Create the database connection and the database cursor
    mydb = create_database_connection()
    cursor = create_database_cursor(mydb)

    delete_window = Toplevel()
    delete_window.geometry('500x400')
    delete_window.title('Delete Student')
    delete_window.configure(bg='dark slate gray')
    label4 = Label(delete_window, text='Delete a student: ', font=('times new roman', 16), bg='silver', fg='black', height=2, width=45)
    label4.grid(row=0, column=0, columnspan=2, pady=10)

    def delete():
        student_id = delete_entry.get()
        try:
            # Delete the student from the student_parent table
            delete_query1 = "DELETE FROM student_parent WHERE student_id = %s"
            cursor.execute(delete_query1, (student_id,))
            mydb.commit()

            # Delete the student from the student table
            delete_query2 = "DELETE FROM student WHERE student_id = %s"
            cursor.execute(delete_query2, (student_id,))
            mydb.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo('Delete Student', 'Student ID does not exist in the database')
                delete_entry.delete(0, END)
            else:
                messagebox.showinfo('Delete Student', 'Student deleted successfully!')
                delete_window.destroy()
            
        except mysql.connector.Error as error:
             messagebox.showerror('Error', f'Error deleting student: {error}')

        cursor.close()
        mydb.close()
    
    delete_entry = create_label_entry_grid(delete_window, "Student ID:  ", 2, 0)
    # Buttons
    delete_button1 = Button(delete_window, text='Delete', font=('Arial', 14), bg='silver', fg='black', command=delete)
    delete_button1.grid(row=3, column=1, padx=5, pady=10)
    back_button = Button(delete_window, text='Close', font=('Arial', 14), bg='silver', fg='black', command=delete_window.destroy)
    back_button.grid(row=3, column=0, padx=5, pady=10)

# Function to update the student information
def update_student():
    # Create the database connection and the database cursor
    mydb = create_database_connection()
    cursor = create_database_cursor(mydb)

    # Function to fetch the student info to be updated
    def fetch_student_info():
        student_id = id_entry.get()
        # Fetch student information from the database based on the provided student ID
        select_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(select_query, (student_id,))
        student_info = cursor.fetchone()

        if student_info:
            # Display the fetched student information in the entry fields for updating
            name_entry.delete(0, END)
            name_entry.insert(END, student_info[1])  # Assuming name is at index 1 in the student_info tuple
            class_entry.delete(0, END)
            class_entry.insert(END, student_info[2])  # Assuming class is at index 2 in the student_info tuple
            gender_entry.delete(0, END)
            gender_entry.insert(END, student_info[3])  # Assuming gender is at index 3 in the student_info tuple
            phone_entry.delete(0, END)
            phone_entry.insert(END, student_info[4])  # Assuming phone is at index 4 in the student_info tuple
            email_entry.delete(0, END)
            email_entry.insert(END, student_info[5])  # Assuming email is at index 5 in the student_info tuple
            address_entry.delete(0, END)
            address_entry.insert(END, student_info[6])  # Assuming address is at index 6 in the student_info tuple
        else:
            messagebox.showinfo('Update Student', 'Student ID does not exist in the database')
            name_entry.delete(0, END)
            class_entry.delete(0, END)
            gender_entry.delete(0, END)
            phone_entry.delete(0, END)
            email_entry.delete(0, END)
            address_entry.delete(0, END)

    # Function that updates the student info
    def update():
        student_id = id_entry.get()
        student_name = name_entry.get()
        student_class = class_entry.get()
        student_gender = gender_entry.get()
        student_phone = phone_entry.get()
        student_email = email_entry.get()
        student_address = address_entry.get()
        
        # Update the student in the student table
        update_query = "UPDATE student SET student_name = %s, class = %s, gender = %s, phone_number = %s, email = %s, address = %s WHERE student_id = %s"
        values = (student_name, student_class, student_gender, student_phone, student_email, student_address, student_id)
        cursor.execute(update_query, values)
        mydb.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo('Update Student', 'Student ID does not exist in the database')
        else:
            messagebox.showinfo('Update Student', 'Student updated successfully!')

    update_window = Toplevel()
    update_window.geometry('700x600')
    update_window.title('Update Student')
    update_window.configure(bg='dark slate gray')
    update_window.grab_set()
    label5 = Label(update_window, text='Update student info: ', font=('Arial Rounded MT Bold', 16), bg='silver', fg='black', height=2, width=45)
    label5.grid(row=0, column=0, columnspan=2, pady=10)
    update_label = Label(update_window, text="Enter the student ID you want to update: ", font=('times new roman', 15), bg='white', fg='black')
    update_label.grid(row=1, column=0, padx=10, pady=10)

    id_label = Label(update_window, text="Student ID:", font=('Arial Rounded MT Bold', 14), bg='dark slate gray', fg='white')
    id_label.grid(row=2, column=0, padx=10, pady=10)
    id_entry = Entry(update_window, width=20, font=('arial', 14))
    id_entry.grid(row=2, column=1, padx=10, pady=10)
    fetch_button = Button(update_window, text='Fetch', font=('Arial', 14), bg='silver', fg='black', command=fetch_student_info)
    fetch_button.grid(row=2, column=2, padx=10, pady=10)

    name_entry = create_label_entry_grid(update_window, "Student Name:", 3, 0)
    class_entry = create_label_entry_grid(update_window, "Student Class:", 4, 0)
    gender_entry = create_label_entry_grid(update_window, "Student Gender:", 5, 0)
    phone_entry = create_label_entry_grid(update_window, "Student Phone:", 6, 0)
    email_entry = create_label_entry_grid(update_window, "Student Email:", 7, 0)
    address_entry = create_label_entry_grid(update_window, "Student Address:", 8, 0)
    # Buttons
    update_button1 = Button(update_window, text='Update', font=('Arial', 14), bg= 'silver', fg='black', command=update)
    update_button1.grid(row=9, column=1, padx=5, pady=10)
    back_button = Button(update_window, text='Close', font=('Arial', 14), bg='silver', fg='black', command=update_window.destroy)
    back_button.grid(row=9, column=0, padx=5, pady=10)

    update_window.mainloop()

# Function to display the student information from database
def display_students():
    # Create the database connection and the database cursor
    mydb = create_database_connection()
    cursor = create_database_cursor(mydb)

    # Retrieve the student data from the database
    cursor.execute("""
                SELECT 
                    s.student_id, 
                    s.student_name, 
                    s.class, 
                    s.gender, 
                    s.phone_number, 
                    s.email, 
                    s.address
                FROM student s
            """)
    student_data = cursor.fetchall()

    # Create a new Tkinter window to display the student information
    student_info_window = Toplevel()
    student_info_window.attributes('-fullscreen', True)
    student_info_window.title('Student Information')
    student_info_window.configure(bg='dark slate gray')
    label6 = Label(student_info_window, text='Student Information:', font=('Arial', 20, "bold"), bg='silver', fg='black', height=2, width=60)
    label6.grid(row=0, column=0, columnspan=2, padx=30, pady=10) 

    # Create the treeview table
    student_tree = ttk.Treeview(student_info_window, columns=['Student ID', 'Student Name', 'Class', 'Gender', 'Phone Number',
                                                 'Email', 'Address'], show='headings')
    student_tree.heading('Student ID', text='Student ID')
    student_tree.heading('Student Name', text='Student Name')
    student_tree.heading('Class', text='Class')
    student_tree.heading('Gender', text='Gender')
    student_tree.heading('Phone Number', text='Phone Number')
    student_tree.heading('Email', text='Email')
    student_tree.heading('Address', text='Address')
    student_tree.grid(row=1, column=1, columnspan=4, padx=10, pady=20)

    # Insert the student data into the treeview
    for student in student_data:
        student_tree.insert('', 'end', values=student)
    
    back_button = Button(student_info_window, text='Close', font=('Arial', 14), bg='silver', fg='black', command=student_info_window.destroy)
    back_button.grid(row=8, column=1, padx=5, pady=10)
    student_info_window.mainloop()

# Function for student management system
def open_student_management_system():
    student_form = Toplevel()
    student_form.title("Student Management System")
    student_form.geometry('800x600')
    student_form.configure(bg="dark slate gray")
    label2 = Label(student_form, text='Student Registration Form', font=('Arial Rounded MT Bold', 20), bg='silver', fg='black', height=2, width=50)
    label2.grid(row=1, column=3, columnspan=3, pady=20)
    
    # Create buttons or other widgets for student management operations
    add_button = Button(student_form, text="Add Student", command=add_student, font=('Arial Rounded MT Bold', 14), bg='white', fg='black')
    add_button.grid(row=2, column=3, padx=5, pady=20)
    delete_button = Button(student_form, text="Delete Student", command=delete_student, font=('Arial Rounded MT Bold', 14), bg='white', fg='black')
    delete_button.grid(row=2, column=4, padx=5, pady=20)
    update_button = Button(student_form, text="Update Student", command=update_student, font=('Arial Rounded MT Bold', 14), bg='white', fg='black')
    update_button.grid(row=3, column=3, padx=5, pady=20)
    display_student_button = Button(student_form, text="Display Student Information", command=display_students, font=('Arial Rounded MT Bold', 14), bg='white', fg='black')
    display_student_button.grid(row=3, column=4, padx=5, pady=20)
    back_button = Button(student_form, text='Close', font=('Arial', 14), bg='silver', fg='black', command=student_form.destroy)
    back_button.grid(row=4, column=3, columnspan=3, padx=1, pady=30)
    student_form.mainloop()