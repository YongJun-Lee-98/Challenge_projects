# Import necessary libraries
import subprocess
import pandas as pd
import time
import csv
import sys
import json
import tkinter as tk
import pymysql
import os

from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from phrase_utils import load_phrases_from_csv, insert_selected_phrase, remove_selected_phrase
from tkinter import messagebox
from tkinter import simpledialog

# Set up the system input
sys.stdin.reconfigure(encoding='utf-8')

frequently_used_phrases = load_phrases_from_csv('frequently_used_phrases.csv')
# Load configuration from the JSON file
with open('config.json') as f:
    config = json.load(f)

# Get the user from the user input
def get_username():
    # Create a new root for the dialog
    dialog_root = tk.Tk()
    dialog_root.withdraw()  # Hide the main window

    # Open a simple dialog that asks for the username
    user = tk.simpledialog.askstring("Username", "Enter your MySQL username:", parent=dialog_root)

    dialog_root.destroy()  # Destroy the dialog root

    return user

def clear_csv_file(filename):
    with open(filename, 'w') as file:
        pass

def run_adb_shell_command(command):
    print("Trying USB connection...")
    cmd = ['adb', 'shell'] + command
    output = subprocess.check_output(cmd)
    return output.decode('utf-8')

def add_selected_contact():
    selected_index = listbox_contacts.curselection()[0]
    selected_contact = contacts_df.iloc[selected_index]
    phone_number = selected_contact['number']
    entry_phone_number.delete(0, tk.END)  # Clear the existing content
    entry_phone_number.insert(0, phone_number)  # Insert the phone number into the entry box

def process_contact():
    entered_display_name = entry_display_name.get()
    matching_contacts = contacts_df[contacts_df['display_name'] == entered_display_name]

    if matching_contacts.empty:
        messagebox.showwarning("No Matching Contact", "No matching contact found. Please enter the phone number.")
    else:
        phone_number = matching_contacts['number'].iloc[0]
        entry_phone_number.delete(0, tk.END)  # Clear the existing content
        entry_phone_number.insert(0, phone_number)  # Insert the phone number into the entry box

def send_sms():
    phone_number = entry_phone_number.get()
    message = entry_message.get("1.0", tk.END).strip()
    
    # Create the table if it doesn't exist
    cursor = mydb.cursor()
    # Create a table for storing phone numbers, messages, and users, if it doesn't exist
    mycursor.execute("""CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        phone_number VARCHAR(255),
                        message TEXT,
                        user VARCHAR(255)
                    )""")
    # Insert the data into the MySQL database
    query = "INSERT INTO messages (phone_number, message, user) VALUES (%s, %s, %s)"
    cursor.execute(query, (phone_number, message, user))
    mydb.commit()
    time.sleep(2)

    # Clear the content in the entry and text boxes
    entry_phone_number.delete(0, tk.END)
    entry_message.delete('1.0', tk.END)
    # Start the app
    subprocess.run(["adb", "shell", "am", "start", "-n", "com.example.sms_app/.MainActivity"])

    # Wait for 10 seconds
    time.sleep(10)

    # Stop the app
    subprocess.run(["adb", "shell", "am", "force-stop", "com.example.sms_app"])
        # Update the send button state
    update_button_send_state()


def update_button_send_state(*_):
    phone_number = entry_phone_number.get()
    message = entry_message.get("1.0", tk.END).strip()
    if phone_number and message:
        button_send.config(state=tk.NORMAL)
    else:
        button_send.config(state=tk.DISABLED)

def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("문구추가")
    new_window.geometry("200x60")

    entry = tk.Entry(new_window)
    entry.pack()


    def insert_phrase():
        new_phrase = entry.get()
        with open('frequently_used_phrases.csv', 'a', newline='') as f:
            f.write("\n" + new_phrase)
        entry.delete(0, tk.END)
        listbox_phrases.delete(0, tk.END)
        frequently_used_phrases.append(new_phrase)
        for index, phrase in enumerate(frequently_used_phrases):
            listbox_phrases.insert(index, phrase)
    btn_insert = tk.Button(new_window, text="삽입", command=insert_phrase)
    btn_insert.pack()

# Get the user from the user input
user = get_username()

# Update the config dictionary with the new user value
config['user'] = user

# Save the updated config dictionary to the config.json file
with open('config.json', 'w') as f:
    json.dump(config, f)

# Connect to the MySQL database
mydb = pymysql.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    db=config["database"]
)

mycursor = mydb.cursor()
# Create a table for storing phone numbers, messages, and users, if it doesn't exist
mycursor.execute("""CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        phone_number VARCHAR(255),
                        message TEXT,
                        user VARCHAR(255)
                    )""")

adb_devices_output = subprocess.check_output(['adb', 'devices']).decode('utf-8')
if 'unauthorized' in adb_devices_output:
    print("Please check the connected device and authorize this computer.")
    exit(1)
elif 'device' not in adb_devices_output:
    print("No device connected. Please connect your Android device via USB.")
    exit(1)


# Run the adb shell command and get the output
cmd = ['adb', 'shell', 'content', 'query', '--uri', 'content://com.android.contacts/data/phones', '--projection', 'display_name:data1']
output = subprocess.check_output(cmd)
clear_csv_file('contacts.csv')

