from dotenv import load_dotenv
import os
from tkinter import *
from tkinter import ttk, messagebox
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

# Function to habdle all user information
def user_info():
    # Function to add a new user
    def add_user():
        mydb = create_database_connection()
        cursor = create_database_cursor(mydb)

        full_name = full_name_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match. Please try again.")
        else:
            try:
                # Insert the new user into the database
                sql = "INSERT INTO users (id, full_name, username, password) VALUES (%s, %s, %s, %s)"
                values = (id_entry.get(), full_name, username, password)
                cursor.execute(sql, values)
                mydb.commit()
                messagebox.showinfo("Registration Successful", "User registered successfully!")
                refresh_grid()
                clear_entries()  # Clear entry fields after successful registration
            except mysql.connector.Error as error:
                messagebox.showerror("Registration Error", f"An error occurred: {error}")
            finally:
                cursor.close()
                mydb.close()

    # Function to update a user
    def update():
        mydb = create_database_connection()
        cursor = create_database_cursor(mydb)

        # Get the selected item from the grid view
        selected_item = tree.selection()
        if len(selected_item) == 0:
            messagebox.showerror("Update Error", "Please select a row to update.")
            return

        # Get the values from the selected row
        selected_row = tree.item(selected_item)['values']
        selected_id = selected_row[0]
        full_name = full_name_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        try:
            # Update the selected row in the database
            sql = "UPDATE users SET full_name = %s, username = %s, password = %s WHERE id = %s"
            values = (full_name, username, password, selected_id)
            cursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Update Successful", "User data updated successfully!")
            refresh_grid()  # Refresh the grid after updating
            clear_entries()  # Clear entry fields after successful update
        except mysql.connector.Error as error:
            messagebox.showerror("Update Error", f"An error occurred: {error}")
        finally:
            cursor.close()
            mydb.close()

    # Function to delete a user
    def delete():
        mydb = create_database_connection()
        cursor = create_database_cursor(mydb)

        # Get the selected item from the grid view
        selected_item = tree.selection()
        if len(selected_item) == 0:
            messagebox.showerror("Delete Error", "Please select a row to delete.")
            return

        # Get the values from the selected row
        selected_row = tree.item(selected_item)['values']
        selected_id = selected_row[0]

        try:
            # Delete the selected row from the database
            sql = "DELETE FROM users WHERE id = %s"
            cursor.execute(sql, (selected_id,))
            mydb.commit()
            messagebox.showinfo("Delete Successful", "User data deleted successfully!")
            refresh_grid()  # Refresh the grid after deleting
            clear_entries()  # Clear entry fields after successful deletion
        except mysql.connector.Error as error:
            messagebox.showerror("Delete Error", f"An error occurred: {error}")
        finally:
            cursor.close()
            mydb.close()

    # Function to refresh the user grid
    def refresh_grid():
        mydb = create_database_connection()
        cursor = create_database_cursor(mydb)

        # Clear the existing data in the grid
        tree.delete(*tree.get_children())

        # Fetch the data from the database and populate the grid
        cursor.execute("SELECT id, full_name, username, password FROM users")
        results = cursor.fetchall()
        for row in results:
            tree.insert("", "end", values=row)
        cursor.close()
        mydb.close()

    # Function to clear the username and password entries
    def clear_entries():
        # Clear entry fields
        id_entry.delete(0, END)
        full_name_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        confirm_password_entry.delete(0, END)

    def on_double_click(event):
        item = tree.selection()[0]
        values = tree.item(item, 'values')
        id_entry.delete(0, END)
        full_name_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        id_entry.insert(0, values[0])
        full_name_entry.insert(0, values[1])
        username_entry.insert(0, values[2])
        password_entry.insert(0, values[3])

    # Create main window
    user_window = Toplevel()
    user_window.title("School Management System")
    user_window.configure(bg="dark slate gray")
    user_window.geometry("800x600")
    user_window.grab_set()
    user_label = Label(user_window, text="Username Info", bg="silver", fg="black", font=("Times New Roman", 30))
    user_label.grid(row=0, column=0, columnspan=2, pady=10)

    id_entry = create_label_entry_grid(user_window, "User ID:  ", 1, 0)
    full_name_entry = create_label_entry_grid(user_window, "Full name:  ", 2, 0)
    username_entry = create_label_entry_grid(user_window, "Username:  ", 3, 0)

    # Password
    password_label = Label(user_window, text="Password:", font=('times new roman', 18), bg='dark slate gray', fg='black')
    password_label.grid(row=4, column=0, pady=10, padx=5, sticky='w')
    password_entry = Entry(user_window, show="*", font=(18))
    password_entry.grid(row=4, column=1, sticky="W")

    # Confirm Password
    confirm_password_label = Label(user_window, text="Confirm Password:", font=('times new roman', 18), bg='dark slate gray', fg='black' )
    confirm_password_label.grid(row=5, column=0, pady=10, padx=5, sticky='w')
    confirm_password_entry = Entry(user_window, show="*", font=(18))
    confirm_password_entry.grid(row=5, column=1, sticky="W")

    # Register Button
    save_button = Button(user_window, text="Save", command=add_user, font=('Arial', 15), bg='silver')
    save_button.grid(row=6, column=0, padx=5, pady=10)

    update_button = Button(user_window, text="Update", command=update, font=('Arial', 15), bg='silver')
    update_button.grid(row=6, column=1, padx=10, pady=10)

    delete_button = Button(user_window, text="Delete", command=delete, font=('Arial', 15), bg='silver')
    delete_button.grid(row=6, column=2, padx=5, pady=10)

    clear_button = Button(user_window, text="Clear", command=clear_entries, font=('Arial', 15), bg='silver')
    clear_button.grid(row=7, column=0, padx=5, pady=10)

    close_button = Button(user_window, text="Close", command=user_window.destroy, font=('Arial', 15), bg='silver')
    close_button.grid(row=7, column=1, padx=5, pady=10)

    # Treeview
    tree = ttk.Treeview(user_window, columns=("ID", "Full Name", "Username", "Password"), show="headings", height=15)
    tree.grid(row=8, column=0, columnspan=4, padx=10, pady=20)

    # Treeview Columns and Headings
    tree.column("ID", width=100, anchor="center")
    tree.heading("ID", text="ID")
    tree.column("Full Name", width=200, anchor="center")
    tree.heading("Full Name", text="Full Name")
    tree.column("Username", width=150, anchor="center")
    tree.heading("Username", text="Username")
    tree.column("Password", width=150, anchor="center")
    tree.heading("Password", text="Password")
    """
    # Scrollbar
    scrollbar = ttk.Scrollbar(user_window, orient="vertical", command=tree.yview)
    scrollbar.grid(row=8, column=4, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)
    """
    # Binding double-click event to the treeview
    tree.bind("<Double-1>", on_double_click)

    # Fetch data from the database and populate the treeview
    refresh_grid()

    # Start the main loop
    user_window.mainloop()