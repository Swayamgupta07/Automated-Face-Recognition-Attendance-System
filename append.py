import csv

# Function to append data to a CSV file
def append_to_csv(file_path, data):
    """
    Appends a row of data to a CSV file.

    :param file_path: Path to the CSV file.
    :param data: List of values to append as a row.
    """
    try:
        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        print(f"Data appended successfully to {file_path}!")
    except Exception as e:
        print(f"An error occurred while appending data: {e}")

# Example usage:
# Data you want to append to the CSV file
new_data = ["Asish Veshala", "15:30:00", "24/01/2025", "Present"]  # Example row with name, time, date, and status

# File path to the CSV file
file_path = 'Attendance.csv'

# Append the new data
append_to_csv(file_path, new_data)
