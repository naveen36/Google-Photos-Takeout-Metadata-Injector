Certainly! Below is the updated **README** file with the new script name: **Google Photos Metadata Injector**.

---

# Google Photos Metadata Injector

## Overview

The **Google Photos Metadata Injector** script is designed to add metadata (such as geolocation, device type, and photo taken time) from JSON files to image and video files (e.g., JPG, MP4, MOV). It processes media files by reading metadata from associated `.json` files and injects it into the media files (EXIF metadata for images and a custom tag for videos). The script works recursively across directories, allowing you to process an entire folder structure.


## Features

- Adds metadata to images and videos.
- Supports various media file formats (JPG, PNG, MP4, MOV, etc.).
- Reads JSON files named similarly to media files (e.g., `file_randomName.JPG.supplemental-metadata.json`).
- Handles files with suffixes like `(1)`, `(2)` in their names (e.g., `file_randomName(1).JPG` and `file_randomName.JPG.supplemental-metadata(1).json`).
- Works recursively through directories to process all media files and matching JSON files.
- Supports image metadata injection using EXIF (for JPG, PNG, etc.).
- Attempts to embed metadata in video files (though the embedding part is a placeholder for future implementation).
- All dates in the metadata are modified to early 2025 (January 1, 2025).

## Prerequisites

Before running this script, ensure that you have the following dependencies installed:

### Required Libraries

- `piexif` for handling EXIF data in images.
- `Pillow` for image manipulation.
- `moviepy` for handling video files.
- `tkinter` for the directory selection dialog.

You can install the required libraries by running:

```bash
pip install piexif pillow moviepy
```

### Optional (FFmpeg for advanced video processing)
If you wish to embed metadata directly into video files, you might need **FFmpeg**. This script currently uses MoviePy for video manipulation, but embedding metadata in video files directly is not yet implemented.

## How to Use

1. **Clone/Download the Script**:
   Save the script to your local machine.

2. **Run the Script**:
   Open a terminal or command prompt and navigate to the directory where the script is saved. Run the following command:

   ```bash
   python google_photos_metadata_injector.py
   ```

   This will start the script and prompt you to select the folder containing the media files.

3. **Select Directory**:
   A file dialog will open. Select the folder that contains your media files (images and videos). The script will process all media files in this folder and its subdirectories.

4. **Script Execution**:
   The script will:
   - Search for the matching `.json` files for each media file (looking for files named similarly to the media file).
   - Parse the JSON files and extract metadata.
   - Inject the metadata into the corresponding media files:
     - **For images**: Metadata will be added to the EXIF data.
     - **For videos**: Metadata will be printed as a placeholder (currently no direct embedding).

5. **Obfuscated File Names**:
   The image and video file names are obfuscated to prevent the exposure of the original filenames. The script will generate random 8-character alphanumeric names for the media files.

6. **Modified Dates**:
   All dates in the metadata (such as `photoTakenTime` and `creationTime`) will be changed to early 2025 (January 1, 2025).

7. **Results**:
   - The script will print messages to the console showing which files are being processed.
   - If there is an error (e.g., missing metadata or incompatible file format), the file will be added to a list of failed files.

8. **Failed Files**:
   - At the end of execution, the script will print a list of files that failed to process.

## Example

Let's assume the folder contains the following files:

- `file_randomName.JPG`
- `file_randomName.JPG.supplemental-metadata.json`

The script will read the metadata from `file_randomName.JPG.supplemental-metadata.json` and inject it into the EXIF data of `file_randomName.JPG`.

If the file name has a suffix like `file_randomName(1).JPG`, it will look for the corresponding JSON file named `file_randomName.JPG.supplemental-metadata(1).json`.

### Example JSON Metadata

Here is an example of the JSON metadata format that the script expects:

```json
{
  "title": "file_randomName.JPG",
  "description": "",
  "imageViews": "36",
  "creationTime": {
    "timestamp": "1735660800",
    "formatted": "Jan 1, 2025, 12:00:00 AM UTC"
  },
  "photoTakenTime": {
    "timestamp": "1735660800",
    "formatted": "Jan 1, 2025, 12:00:00 AM UTC"
  },
  "geoData": {
    "latitude": 0.0,
    "longitude": 0.0,
    "altitude": 0.0,
    "latitudeSpan": 0.0,
    "longitudeSpan": 0.0
  },
  "url": "https://photos.google.com/photo/sdasdasdasdafeawgegawAFgegw",
  "googlePhotosOrigin": {
    "mobileUpload": {
      "deviceType": "IOS_PHONE"
    }
  }
}
```

### Metadata Fields Added

- **`deviceType`**: The device type (e.g., `IOS_PHONE`).
- **`latitude`**: Latitude of the location where the photo/video was taken.
- **`longitude`**: Longitude of the location where the photo/video was taken.
- **`altitude`**: Altitude of the location.
- **`photoTakenTime`**: The formatted time when the photo/video was taken (set to January 1, 2025).

## Known Issues

- **Video Metadata Embedding**: The script currently prints metadata for video files, but it does not actually embed the metadata. This could be extended by using `FFmpeg` or other tools in the future.
- **File Permissions**: Ensure the script has the necessary permissions to read and write to the media and JSON files.

## License

This script is open-source and free to use under the MIT license. Feel free to contribute or modify it as needed.

---

### End of README

Now, the README has been updated with the new script name: **Google Photos Metadata Injector**. If you need further modifications, feel free to ask!