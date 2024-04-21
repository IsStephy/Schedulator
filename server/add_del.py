import json
from classes import Teacher, Course, Group, Offices
from typing import Any
from models import db


def data_exists_in_json(user_id, data: Any) -> bool:
    try:
        user = db.query.get(user_id)
        existing_data = json.loads(user.ScheduleData)
        for entry in existing_data:
            if entry['type'] == 'Group' and entry['data']['name'] == data.name:
                return True
    except (
            FileNotFoundError):
        pass
    except Exception as e:
        print("Error checking data in JSON:", e)
    return False


def add_data_to_json(user_id, data_type: str, data: Any):
    try:
        if not data_exists_in_json(user_id, data):
            try:
                user = db.query.get(user_id)
                existing_data = json.loads(user.ScheduleData)
            except json.decoder.JSONDecodeError:
                existing_data = []

            data_dict = {"type": data_type, "data": data.__dict__}
            existing_data.append(data_dict)
            user.ScheduleData = json.dumps(existing_data)
            db.session.commit()
    except Exception as e:
        print("Error adding data to JSON:", e)


def remove_data_from_json(user_id, name):
    try:
        user = db.query.get(user_id)
        if user and user.ScheduleData:
            data = json.loads(user.ScheduleData)
            updated_data = [entry for entry in data if entry['data']['name'] != name]
            user.ScheduleData = json.dumps(updated_data)
            db.session.commit()
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except Exception as e:
        print("Error removing data from JSON:", e)