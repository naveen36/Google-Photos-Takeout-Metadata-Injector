import os
import json
import piexif
from PIL import Image
from moviepy.editor import VideoFileClip  # Correct import for video files
from tkinter import Tk
from tkinter.filedialog import askdirectory
import re

# List to store paths of files that failed
failed_files = []

# Function to add metadata to the EXIF data of an image
def add_exif_metadata(image_path, metadata):
    try:
        print(f"Processing image: {image_path}")
        
        # Open image to get its EXIF data
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info.get("exif", b""))

        # Create EXIF tag for 'supplemental-metadata' as user comment
        user_comment = json.dumps(metadata, ensure_ascii=False)

        # Ensure the user comment is encoded to bytes
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = user_comment.encode('utf-8')

        # Convert back to byte format for piexif to save it
        exif_bytes = piexif.dump(exif_dict)

        # Save the image with updated EXIF data
        img.save(image_path, exif=exif_bytes)
        print(f"Metadata added to image {image_path}")
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        failed_files.append(image_path)  # Add to failed files list

# Function to add metadata to video files
def add_video_metadata(video_path, metadata):
    try:
        print(f"Processing video: {video_path}")
        
        # For videos, we'll store metadata as a custom tag (using moviepy or similar)
        metadata_str = json.dumps(metadata, ensure_ascii=False)
        
        # Using moviepy to open video and manipulate its metadata
        video = VideoFileClip(video_path)  # Correct usage of VideoFileClip

        # Just print the metadata as a placeholder for actual embedding
        print(f"Adding metadata to video {video_path}: {metadata_str}")
        
        # For actual metadata embedding, consider using FFmpeg (not implemented here)
        # moviepy does not provide direct metadata manipulation for containers
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")
        failed_files.append(video_path)  # Add to failed files list

# Function to process each file in the current directory
def process_directory(root_dir):
    print(f"Scanning directory: {root_dir}")
    
    # Define the regex pattern for matching json filenames with random data
    json_pattern = re.compile(r"^(.*\.\w+)\..*\.json$")

    # Loop through all files in the current directory and subdirectories
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            media_path = os.path.join(root, file)
            base_name, ext = os.path.splitext(file)

            # Check if the file is an image or video file (e.g., JPG, PNG, MP4, MOV, etc.)
            if ext.lower() in ['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi']:
                print(f"Found media file: {media_path}")

                # Search for the corresponding JSON file in the current directory
                json_file = None

                # Check for suffixes (e.g., DSC00052(1).JPG) and look for the matching JSON file
                # 1. Remove suffix like (1) from the base name for matching.
                base_name_without_suffix = re.sub(r'\(\d+\)', '', base_name)
                
                # 2. Try to find the JSON file by checking against the base name (including suffixes)
                for candidate in os.listdir(root):
                    if candidate.endswith(".json"):
                        json_base_name, json_ext = os.path.splitext(candidate)

                        # Check if the candidate matches the base name pattern
                        if base_name_without_suffix in json_base_name:
                            json_file = os.path.join(root, candidate)
                            break  # Stop once a match is found

                # Print for debugging purposes to check the JSON paths being searched
                print(f"Checking for JSON file: {json_file}")

                if json_file:
                    try:
                        # Read the JSON metadata
                        with open(json_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        print(f"Loaded metadata from: {json_file}")

                        # Extract relevant fields from the JSON metadata
                        media_metadata = {
                            'deviceType': metadata.get('googlePhotosOrigin', {}).get('mobileUpload', {}).get('deviceType'),
                            'latitude': metadata.get('geoData', {}).get('latitude'),
                            'longitude': metadata.get('geoData', {}).get('longitude'),
                            'altitude': metadata.get('geoData', {}).get('altitude'),
                            'photoTakenTime': metadata.get('photoTakenTime', {}).get('formatted')
                        }

                        # Add metadata to the file based on its type (image or video)
                        if ext.lower() in ['.jpg', '.jpeg', '.png']:
                            add_exif_metadata(media_path, media_metadata)
                        elif ext.lower() in ['.mp4', '.mov', '.avi']:
                            add_video_metadata(media_path, media_metadata)
                        else:
                            print(f"Unsupported format for {file}")
                    except Exception as e:
                        print(f"Error processing metadata for {json_file}: {e}")
                        failed_files.append(json_file)  # Add JSON metadata file to failed list
                else:
                    print(f"\033[91mNo matching JSON metadata file found for {file}\033[0m")
                    failed_files.append(media_path)  # Add media file to failed list

# Ask user to select an input directory using tkinter file dialog
def ask_for_directory():
    # Hide the tkinter root window
    Tk().withdraw()

    # Open a directory selection dialog and return the selected directory
    directory = askdirectory(title="Select the folder containing media files")
    if directory:
        return directory
    else:
        print("No directory selected.")
        return None

# Main function to start the process
def main():
    # Ask user to select the input directory
    root_directory = ask_for_directory()
    
    # If a directory is selected, process it
    if root_directory:
        process_directory(root_directory)

    # Print the list of failed files
    if failed_files:
        print("\nThe following files failed:")
        for file in failed_files:
            print(file)
    else:
        print("\nAll files processed successfully!")

# Run the script
if __name__ == "__main__":
    main()
