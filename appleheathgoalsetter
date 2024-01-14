import boto3
import csv
from datetime import datetime, timedelta, timezone
from io import StringIO

# Constants (replace these with your actual values)
CSV_FILE_PATH = '/Users/markferry/Downloads/apple_health_export/Workout.csv'  # Path to your CSV file
OUTPUT_HTML_FILE_PATH = '/Users/markferry/Downloads/apple_health_export/workoutgoal.html'  # Path to output HTML file
S3_BUCKET_NAME = 'ferrytheboatworkouttracker'  # Your S3 bucket name
S3_OBJECT_KEY = 'workoutgoal.html'  # S3 object key (file name in S3)

# Function to process the CSV and generate HTML content
def process_workouts(csv_content):
    def parse_health_data(csv_data):
        workouts = []
        reader = csv.DictReader(StringIO(csv_data))
        for row in reader:
            try:
                workout_date = datetime.strptime(row['startDate'], '%Y-%m-%d %H:%M:%S %z')
                duration = float(row['duration'])
                if row['durationUnit'] == 'min' and duration >= 30:
                    workouts.append(workout_date)
            except ValueError:
                continue
        return workouts

    def analyze_workouts(workouts, start_date):
        current_date = start_date
        week_count = 0
        successful_weeks = 0

        while current_date < datetime.now(timezone.utc):
            week_end = current_date + timedelta(days=7)
            week_workouts = [d for d in workouts if current_date <= d < week_end]
            if len(week_workouts) >= 4:
                successful_weeks += 1
            week_count += 1
            current_date = week_end

        return successful_weeks, week_count

    workouts = parse_health_data(csv_content)
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)  # Adjust as needed
    successful_weeks, total_weeks = analyze_workouts(workouts, start_date)
    html_content = """
        <html>
        <head>
            <style>
                body {{
                    background-color: black;
                    color: #DB4F3D; /* Updated text color */;
                    font-family: Arial, sans-serif;
                }}
            </style>
        </head>
        <body>
            <h1>Workout Summary</h1>
            <p>You have met your workout goals {} of {} weeks.</p>
        </body>
        </html>
        """.format(successful_weeks, total_weeks)

    return html_content

# Read the CSV file
with open(CSV_FILE_PATH, 'r') as file:
    csv_content = file.read()

# Generate HTML content
html_content = process_workouts(csv_content)

# Write the HTML content to a file
with open(OUTPUT_HTML_FILE_PATH, 'w') as html_file:
    html_file.write(html_content)

# Upload the HTML file to S3
s3_client = boto3.client('s3')
s3_client.upload_file(OUTPUT_HTML_FILE_PATH, S3_BUCKET_NAME, S3_OBJECT_KEY, ExtraArgs={'ContentType': 'text/html'})
print("HTML file uploaded to S3 successfully.")

# Don't forget to configure your AWS credentials before running the script
