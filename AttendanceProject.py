import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk
import csv
import face_recognition

# Path to images folder
path = 'Images_Attendance'
images = []
classNames = []

# Load images and names
if not os.path.exists(path):
    print(f"Error: Folder '{path}' not found.")
    exit()

myList = os.listdir(path)
print(f"Found images: {myList}")
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    if curImg is not None:
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    else:
        print(f"Warning: Unable to read image {cl}")
print(f"Class names: {classNames}")

def initialize_users_file(users_file):
    if not os.path.exists(users_file):
        with open(users_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "ID"])  # Write the header row
            print(f"{users_file} initialized with headers.")
    else:
        print(f"{users_file} already exists.")

def add_user(users_file, name, user_id):
    if not os.path.exists(users_file):
        print(f"Error: {users_file} does not exist. Run initialize_users_file first.")
        return

    with open(users_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, user_id])  # Add a new user
        print(f"User {name} with ID {user_id} added to {users_file}.")

def is_user_registered(users_file, name):
    if not os.path.exists(users_file):
        print(f"Error: {users_file} does not exist.")
        return False

    with open(users_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Compare names in lowercase for case-insensitive comparison
            if row["Name"].lower() == name.lower():
                return True
    return False


# Function to find encodings
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("Warning: No face detected in an image.")
    return encodeList

# Generate encodings
encodeListKnown = findEncodings(images)
print('Encoding Complete')
print("Known encodings: ", len(encodeListKnown))

# Function to mark attendance
def markAttendance(name):
    attendance_file = 'Attendance.csv'
    users_file = 'Users.csv'  # File to check registered users
    status = getAttendanceStatus(name)  # Get status from the custom function
    tString = datetime.now().strftime('%H:%M:%S')
    dString = datetime.now().strftime('%d/%m/%Y')

    # Ensure user is registered before marking attendance
    if not is_user_registered(users_file, name):
        print(f"User {name} is not registered. Attendance not marked.")
        return

    # Check if the attendance file exists; create if not
    if not os.path.exists(attendance_file):
        with open(attendance_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Time", "Date", "Status"])  # Write headers

    # Mark attendance only if not already present for today
    with open(attendance_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList if dString in line]
        if name not in nameList:
            writer = csv.writer(f)
            writer.writerow([name, tString, dString, status])  # Append data
            print(f"Attendance marked for {name} as {status}.")
        else:
            print(f"Attendance already marked for {name} today.")


    # Log late or absent individuals in Late_Absent.csv
    late_absent_file = 'Late_Absent.csv'
    if status == "Late":
        if not os.path.exists(late_absent_file):
            with open(late_absent_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Time", "Date", "Status"])  # Write headers
        with open(late_absent_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, tString, dString, status])
            print(f"Late entry logged for {name}.")


def getAttendanceStatus(name):
    # Define custom present and late times for each user
    # The format is 'HH:MM' 24-hour format
    custom_times = {
        "Mummy": {"present": "03:00", "late": "04:00"},
        "NARENDRA-MODI": {"present": "03:45", "late": "09:00"},
        "RAHUL GANDHI": {"present": "03:30", "late": "09:45"},
        "SWAYAM(ME)": {"present": "03:00", "late": "10:15"},
    }

    # Make the name comparison case-insensitive by converting both to lowercase
    name_lower = name.lower()

    # Check if the user has a custom time defined (case-insensitive)
    for key in custom_times:
        if name_lower == key.lower():  # Convert both the input name and the dictionary key to lowercase
            present_time = custom_times[key]["present"]
            late_time = custom_times[key]["late"]

            # Get the current time
            current_time = datetime.now().strftime('%H:%M')

            # If the current time is earlier than the 'present' time, the person is "Present"
            if current_time <= present_time:
                return "Present"
            # If the current time is between 'present' and 'late' time, the person is "Late"
            elif present_time < current_time <= late_time:
                return "Late"
            else:
                return "Absent"

    # If no custom time is found
    print(f"No custom time set for {name}. Using default values.")
    return "Absent" # Default status

# Function to identify absentees and attendees
def get_absentees():
    present_individuals = []
    attendance_file = 'Attendance.csv'
    late_absent_file = 'Late_Absent.csv'

    # Ensure both files exist
    if not os.path.exists(attendance_file):
        open(attendance_file, 'w').write("Name,Time,Date,Status\n")
    if not os.path.exists(late_absent_file):
        open(late_absent_file, 'w').write("Name,Time,Date,Status\n")

    # Read attendance records
    print("Reading Attendance Records...")
    with open(attendance_file, 'r') as f:
        data = f.readlines()
        for line in data:
            if line.strip() and not line.startswith("Name"):  # Skip header and empty lines
                present_individuals.append(line.split(',')[0])

    # List of all individuals
    all_individuals = ["Mummy", "NARENDRA-MODI", "RAHUL GANDHI", "SWAYAM(ME)"]

    # Determine absentees
    absentees = [person for person in all_individuals if person not in present_individuals]
    print(f"Present Individuals: {present_individuals}")
    print(f"Absent Individuals: {absentees}")
    return absentees, present_individuals

# Define tasks for each individual
task_list = {
    "Mummy": ["Task1 for Mummy", "Task2 for Mummy"],
    "NARENDRA-MODI": ["Task1 for Narendra", "Task2 for Narendra"],
    "RAHUL GANDHI": ["Task1 for Rahul", "Task2 for Rahul"],
    "SWAYAM(ME)": ["Task1 for Swayam", "Task2 for Swayam"]
}

# Function to assign work of absent individuals
def assign_work(absentees, attendees):
    if not absentees:
        print("\nAll individuals are present. No tasks need reassignment.")
        return

    print("\nAbsent individuals and their tasks:")
    for absentee in absentees:
        tasks = task_list.get(absentee, [])
        print(f"{absentee}: {tasks}")

        # Reassign tasks to available individuals
        for task in tasks:
            assigned_to = attendees[0]  # Assign tasks sequentially or replace with random.choice(attendees)
            print(f"  - '{task}' assigned to {assigned_to}")
            attendees.append(attendees.pop(0))  # Rotate attendees to balance task distribution

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to access webcam.")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Error: Unable to read image.")
        break

    # Resize and process frame
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Match current encodings with known encodings
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if faceDis[matchIndex] < 0.6:
            name = classNames[matchIndex].upper()
            markAttendance(name)
        else:
            name = "UNKNOWN"

        # Draw rectangle and label for each face
        y1, x2, y2, x1 = [v * 4 for v in faceLoc]  # Scale back up
        color = (0, 255, 0) if name != "UNKNOWN" else (0, 0, 255)  # Green for known, red for unknown
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # Display frame with bounding boxes
    cv2.imshow('Webcam', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):  # Exit on 'q'
        break

cap.release()
cv2.destroyAllWindows()

# Identify absentees and redistribute their tasks
absentees, attendees = get_absentees()
assign_work(absentees, attendees)  # Ensure this line is after the attendance collection

# GUI Interface
def createGUI():
    window = Tk()
    window.title("Attendance System")
    window.geometry("800x600")

    def viewAttendance():
        top = Toplevel(window)
        top.title("Attendance Records")
        df = pd.read_csv('Attendance.csv')
        frame = Frame(top)
        frame.pack(fill=BOTH, expand=1)
        tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")
        for col in df.columns:
            tree.heading(col, text=col)
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        tree.pack(fill=BOTH, expand=1)

    def exportToExcel():
        df = pd.read_csv('Attendance.csv')
        df.to_excel('Attendance.xlsx', index=False)
        print("Attendance exported to Attendance.xlsx")

    Label(window, text="Attendance System", font=("Arial", 20)).pack(pady=20)
    Button(window, text="View Attendance", command=viewAttendance, width=20).pack(pady=10)
    Button(window, text="Export to Excel", command=exportToExcel, width=20).pack(pady=10)
    Button(window, text="Exit", command=window.destroy, width=20).pack(pady=10)

    window.mainloop()

createGUI()
