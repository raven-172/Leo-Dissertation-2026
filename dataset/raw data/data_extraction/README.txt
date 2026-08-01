BATCH FRAME EXTRACTOR
=====================

1. OVERVIEW
-----------

This package extracts frames from one video or from all supported videos
inside a folder.

The script uses Uniform Frame Sampling. By default, it extracts one frame
every 10 seconds.

For every video, the script reports:

- Processing status
- Number of extracted images
- Processing time
- Output folder

It also creates a CSV report in the main output folder.


2. INCLUDED FILES
-----------------

extract_frames_cli.py
    The Python command-line program.

README.txt
    This instruction file.


3. REQUIREMENTS
---------------

- Windows, macOS, or Linux
- Python 3.10 or newer
- FFmpeg

No additional Python packages are required.


4. CHECK PYTHON
---------------

Open Command Prompt or Terminal and run:

    python --version

If the command does not work, try:

    python3 --version


5. INSTALL AND CHECK FFMPEG
---------------------------

After installing FFmpeg, run:

    ffmpeg -version

If this command works, FFmpeg is available in the system PATH.

If FFmpeg is not available in PATH, you can provide the full path to
ffmpeg.exe by using the --ffmpeg option.


6. BASIC COMMAND
----------------

Windows example:

    python extract_frames_cli.py --input "D:\CCTV Videos" --output "D:\CCTV Frames" --interval 10

Short form:

    python extract_frames_cli.py -i "D:\CCTV Videos" -o "D:\CCTV Frames" -t 10

macOS or Linux example:

    python3 extract_frames_cli.py --input "/Users/name/CCTV Videos" --output "/Users/name/CCTV Frames" --interval 10


7. COMMAND OPTIONS
------------------

-i, --input
    Required.
    Input video file or folder containing videos.

-o, --output
    Required.
    Output folder used to save extracted frames.

-t, --interval
    Optional.
    Extract one frame every N seconds.
    Default value: 10

--recursive
    Optional.
    Search for videos inside all input subfolders.

--overwrite
    Optional.
    Process completed videos again and replace their extracted frames.

--ffmpeg
    Optional.
    Full path to ffmpeg.exe or the FFmpeg executable.


8. COMMAND EXAMPLES
-------------------

Extract one frame every 10 seconds:

    python extract_frames_cli.py -i "D:\Videos" -o "D:\Frames" -t 10

Extract one frame every 5 seconds:

    python extract_frames_cli.py -i "D:\Videos" -o "D:\Frames" -t 5

Process one video file:

    python extract_frames_cli.py -i "D:\Videos\camera01.mp4" -o "D:\Frames" -t 10

Search all subfolders:

    python extract_frames_cli.py -i "D:\Videos" -o "D:\Frames" -t 10 --recursive

Process completed videos again:

    python extract_frames_cli.py -i "D:\Videos" -o "D:\Frames" -t 10 --overwrite

Use a specific FFmpeg executable:

    python extract_frames_cli.py -i "D:\Videos" -o "D:\Frames" -t 10 --ffmpeg "C:\ffmpeg\bin\ffmpeg.exe"


9. SUPPORTED VIDEO FORMATS
--------------------------

- MP4
- AVI
- MOV
- MKV
- M4V
- WMV
- FLV
- TS
- MTS
- M2TS


10. OUTPUT STRUCTURE
--------------------

Example input folder:

    D:\CCTV Videos
    |-- Camera01_0800-0900.mp4
    |-- Camera01_0900-1000.mp4
    `-- Camera02_0800-0900.mp4

Example output folder:

    D:\CCTV Frames
    |-- Camera01_0800-0900
    |   |-- frame_000001.jpg
    |   |-- frame_000002.jpg
    |   `-- _completed.json
    |
    |-- Camera01_0900-1000
    |   |-- frame_000001.jpg
    |   `-- _completed.json
    |
    `-- frame_extraction_report_YYYYMMDD_HHMMSS.csv

Each source video receives its own output folder.


11. PROCESSING REPORT
---------------------

The Command Prompt or Terminal shows a report after every video:

    [1/3] Processing: Camera01_0800-0900.mp4
    Status           : COMPLETED
    Extracted frames : 360
    Processing time  : 00:01:24
    Output folder    : D:\CCTV Frames\Camera01_0800-0900

At the end, the script shows a final summary for the entire batch.


12. CSV REPORT
--------------

A CSV report is saved in the main output folder.

The report includes:

- video_name
- status
- input_path
- output_path
- interval_seconds
- frame_count
- processing_seconds
- processing_time
- error

The CSV uses UTF-8 encoding and can be opened in Microsoft Excel.


13. COMPLETED VIDEO HANDLING
----------------------------

After a video is processed successfully, the script creates:

    _completed.json

When the script is run again with the same sampling interval, completed videos
are skipped automatically.

Use --overwrite to process them again.


14. EXPECTED FRAME COUNT
------------------------

For a one-hour video:

- One frame every 10 seconds: approximately 360 images
- One frame every 5 seconds: approximately 720 images
- One frame every 30 seconds: approximately 120 images

The exact number can vary slightly depending on the real video duration and
timestamp structure.


15. COMMON ERRORS
-----------------

Error: FFmpeg was not found

    Install FFmpeg and add it to PATH, or use:

    --ffmpeg "C:\ffmpeg\bin\ffmpeg.exe"

Error: Input path does not exist

    Check the input path.
    Put paths containing spaces inside quotation marks.

No supported videos were found

    Confirm that the folder contains one of the supported video formats.
    Use --recursive when the videos are inside subfolders.

Permission error

    Make sure the output folder is writable.
    Avoid protected system folders.


16. RECOMMENDED COMMAND
-----------------------

For the current sampling method of one frame every 10 seconds:

    python extract_frames_cli.py -i "YOUR_INPUT_PATH" -o "YOUR_OUTPUT_PATH" -t 10 --recursive
