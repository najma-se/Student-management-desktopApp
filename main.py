from dotenv import load_dotenv
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from user_form import *
from parent_form import *
from Student_form import *

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


# Function to display the dashboard
def show_dashboard():
    # Create the dashboard window
    dashboard = Tk()
    dashboard.title("School Management System - Dashboard")
    dashboard.geometry('700x500')
    dashboard.configure(bg="dark slate gray")
    label1 = Label(dashboard, text='Welcome to School Management System', font=('Arial Black', 20), bg='silver', fg='black', height=2, width=40)
    label1.grid(row=1, column=1, columnspan=1, pady=20)

    # Create menu option for opening the student management system form
    student_management_button = Button(dashboard, text="Student Registration Form", command=open_student_management_system, 
                                       font=('Arial Rounded MT Bold', 14), bg='white', fg='black')
    student_management_button.grid(row=3, column=1, columnspan=1, pady=20)
    # Create menu option for parent form
    parent_form_button = Button(dashboard, text="Parent Form", command=parents_form, font=('Arial Rounded MT Bold', 14), bg='white', fg='black')
    parent_form_button.grid(row=4, column=1, columnspan=1, pady=20)
    # Create menu option for user form
    users_form_button = Button(dashboard, text="Users", command=user_info, font=('Arial Rounded MT Bold', 14), bg='white', fg='black')
    users_form_button.grid(row=5, column=1, columnspan=1, pady=20)

    back_button = Button(dashboard, text='Close', font=('Arial', 14), bg='white', fg='black', command=dashboard.destroy)
    back_button.grid(row=6, column=1, columnspan=1, padx=10, pady=30)
    dashboard.mainloop()

# Login function
def login():
    # Create the database connection and the database cursor
    mydb = create_database_connection()
    cursor = create_database_cursor(mydb)

    username = username_entry.get()
    password = password_entry.get()
    # Execute the query to check if the user exists
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Login", "Login successful")
        root.destroy()  # Close the login window
        show_dashboard()
    else:
        messagebox.showerror("Login", "Invalid username or password")

    cursor.close()
    mydb.close()

root = Tk()
root.title("School Management System")
root.configure(bg="dark slate gray")
root.geometry("800x400")
title_label = Label(root, text="Login", font=('arial black', 25), bg='silver', fg='black', height=0, width=30)
title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

username_label = Label(root, text="Username:", font=("Arial Rounded MT Bold", 16), bg='dark slate gray')
username_label.grid(row=1, column=0, padx=10, pady=10)
username_entry = Entry(root, width=20, font=('arial', 14))
username_entry.grid(row=1, column=1, padx=10, pady=10)

password_label = Label(root, text="Password:", font=("Arial Rounded MT Bold", 16), bg='dark slate gray')
password_label.grid(row=2, column=0, padx=10, pady=10)
password_entry = Entry(root, show="*", width=20, font=('arial', 14))
password_entry.grid(row=2, column=1, padx=10, pady=10)

login_button = Button(root, text="Login", command=login, font=("Arial Rounded MT Bold", 14), bg='silver', fg='black')
login_button.grid(row=3, column=0, columnspan=2, pady=20)
root.mainloop()

def main():
    login()
