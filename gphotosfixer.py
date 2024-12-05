import os
import json
import shutil
from datetime import datetime

def get_json_file(file_name):
    truncated_file_name = file_name
    if len(file_name) > 46:
        truncated_file_name = file_name[0:46]
    return f"{truncated_file_name}.json"

def get_photo_taken_time_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as json_file:
        try:
            metadata = json.load(json_file)
            photo_taken_time = metadata.get("photoTakenTime", {}).get("timestamp")
            return photo_taken_time
        except json.JSONDecodeError:
            print(f"Error reading JSON metadata for {json_path}.")

def organize_photos(input_folder, output_folder):
    # Supported media file extensions
    media_extensions = {".jpg", ".jpeg", ".png", ".mp4", ".mov", ".avi", ".heic"}
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        file_root, file_ext = os.path.splitext(file_name)

        # Skip non-media and non-JSON files
        if file_ext.lower() in media_extensions:
            # Look for corresponding JSON file
            json_file = get_json_file(file_name)
            json_path = os.path.join(input_folder, json_file)
            jpg_json_file = get_json_file(file_root + ".JPG")
            jpg_json_path = os.path.join(input_folder, jpg_json_file)
            photo_taken_time = None
            print(f"Finding JSON for {file_path}")
            if os.path.exists(json_path):
                # print(f"\tFound {json_path}")
                photo_taken_time = get_photo_taken_time_from_json(json_path)
            elif file_ext.lower() == ".mp4" and os.path.exists(jpg_json_path):
                # print(f"\tFound {jpg_json_path}")
                photo_taken_time = get_photo_taken_time_from_json(jpg_json_path)
            else:
                print(f"Error finding JSON file for {file_path} at {json_path} or {jpg_json_path}.")
                continue
            # print(f"\tTimestamp: {photo_taken_time}")
            
            # If metadata exists, use it; otherwise, use file's last modified time
            if photo_taken_time:
                photo_date = datetime.fromtimestamp(int(photo_taken_time))
            else:
                print(f"Error extracting timestamp for {file_name}.")
                continue

            # Create year/month folder structure
            year_month_folder = os.path.join(output_folder, f"{photo_date.year}", f"{photo_date.month:02}")
            os.makedirs(year_month_folder, exist_ok=True)
            
            # Copy the file
            shutil.copy(file_path, os.path.join(year_month_folder, file_name))

    print("Photos organized successfully!")

# Usage example
input_folder = "../dummy photos"  # Replace with your input folder path
output_folder = "../dumphotosoutput_11"  # Replace with your output folder path
organize_photos(input_folder, output_folder)
