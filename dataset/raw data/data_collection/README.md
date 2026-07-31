# SmartPSS Playback Batch Export

A Windows automation workflow for exporting SmartPSS Playback recordings from an Excel task list.

This project was created for SmartPSS environments where recordings are accessed through P2P-connected devices and the installed SmartPSS version does not provide a practical batch export API, command-line interface, or stable programmatic export interface. The normal workflow therefore requires repeated manual interaction with the SmartPSS user interface.

The Python script reproduces that manual workflow through calibrated screen coordinates, processes one Excel row at a time, waits for each MP4 export to complete, records the result, and continues to the next task.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Why This Automation Is Necessary](#2-why-this-automation-is-necessary)
3. [Environment and Constraints](#3-environment-and-constraints)
4. [Original Manual Workflow](#4-original-manual-workflow)
5. [How the Manual Workflow Was Converted to Python](#5-how-the-manual-workflow-was-converted-to-python)
6. [Project Files](#6-project-files)
7. [Excel Input Structure](#7-excel-input-structure)
8. [How the Script Selects a Camera](#8-how-the-script-selects-a-camera)
9. [Output File Naming](#9-output-file-naming)
10. [Installation](#10-installation)
11. [Initial SmartPSS Preparation](#11-initial-smartpss-preparation)
12. [Coordinate Calibration](#12-coordinate-calibration)
13. [Fixed Download Folder Configuration](#13-fixed-download-folder-configuration)
14. [Excel Validation](#14-excel-validation)
15. [Recommended Test Procedure](#15-recommended-test-procedure)
16. [Running the Full Batch](#16-running-the-full-batch)
17. [Resuming After an Interruption](#17-resuming-after-an-interruption)
18. [Download Completion Detection](#18-download-completion-detection)
19. [Emergency Stop](#19-emergency-stop)
20. [Important Operational Rules](#20-important-operational-rules)
21. [Known Limitations](#21-known-limitations)
22. [Troubleshooting](#22-troubleshooting)
23. [Example End-to-End Workflow](#23-example-end-to-end-workflow)

---

## 1. Project Overview

The project automates the export of video recordings from the SmartPSS Playback screen.

Each Excel row defines one recording request:

- Device Name
- Channel
- Camera Name
- Start Time
- End Time

The script performs the required SmartPSS user-interface actions, downloads the video as MP4, verifies that the file is complete, renames it, updates the result workbook, closes the download window, and continues to the next row.

The automation is designed for long batch jobs where manually exporting each recording would require repeated clicking, time entry, waiting, checking, and file management.

---

## 2. Why This Automation Is Necessary

The workflow is automated through the graphical user interface because of the characteristics of the installed SmartPSS environment.

### 2.1 SmartPSS version limitations

The target environment uses a SmartPSS 2.x installation. In this environment, Playback export is exposed primarily as an interactive desktop workflow.

The application does not provide a documented and practical batch export interface for this use case. There is no normal command such as:

```text
export device X, channel Y, from time A to time B
```

that can be called directly from Python.

As a result, the export process must be performed through the same controls that a human operator uses.

### 2.2 P2P-connected devices

The cameras are accessed through P2P device connections rather than through a locally managed NVR workflow with an accessible recording API.

The recordings are therefore retrieved through SmartPSS Playback. The Python script cannot simply read files from a local recording folder or query an NVR file system.

### 2.3 Repetitive manual work

For every requested recording, a human operator would normally need to:

1. Search for the device.
2. Expand the device.
3. Select the correct channel.
4. Configure playback filters.
5. Enter the requested start and end time.
6. Search for the recording.
7. Start playback.
8. Mark the export interval.
9. Select MP4.
10. Confirm the export.
11. Wait for the download.
12. Check that the file has completed.
13. Close the download window.
14. Repeat the same process for the next recording.

When many recordings are required, this process becomes slow, repetitive, and vulnerable to operator error.

### 2.4 Why coordinate-based automation is used

SmartPSS does not expose stable control identifiers that the project can reliably access through a public automation API.

For this reason, the script uses calibrated screen coordinates through `PyAutoGUI`.

This approach is less flexible than a direct application API, but it reproduces the manual workflow consistently when:

- the SmartPSS window remains in the same position;
- the resolution remains unchanged;
- Windows Display Scaling remains unchanged;
- the list of channels appears in the same layout;
- the operator does not use the mouse or keyboard during execution.

---

## 3. Environment and Constraints

The automation was designed around the following operating assumptions:

- Windows operating system
- SmartPSS opened on the Playback screen
- P2P-connected devices
- Up to 13 channel positions
- MP4 export format
- One fixed SmartPSS Playback Export folder
- Excel-based task list
- Python controlling the interface through PyAutoGUI

The script is not a SmartPSS plugin and does not modify SmartPSS internally.

It acts as an automated operator.

### Required screen stability

After calibration, the following must remain unchanged:

- monitor arrangement;
- primary display;
- screen resolution;
- Windows Display Scaling;
- SmartPSS window size;
- SmartPSS window position;
- Playback panel layout;
- channel-row spacing.

Changing these settings can make saved coordinates point to the wrong controls.

---

## 4. Original Manual Workflow

Before automation, each video is exported manually through the following sequence.

### Step 1: Search for the device

The operator clicks the device search field, removes the previous value, enters the required device name, and presses the device search icon.

### Step 2: Expand the device

After the device appears, the operator clicks the expand arrow to display its channels.

### Step 3: Select the channel

The operator selects the required channel from the visible channel list.

The automation identifies the channel by its position from 1 to 13.

### Step 4: Configure Playback filters

The required settings are selected:

```text
Record
All Records
Main Stream
```

### Step 5: Enter the time range

The operator opens the Time window and enters:

```text
Start Time
End Time
```

SmartPSS receives the values in this format:

```text
yyyy-mm-dd hh:mm:ss
```

Example:

```text
2026-07-20 07:30:00
```

### Step 6: Search for the recording

The operator clicks the Playback Search button.

Only one Search click should be sent. A second click can cancel or replace the current search result.

### Step 7: Start playback

The operator clicks Play and waits briefly so that SmartPSS loads the selected recording.

### Step 8: Open Export Setup

The scissors icon is clicked twice, with a short interval between clicks, to define the export range and open the Export Setup window.

### Step 9: Select MP4

The Playback Export folder is already configured in SmartPSS.

The operator only selects:

```text
MP4
```

and confirms the Export Setup dialog.

### Step 10: Confirm the export prompt

The final confirmation prompt is accepted.

### Step 11: Wait for the download

SmartPSS downloads the recording into the fixed Playback Export folder.

The operator normally has to wait until the file is no longer growing and the export has completed.

### Step 12: Close the download window

The download or export-progress window is closed once.

The next recording can then be processed.

---

## 5. How the Manual Workflow Was Converted to Python

The script maps each manual action to a controlled PyAutoGUI action.

| Manual action | Python automation |
|---|---|
| Click the device search field | Calibrated `device_search_input` coordinate |
| Clear the previous device | Explicit `Ctrl+A` and text replacement |
| Enter the device name | Clipboard-based text entry |
| Press device search | Single calibrated click |
| Expand device | Calibrated expand-arrow click |
| Select channel | One of 13 independently calibrated positions |
| Select Record | Dropdown and option coordinates |
| Select All Records | Dropdown and option coordinates |
| Select Main Stream | Dropdown and option coordinates |
| Enter start and end times | Atomic clipboard paste using `yyyy-mm-dd hh:mm:ss` |
| Press Playback Search | Exactly one click |
| Press Play | Calibrated Play coordinate |
| Click scissors twice | Two controlled clicks with a delay |
| Select MP4 | Format dropdown and MP4 coordinates |
| Confirm export | Export and prompt coordinates |
| Detect completed download | File-system monitoring |
| Rename output | Python file operation |
| Close download window | Exactly one click |
| Continue to next task | Excel status and loop control |

### Why the time values are pasted atomically

SmartPSS time fields can behave like masked input controls.

Typing the value character by character can shift the minute and second positions. For example, a value intended as:

```text
2026-07-20 07:30:00
```

could be interpreted incorrectly if entered one character at a time.

The script therefore converts the Excel value and pastes the full date-time string at once.

### Why Playback Search is clicked exactly once

During testing, a second Search click was found to cancel or replace the newly loaded search result.

That can cause the export step to reuse the recording from the previous Excel row.

The script explicitly sends one Search click only.

### Why the download window is clicked only once

A second close click can pass through after the modal window disappears and activate a control underneath, including the Playback Search button.

The current script therefore sends one physical click to close the completed download window.

---

## 6. Project Files

This repository contains three main files:

```text
smartpss_playback_export_ai.py
smartpss_export_tasks.xlsx
README.md
```

### `smartpss_playback_export.py`

The Python automation script.

It contains:

- coordinate calibration;
- Excel validation;
- SmartPSS UI control;
- file-completion monitoring;
- output renaming;
- status workbook management;
- interruption recovery.

### `smartpss_export_tasks.xlsx`

The English Excel task template.

The first six columns are user input. The remaining columns are maintained by the script.

### `README.md`

Project explanation, design rationale, manual process, automation mapping, setup instructions, operating procedures, and troubleshooting.

### Local configuration file

The script creates or uses a local configuration file:

```text
smartpss_export_config.json
```

This file is not one of the three main repository files because it is machine-specific.

It contains:

- local screen coordinates;
- the fixed download folder;
- timing values.

Each machine should generate its own configuration through calibration.

---

## 7. Excel Input Structure

The `Task_List` worksheet contains the following columns.

| Column | Entered by | Description |
|---|---|---|
| Task ID | User | Unique task identifier |
| Device Name | User | Exact device name shown in SmartPSS |
| Channel | User | Channel position from 1 to 13 |
| Camera Name | User | Descriptive label used in the output filename |
| Start Time | User | Beginning of the requested recording |
| End Time | User | End of the requested recording |
| Status | Script | Task state |
| Output File | Script | Final MP4 path |
| Processing Started | Script | Start timestamp |
| Processing Finished | Script | Completion timestamp |
| Elapsed Time | Script | Total task duration |
| Notes | Script | Completion or error details |

Recommended time display:

```text
yyyy-mm-dd hh:mm:ss
```

The Excel cell should contain a real Excel date-time value rather than plain descriptive text.

### Status values

The script uses:

```text
IN PROGRESS
COMPLETED
ERROR
```

---

## 8. How the Script Selects a Camera

The script selects a camera using:

```text
Device Name + Channel
```

`Camera Name` is not used to identify or verify the channel in SmartPSS.

For example:

| Device Name | Channel | Camera Name |
|---|---:|---|
| STORE_A | 4 | Checkout |

The script performs:

```text
Search STORE_A
Expand STORE_A
Click calibrated Channel 4 position
```

`Checkout` is used only as a descriptive label and as part of the output filename.

This means the user must ensure that the Channel value correctly represents the required camera position.

---

## 9. Output File Naming

Completed MP4 files are renamed using:

```text
TaskID_DeviceName_CHxx_CameraName_StartTime-EndTime.mp4
```

Example:

```text
1_STORE_A_CH04_CHECKOUT_20260720_073000-20260720_083000.mp4
```

Invalid filename characters are sanitized automatically.

---

## 10. Installation

Install Python 3.10 or newer.

Install the required packages:

```powershell
py -m pip install openpyxl pyautogui pyperclip
```

The script can then be tested with:

```powershell
py smartpss_playback_export.py --help
```

---

## 11. Initial SmartPSS Preparation

Before calibration:

1. Open SmartPSS.
2. Open the Playback screen.
3. Maximize the window or place it in the exact position that will be used during automation.
4. Confirm that the device search panel is visible.
5. Confirm that the channel list appears in a consistent vertical order.
6. Confirm that Playback filters are visible.
7. Confirm that the Time control is accessible.
8. Confirm that the Search, Play, and scissors controls are visible.
9. Perform one manual export to confirm that MP4 export works.
10. Choose and retain one Playback Export folder.

Do not change the SmartPSS window geometry after calibration.

---

## 12. Coordinate Calibration

Run:

```powershell
py smartpss_playback_export.py --calibrate
```

The script guides the operator through capturing:

- device search input;
- device search button;
- device expand arrow;
- Channel 1 through Channel 13;
- Playback filter controls;
- Time window fields;
- Playback Search;
- Play;
- scissors;
- MP4 format selection;
- confirmation buttons;
- download-window close button.

The calibration creates:

```text
smartpss_export_config.json
```

### Calibrating only the close button

When only the download-window close coordinate changes:

```powershell
py smartpss_playback_export.py --calibrate-close-button
```

This does not recalibrate the 13 channel positions.

---

## 13. Fixed Download Folder Configuration

SmartPSS Playback Export and Python must use the same folder.

Example:

```text
D:\SmartPSS_Exports\DownLoad
```

Store the folder in the local configuration:

```powershell
py smartpss_playback_export.py --set-download-dir "D:\SmartPSS_Exports\DownLoad"
```

This command updates:

```text
smartpss_export_config.json
```

The folder must already exist.

The script does not change the SmartPSS export path through the UI. The operator must ensure manually that SmartPSS Playback Export is using the same location.

---

## 14. Excel Validation

Before controlling SmartPSS, validate the task workbook:

```powershell
py smartpss_playback_export.py ^
  --excel smartpss_export_tasks.xlsx ^
  --validate
```

Validation checks include:

- required columns;
- Device Name;
- Camera Name;
- Channel range;
- valid start time;
- valid end time;
- End Time later than Start Time.

No SmartPSS clicks are performed during validation.

---

## 15. Recommended Test Procedure

Do not begin with a full batch.

Create two tasks with clearly different:

- channels; or
- time ranges.

Run:

```powershell
py smartpss_playback_export.py ^
  --excel smartpss_export_tasks.xlsx ^
  --max-tasks 2 ^
  --force
```

Using two rows is important.

A one-row test confirms that one export can complete. A two-row test also confirms that:

- the second device search starts correctly;
- the second Playback Search is not cancelled;
- the second export does not reuse the first task's recording;
- the download window closes correctly;
- the automation returns to the correct starting state.

---

## 16. Running the Full Batch

Run:

```powershell
py smartpss_playback_export.py ^
  --excel smartpss_export_tasks.xlsx ^
  --continue-on-error
```

The script creates a result workbook:

```text
smartpss_export_tasks_result.xlsx
```

The result workbook stores processing progress and should be used for future continuation.

---

## 17. Resuming After an Interruption

Interruptions may occur because of:

- manual cancellation;
- network issues;
- SmartPSS playback failure;
- device unavailability;
- computer restart;
- operator pause;
- PyAutoGUI fail-safe;
- Terminal closure.

To continue, use the result workbook:

```powershell
py smartpss_playback_export.py ^
  --excel smartpss_export_tasks_result.xlsx ^
  --retry-errors ^
  --continue-on-error
```

Do not return to the original blank template after progress has been recorded.

### Resume behavior

| Status | Default behavior |
|---|---|
| COMPLETED | Skipped when the output file still exists |
| ERROR | Retried only with `--retry-errors` |
| IN PROGRESS | Processed again because completion was not confirmed |
| Blank | Processed normally |

Do not add `--force` unless completed tasks should be exported again.

---

## 18. Download Completion Detection

The presence of an MP4 file alone does not prove that the download has finished.

SmartPSS may create the file before all video data has been written.

The script therefore:

1. records the MP4 files that already exist before export;
2. starts the SmartPSS export;
3. scans the fixed folder recursively;
4. detects `.mp4` and `.MP4`;
5. identifies a new or changed file;
6. checks its size and modification time repeatedly;
7. waits until the file remains stable;
8. checks that SmartPSS has released the file handle;
9. renames the file;
10. closes the download window;
11. begins the next Excel task.

This prevents the next task from starting while the previous file is incomplete.

---

## 19. Emergency Stop

PyAutoGUI fail-safe is enabled.

To stop the automation:

1. Move the pointer to the absolute top-left corner of the primary screen.
2. Keep it there until the script performs its next PyAutoGUI action.
3. PyAutoGUI raises a fail-safe exception and stops.

The target position is approximately:

```text
X = 0
Y = 0
```

This means the corner of the full screen, not the corner of the SmartPSS window.

An alternative is:

1. Switch to Terminal.
2. Press:

```text
Ctrl+C
```

---

## 20. Important Operational Rules

During execution:

- Do not use the mouse.
- Do not use the keyboard.
- Do not resize SmartPSS.
- Do not move the SmartPSS window.
- Do not change Windows Display Scaling.
- Do not change the screen resolution.
- Do not lock Windows.
- Do not allow the computer to sleep.
- Keep SmartPSS and Python running at the same privilege level.
- Close the Excel workbook before starting the script.

### Administrator privilege

If SmartPSS is running as Administrator but Python is not, Windows may allow mouse movement while blocking clicks or keyboard input.

Run both applications at the same privilege level.

---

## 21. Known Limitations

This project has the following limitations.

### Coordinate dependence

The script uses fixed coordinates. It does not locate controls semantically.

### Channel position dependence

The script assumes Channel 1-13 remain in the calibrated positions.

If SmartPSS:

- hides offline channels;
- reorders channels;
- changes row spacing;
- scrolls the list;
- displays fewer rows;

the selected coordinate may no longer represent the intended channel.

### No visual verification of camera name

The script does not read the channel label from SmartPSS.

The Excel `Camera Name` is descriptive only.

### No SmartPSS API validation

The script does not receive a structured confirmation from SmartPSS that the requested device, channel, and time range are correct.

Accuracy depends on stable UI behavior and correct calibration.

### One active desktop

The SmartPSS window must remain visible on the active Windows desktop.

The machine cannot be locked or switched to a disconnected session while UI automation is running.

---

## 22. Troubleshooting

### Mouse moves but clicks do not work

Cause:

- SmartPSS and Python are running at different privilege levels.

Resolution:

- close both;
- reopen both normally; or
- run both as Administrator.

### The wrong channel is selected

Cause:

- the channel layout moved;
- the device has a different number of visible channels;
- the SmartPSS window size changed;
- display scaling changed.

Resolution:

- restore the calibrated layout;
- recalibrate all coordinates.

### The second task exports the first task's video

Cause:

- Playback Search was activated twice;
- a second close-window click passed through to Search;
- SmartPSS did not load the new search result.

Resolution:

- use the current script;
- confirm that Terminal reports one Search click;
- test two clearly different rows.

### The MP4 appears but the script is still waiting

The file may still be growing or locked by SmartPSS.

Review the Terminal status:

```text
stable 10/20s
writing/file locked
```

The script continues only after the file is stable and released.

### The download window does not close

Recalibrate only the close button:

```powershell
py smartpss_playback_export.py --calibrate-close-button
```

### The script monitors the wrong folder

Update the configuration:

```powershell
py smartpss_playback_export.py ^
  --set-download-dir "D:\SmartPSS_Exports\DownLoad"
```

Confirm that SmartPSS Playback Export uses the same folder.

### The Excel file cannot be saved

Close the workbook in Excel before running Python.

---

## 23. Example End-to-End Workflow

### Prepare tasks

Open:

```text
smartpss_export_tasks.xlsx
```

Enter two test rows.

Example:

| Task ID | Device Name | Channel | Camera Name | Start Time | End Time |
|---:|---|---:|---|---|---|
| 1 | STORE_A | 1 | Entrance | 2026-07-20 07:30:00 | 2026-07-20 08:30:00 |
| 2 | STORE_A | 4 | Checkout | 2026-07-20 09:00:00 | 2026-07-20 10:00:00 |

Close Excel.

### Validate

```powershell
py smartpss_playback_export.py ^
  --excel smartpss_export_tasks.xlsx ^
  --validate
```

### Test

```powershell
py smartpss_playback_export.py ^
  --excel smartpss_export_tasks.xlsx ^
  --max-tasks 2 ^
  --force
```

### Review

Check:

- the first and second videos are different;
- the channels are correct;
- the time ranges are correct;
- both MP4 files are complete;
- the result workbook contains `COMPLETED`;
- the Output File column contains valid paths.

### Run the full workload

```powershell
py smartpss_playback_export.py ^
  --excel smartpss_export_tasks.xlsx ^
  --continue-on-error
```

### Continue later

```powershell
py smartpss_playback_export.py ^
  --excel smartpss_export_tasks_result.xlsx ^
  --retry-errors ^
  --continue-on-error
```

---

## Final Notes

This project does not replace SmartPSS or bypass its recording controls.

It automates an existing manual Playback export workflow so that a large number of recording requests can be processed consistently from Excel.

The reliability of the process depends on:

- correct Excel data;
- correct coordinate calibration;
- stable SmartPSS layout;
- consistent channel positions;
- matching download-folder configuration;
- uninterrupted Windows desktop access.
