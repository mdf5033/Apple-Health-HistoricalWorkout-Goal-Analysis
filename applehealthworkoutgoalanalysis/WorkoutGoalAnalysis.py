from io import StringIO
import pandas as pd
import csv
from datetime import datetime, timedelta, timezone
from dateutil import parser
import tkinter as tk
from tkinter import filedialog

# Function to allow the user to browse to the file location
def browse_file():
    root = tk.Tk()
    root.withdraw()  # Prevents the Tkinter window from coming up
    file_path = filedialog.askopenfilename()
    return file_path

# Function to try parsing the date with multiple formats
def try_parse_date(date_str):
    try:
        # Using dateutil's parser to handle variable formats
        return parser.parse(date_str)
    except ValueError:
        return None

# Function to parse the health data with flexible date parsing
def parse_health_data_flexible(csv_data, min_duration):
    workouts = []
    reader = csv.DictReader(StringIO(csv_data))
    for row in reader:
        try:
            workout_date = try_parse_date(row['startDate'])
            if not workout_date:
                raise ValueError(f"Unable to parse date: {row['startDate']}")

            duration = float(row['duration'])  # Convert duration to float
            if row['durationUnit'].lower() == 'min' and duration >= min_duration:
                workouts.append(workout_date)
        except ValueError as e:
            print(f"Error parsing row: {row}, Error: {e}")
            continue  # Ensure 'continue' is inside the except block
    print(f"Total workouts parsed: {len(workouts)}")  # Diagnostic print
    return workouts


# Function to analyze workouts
def analyze_workouts(workouts, start_date, num_workouts_per_week):
    current_date = start_date
    week_count = 0
    successful_weeks = 0

    # Calculate the start of the current week, making sure it's a datetime object with a timezone
    today = datetime.now(timezone.utc)
    start_of_current_week = datetime(today.year, today.month, today.day, tzinfo=timezone.utc) - timedelta(days=today.weekday())

    while current_date < start_of_current_week:
        week_end = current_date + timedelta(days=7)
        week_workouts = [d for d in workouts if current_date <= d < week_end]

        if len(week_workouts) >= num_workouts_per_week:
            successful_weeks += 1

        week_count += 1
        current_date = week_end
        print(f"Week starting {current_date}: {len(week_workouts)} workouts")  # Diagnostic print
    return successful_weeks, week_count



# Main function to process the CSV and analyze workout data
def process_workouts(csv_file_path, start_date, num_workouts_per_week):
    # Read the CSV file
    df = pd.read_csv(csv_file_path, parse_dates=['startDate'])
    csv_content = df.to_csv(index=False)
    workouts = parse_health_data_flexible(csv_content, min_duration)
    return analyze_workouts(workouts, start_date, num_workouts_per_week)

# User inputs for file path
csv_file_path = browse_file()

# Prompt for the start date
start_date_input = input(
    "What date would you like to start tracking your goal from (YYYY-MM-DD) or type 'earliest' to start from the earliest date in your file: ")

# Prompt for the minimum workout duration
min_duration = float(input("Enter the minimum duration of each workout in minutes: "))

# Determine the start date
if start_date_input.lower() == 'earliest':
    df = pd.read_csv(csv_file_path, parse_dates=['startDate'])
    start_date = df['startDate'].min().to_pydatetime()
else:
    # Adjust the start date to be timezone-aware
    eastern_timezone = timezone(timedelta(hours=-5))  # Eastern Time Zone (UTC-5)
    start_date = datetime.strptime(start_date_input, '%Y-%m-%d')
    start_date = start_date.replace(tzinfo=eastern_timezone)

    # More user inputs
desired_workouts_per_week = int(input("Enter the number of desired workouts per week: "))

# Process workouts and display message
successful_weeks, total_weeks = process_workouts(csv_file_path, start_date, desired_workouts_per_week)
print(f"You met your workout goal {successful_weeks} of {total_weeks} weeks since {start_date.date()}.")

