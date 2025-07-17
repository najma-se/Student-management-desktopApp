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

# Function to add parent information
def add_parent():
    # Create the database connection and the database cursor
    mydb = create_database_connection()
    cursor = create_database_cursor(mydb)

    # Create window
    add_window1 = Toplevel()
    add_window1.title("Add Parent")
    add_window1.geometry('700x500')
    add_window1.configure(bg="dark slate gray")
    label3 = Label(add_window1, text='Add Parent: ', font=('Arial', 16), bg='silver', fg='black', height=2, width=40)
    label3.grid(row=0, column=0, columnspan=2, pady=10)

    # Function that saves the parent info
    def save_parents():
        parent_id = int(parent_id_entry.get())
        parent_name = parent_name_entry.get()
        student_id = student_id_entry.get()
        phone_number = phone_number_entry.get()
        email = email_entry.get()

        try:
            insert_query = "INSERT INTO parents (parent_id, parent_name, student_id, parent_phoneNumber, parent_email) " \
                                   "VALUES (%s, %s, %s, %s, %s)"
            values = (parent_id, parent_name, student_id, phone_number, email)
            cursor.execute(insert_query, values)
            mydb.commit()

            messagebox.showinfo("Add Parent", "Parent added successfully!")
            add_window1.destroy()
        except mysql.connector.Error as error:
            messagebox.showerror("Add Parent", f"Failed to add parent: {error}")
                
        cursor.close()
        mydb.close()

    parent_id_entry = create_label_entry_grid(add_window1, "Parent ID:  ", 1, 0)
    parent_name_entry = create_label_entry_grid(add_window1, "Parent Name:  ", 2, 0)
    student_id_entry = create_label_entry_grid(add_window1, "Student ID:  ", 3, 0)
    phone_number_entry = create_label_entry_grid(add_window1, "Phone Number:  ", 4,0)
    email_entry = create_label_entry_grid(add_window1, "Email:  ", 5, 0)
    # Buttons
    save_parent_button = Button(add_window1, text="Save", command=save_parents, font=('Arial Rounded MT Bold', 14), bg='silver')
    save_parent_button.grid(row=6, column=1, padx=5, pady=10)
    back_button = Button(add_window1, text='Close', font=('Arial', 14), bg='silver', fg='black', command=add_window1.destroy)
    back_button.grid(row=6, column=0, padx=5, pady=10)

# Function to display parent information 
def display_parents_info():
    # Create the database connection and the database cursor
    mydb = create_database_connection()
    cursor = create_database_cursor(mydb)

    # Retrieve the parent data from the database
    cursor.execute("""
                SELECT 
                    p.parent_id,
                    p.parent_name,
                    p.student_id,
                    p.parent_phoneNumber,
                    p.parent_email
                FROM parents p
                LEFT JOIN student s ON p.student_id = s.student_id
            """)
    parent_data = cursor.fetchall()

    # Create a new Tkinter window to display the parent and student information
    parent_info_window = Toplevel()
    parent_info_window.geometry('1000x600')
    parent_info_window.title('Parent and Student Information')
    parent_info_window.configure(bg='dark slate gray')
    label6 = Label(parent_info_window, text='Parent and Student Information:', font=('Arial', 20), bg='silver', fg='black')
    label6.grid(row=0, column=0, columnspan=2, padx=30, pady=10) 

    # Create the treeview table
    parent_tree = ttk.Treeview(parent_info_window, columns=['Parent ID', 'Parent Name', 'Student ID', 'Parent Phone Number', 'Parent Email'], show='headings')
    parent_tree.heading('Parent ID', text='Parent ID')
    parent_tree.heading('Parent Name', text='Parent Name')
    parent_tree.heading('Student ID', text='Student ID')
    parent_tree.heading('Parent Phone Number', text='Parent Phone Number')
    parent_tree.heading('Parent Email', text='Parent Email')
    parent_tree.grid(row=1, column=1, columnspan=4, padx=10, pady=20)
    
    # Insert the parent and student data into the treeview
    for parent in parent_data:
        parent_tree.insert('', 'end', values=parent)

    back_button = Button(parent_info_window, text='Close', font=('Arial', 14), bg='silver', fg='black', command=parent_info_window.destroy)
    back_button.grid(row=8, column=1, padx=5, pady=10)
    cursor.close()
    mydb.close()

# Function to manage parent form
def parents_form():
    parent_form = Toplevel()
    parent_form.title("Parent Form")
    parent_form.geometry('700x500')
    parent_form.configure(bg="dark slate gray")
    label7 = Label(parent_form, text='Parent Form', font=('Arial Rounded MT Bold', 20), bg='silver', fg='black', height=2, width=40)
    label7.grid(row=1, column=1, columnspan=1, pady=20)

    # Create the buttons
    add_parent_button = Button(parent_form, text='Add Parent', font=('Arial Rounded MT Bold', 14), bg='white', fg='black', command=add_parent)
    add_parent_button.grid(row=3, column=1, pady=20)

    display_parents_button = Button(parent_form, text='Display Parents', font=('Arial Rounded MT Bold', 14), bg='white', fg='black', command=display_parents_info)
    display_parents_button.grid(row=4, column=1, pady=20)

    back_button = Button(parent_form, text='Close', font=('Arial', 14), bg='white', fg='black', command=parent_form.destroy)
    back_button.grid(row=5, column=1, columnspan=1, pady=20)
