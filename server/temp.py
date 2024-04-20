from app import app  # Import the Flask application instance
import json
from models import db, User

# Load JSON data from file
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

# Update the user's schedule in the database
def update_user_schedule(user_id, schedule_data):
    with app.app_context():  # Ensure we're within an application context
        user = User.query.get(user_id)
        if user:
            user.ScheduleData = json.dumps(schedule_data)  # Serialize the schedule data to JSON format
            db.session.commit()
            return "Schedule updated successfully"
        else:
            return "User not found"

# Example usage
file_path = 'file_1.json'
json_data = load_json_data(file_path)
if json_data:
    user_id = "65cefe30c11a4ad7bcb7df25a69fcea4"
    result = update_user_schedule(user_id, json_data)  # Pass the loaded JSON data directly
    print(result)
else:
    print("Failed to load JSON data")
