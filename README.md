# Automated-Face-Recognition-Attendance-System
This project is an Automated Face Recognition Attendance System that detects and recognizes faces from images to mark attendance. It leverages OpenCV and face-recognition libraries to identify individuals and log attendance in a CSV file.

Features

Face detection and recognition using OpenCV and dlib

Attendance tracking with automatic CSV updates

Supports multiple users by adding images to the Images_Attendance folder

Identifies known and unknown faces

Generates separate logs for late and absent users

Prerequisites

Ensure you have the following installed on your system:

Python 3.8+

Required Python libraries:

pip install opencv-python numpy pandas face-recognition

Project Setup

Clone the repository:

git clone https://github.com/Swayamgupta07/Automated-Face-Recognition-Attendance-System.git
cd Automated-Face-Recognition-Attendance-System

Create a folder for storing images:

Manually create a folder named Images_Attendance in the project directory.

Add images of individuals who need to be recognized.

Each image should be named as the person's full name (e.g., John_Doe.jpg).

python AttendanceProject.py

Marking Attendance:

The program will scan faces and update the Attendance.csv file with the person's name and timestamp.

If a person is late, their details are logged in Late_Absent.csv.

Adding More Users

To add more individuals, place their images inside the Images_Attendance folder.

Make sure to append their names correctly in the CSV file if needed.

Run the script again to include them in the recognition system.

Files Overview

AttendanceProject.py - Main script to run face recognition

Attendance.csv - Logs recognized individuals with timestamps

Late_Absent.csv - Tracks late or absent users

Users.csv - Stores registered users

setup_users.py - Helper script to register users

Images_Attendance/ - Folder containing images of recognized individuals

Notes

Ensure good lighting and clear images for better recognition.

Images should have faces clearly visible and not obstructed.

The system may require retraining if a new user is added frequently.

Contributing

If you wish to improve this project, feel free to fork and submit a pull request!

License

This project is open-source and free to use.