# Decode the binary output to a string
output_str = output.decode('utf-8')

# Split the string into lines and remove any trailing newline characters
lines = [line.strip() for line in output_str.split('\n')]

# Create a list of dictionaries, where each dictionary represents a row in the output
rows = []
for line in lines:
    if ',' in line:
        name, number = line.split(',')
        name = name.split('=', 1)[-1].strip()
        number = number.split('=', 1)[-1].strip()
        number = number.replace('-', '')
        number = number.replace(' ', '')
        if number.startswith('1'):
            number = '0' + number


        try:
            rows.append({'display_name': name, 'number': number})
        except Exception as e:
            print(f"Error while appending row: {e}")  # 에러 발생 시 에러 메시지 출력



# Save the list of dictionaries to a CSV file
with open('contacts.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['display_name', 'number'])
    writer.writeheader()
    writer.writerows(rows)


# Read the CSV file and display the contacts
contacts_df = pd.read_csv('contacts.csv', dtype={'number': str})

# Create a Tkinter window for the GUI
root = tk.Tk()
root.title("메세지 보내기")

# tk img_section
# Create and populate the listbox with contact names

# Load frequently used phrases from CSV

container1 = tk.Frame(root)
container1.grid(row=0,column=0, sticky='n')


intro_listbox = "원하는 사람을 누르고 선택을 눌러주세요"
intro_label = tk.Label(container1, text=intro_listbox)
intro_label.grid(row=0, column=0, columnspan=2)

listbox_contacts = tk.Listbox(container1,width=30, height=10)
for index, row in contacts_df.iterrows():
    # print(row['number'])  # Debug: print the phone number
    listbox_contacts.insert(index, f"{row['display_name']} ({row['number']})")
listbox_contacts.grid(row=1,column=0,columnspan=2)

# Create a button to add the selected contact's phone number to the entry box
button_add = tk.Button(container1, text="선택", command=add_selected_contact)
button_add.grid(row=2, column=1)

intro_listbox2 = "원하는 사람 입력하고 찾기를 눌러주세요"
intro_label2 = tk.Label(container1, text=intro_listbox2)
intro_label2.grid(row=3, column=0, columnspan=2)

# Create an entry box for the display_name input
entry_display_name = tk.Entry(container1)
entry_display_name.grid(row=4, column=0, columnspan=2)

# Create a button to proceed with the entered contact name or phone number
button_proceed = tk.Button(container1, text="찾기", command=process_contact)
button_proceed.grid(row=5, column=1)

intro_listbox3 = " ↧번호 입력칸(번호 없을시 전화번호 숫자만 입력)"
intro_label3 = tk.Label(container1, text=intro_listbox3)
intro_label3.grid(row=6, column=0, columnspan=2)

# Create an entry box for the phone number input (optional)
phone_number_var = tk.StringVar()
phone_number_var.trace_add("write", update_button_send_state)

entry_phone_number = tk.Entry(container1,textvariable=phone_number_var)
entry_phone_number.grid(row=7, column=0, columnspan=2, pady=10)

container2 = tk.Frame(root)
container2.grid(row=0, column=1, sticky='n')

# 자주 사용문구
intro_listbox3 = "문구를 선택하고 메세지 삽입을 눌러주세요"
intro_label2 = tk.Label(container2, text=intro_listbox3)
intro_label2.grid(row=0, column=0, columnspan=2)

# Create a listbox for frequently used phrases
listbox_phrases = tk.Listbox(container2,width=30, height=10)
for index, phrase in enumerate(frequently_used_phrases):
    listbox_phrases.insert(index, phrase)
listbox_phrases.grid(row=1, column=0, columnspan=2)

# Create a button to add a new phrase
button_add_phrase = tk.Button(container2, text="구문추가", command=open_new_window)
button_add_phrase.grid(row=3, column=0, pady=5)

# Create a button to remove the selected phrase
button_remove_phrase = tk.Button(container2, text="선택된 구문 제거", command=lambda: remove_selected_phrase(listbox_phrases, frequently_used_phrases, 'frequently_used_phrases.csv'))
button_remove_phrase.grid(row=3, column=1, pady=5)

# Create a button to insert the selected phrase
button_insert = tk.Button(container2, text="메세지 삽입", command=lambda: insert_selected_phrase(entry_message, listbox_phrases), bg="blue", fg="white")
button_insert.grid(row=4, column=1)

container3 = tk.Frame(root)
container3.grid(row=1, column=0, rowspan=1, columnspan=2)

intro_listbox4 = "메세지 내용을 입력해주세요"
intro_labe5 = tk.Label(container3, text=intro_listbox4)
intro_labe5.grid(row=0, column=0, columnspan=2)

# Create an text box for the message
entry_message = tk.Text(container3)
entry_message.bind("<KeyRelease>", update_button_send_state)
entry_message.grid(row=1, column=0, rowspan=3, columnspan=2)

# Create a button to send the SMS
button_send = tk.Button(container3, text="메세지 전송", command=send_sms, state=tk.DISABLED, bg="blue", fg="yellow")
button_send.grid(row=4, column=1)


# Start the Tkinter main loop
root.mainloop()