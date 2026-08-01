from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".m4v",
    ".wmv",
    ".flv",
    ".ts",
    ".mts",
    ".m2ts",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract frames from one video or all videos in a folder "
            "and save the results to an output folder."
        )
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=Path,
        help="Input video file or folder containing videos.",
    )

    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="Output folder used to save extracted frames.",
    )

    parser.add_argument(
        "-t",
        "--interval",
        type=float,
        default=10.0,
        help="Extract one frame every N seconds. Default: 10.",
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search for videos inside all input subfolders.",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Process videos again even if they were completed previously.",
    )

    parser.add_argument(
        "--ffmpeg",
        type=Path,
        default=None,
        help=(
            "Optional path to ffmpeg.exe. "
            "This is not required when FFmpeg is available in PATH."
        ),
    )

    return parser.parse_args()


def format_duration(seconds: float) -> str:
    total_seconds = int(round(seconds))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def resolve_ffmpeg(ffmpeg_argument: Path | None) -> str:
    if ffmpeg_argument is not None:
        ffmpeg_path = ffmpeg_argument.expanduser().resolve()

        if not ffmpeg_path.is_file():
            raise FileNotFoundError(
                f"FFmpeg was not found at:\n{ffmpeg_path}"
            )

        return str(ffmpeg_path)

    ffmpeg_in_path = shutil.which("ffmpeg")

    if ffmpeg_in_path is None:
        raise FileNotFoundError(
            "FFmpeg was not found.\n"
            "Install FFmpeg and make sure the 'ffmpeg' command is available "
            "in CMD, or provide the full path with --ffmpeg."
        )

    return ffmpeg_in_path


def find_videos(input_path: Path, recursive: bool) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
            raise ValueError(
                f"Unsupported video format: {input_path.suffix}"
            )

        return [input_path]

    if not input_path.is_dir():
        raise FileNotFoundError(
            f"Input path does not exist:\n{input_path}"
        )

    file_iterator = (
        input_path.rglob("*")
        if recursive
        else input_path.glob("*")
    )

    videos = [
        path
        for path in file_iterator
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS
    ]

    return sorted(videos)


def get_video_output_folder(
    video_path: Path,
    input_path: Path,
    output_root: Path,
) -> Path:
    if input_path.is_file():
        return output_root / video_path.stem

    relative_parent = video_path.parent.relative_to(input_path)
    return output_root / relative_parent / video_path.stem


def clear_previous_result(output_folder: Path) -> None:
    for image_path in output_folder.glob("frame_*.jpg"):
        image_path.unlink()

    completed_marker = output_folder / "_completed.json"

    if completed_marker.exists():
        completed_marker.unlink()


def read_completed_result(
    completed_marker: Path,
    interval_seconds: float,
) -> int | None:
    if not completed_marker.exists():
        return None

    try:
        data = json.loads(
            completed_marker.read_text(encoding="utf-8")
        )

        saved_interval = float(data["interval_seconds"])
        frame_count = int(data["frame_count"])

        if abs(saved_interval - interval_seconds) < 0.000001:
            return frame_count

    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
    ):
        return None

    return None


def extract_frames_from_video(
    video_path: Path,
    input_path: Path,
    output_root: Path,
    interval_seconds: float,
    ffmpeg_path: str,
    overwrite: bool,
) -> dict[str, object]:
    output_folder = get_video_output_folder(
        video_path=video_path,
        input_path=input_path,
        output_root=output_root,
    )

    output_folder.mkdir(parents=True, exist_ok=True)
    completed_marker = output_folder / "_completed.json"

    if not overwrite:
        completed_frame_count = read_completed_result(
            completed_marker=completed_marker,
            interval_seconds=interval_seconds,
        )

        if completed_frame_count is not None:
            return {
                "video_name": video_path.name,
                "status": "SKIPPED",
                "input_path": str(video_path),
                "output_path": str(output_folder),
                "interval_seconds": interval_seconds,
                "frame_count": completed_frame_count,
                "processing_seconds": 0.0,
                "processing_time": "00:00:00",
                "error": "",
            }

    clear_previous_result(output_folder)
    output_pattern = output_folder / "frame_%06d.jpg"

    ffmpeg_command = [
        ffmpeg_path,
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(video_path),
        "-vf",
        f"fps=fps=1/{interval_seconds}:start_time=0",
        "-q:v",
        "2",
        str(output_pattern),
    ]

    start_time = time.perf_counter()

    try:
        subprocess.run(
            ffmpeg_command,
            check=True,
            capture_output=True,
            text=True,
        )

        processing_seconds = time.perf_counter() - start_time
        extracted_images = sorted(output_folder.glob("frame_*.jpg"))
        frame_count = len(extracted_images)

        completed_data = {
            "source_video": str(video_path.resolve()),
            "output_folder": str(output_folder.resolve()),
            "interval_seconds": interval_seconds,
            "frame_count": frame_count,
            "processing_seconds": round(processing_seconds, 3),
            "processing_time": format_duration(processing_seconds),
            "completed_at": datetime.now().isoformat(timespec="seconds"),
        }

        completed_marker.write_text(
            json.dumps(
                completed_data,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        return {
            "video_name": video_path.name,
            "status": "COMPLETED",
            "input_path": str(video_path),
            "output_path": str(output_folder),
            "interval_seconds": interval_seconds,
            "frame_count": frame_count,
            "processing_seconds": round(processing_seconds, 3),
            "processing_time": format_duration(processing_seconds),
            "error": "",
        }

    except subprocess.CalledProcessError as error:
        processing_seconds = time.perf_counter() - start_time

        error_message = (
            error.stderr.strip()
            if error.stderr
            else str(error)
        )

        return {
            "video_name": video_path.name,
            "status": "FAILED",
            "input_path": str(video_path),
            "output_path": str(output_folder),
            "interval_seconds": interval_seconds,
            "frame_count": 0,
            "processing_seconds": round(processing_seconds, 3),
            "processing_time": format_duration(processing_seconds),
            "error": error_message,
        }


def save_csv_report(
    results: list[dict[str, object]],
    output_root: Path,
) -> Path:
    report_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = (
        output_root
        / f"frame_extraction_report_{report_timestamp}.csv"
    )

    fieldnames = [
        "video_name",
        "status",
        "input_path",
        "output_path",
        "interval_seconds",
        "frame_count",
        "processing_seconds",
        "processing_time",
        "error",
    ]

    with report_path.open(
        mode="w",
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(results)

    return report_path


def main() -> int:
    arguments = parse_arguments()

    input_path = arguments.input.expanduser().resolve()
    output_root = arguments.output.expanduser().resolve()

    if arguments.interval <= 0:
        print(
            "Error: --interval must be greater than 0.",
            file=sys.stderr,
        )
        return 1

    try:
        ffmpeg_path = resolve_ffmpeg(arguments.ffmpeg)

        videos = find_videos(
            input_path=input_path,
            recursive=arguments.recursive,
        )

    except (FileNotFoundError, ValueError) as error:
        print(f"\nError:\n{error}", file=sys.stderr)
        return 1

    if not videos:
        print(
            f"No supported videos were found in:\n{input_path}"
        )
        return 0

    output_root.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("BATCH FRAME EXTRACTION")
    print("=" * 72)
    print(f"Input path       : {input_path}")
    print(f"Output path      : {output_root}")
    print(f"Sampling interval: {arguments.interval} seconds")
    print(f"Videos found     : {len(videos)}")
    print(f"FFmpeg           : {ffmpeg_path}")
    print("=" * 72)

    batch_start_time = time.perf_counter()
    results: list[dict[str, object]] = []

    for video_index, video_path in enumerate(videos, start=1):
        print(
            f"\n[{video_index}/{len(videos)}] "
            f"Processing: {video_path.name}"
        )

        result = extract_frames_from_video(
            video_path=video_path,
            input_path=input_path,
            output_root=output_root,
            interval_seconds=arguments.interval,
            ffmpeg_path=ffmpeg_path,
            overwrite=arguments.overwrite,
        )

        results.append(result)

        print(f"Status           : {result['status']}")
        print(f"Extracted frames : {result['frame_count']}")
        print(f"Processing time  : {result['processing_time']}")
        print(f"Output folder    : {result['output_path']}")

        if result["error"]:
            print(f"Error            : {result['error']}")

    total_batch_seconds = time.perf_counter() - batch_start_time

    completed_results = [
        result
        for result in results
        if result["status"] == "COMPLETED"
    ]

    skipped_results = [
        result
        for result in results
        if result["status"] == "SKIPPED"
    ]

    failed_results = [
        result
        for result in results
        if result["status"] == "FAILED"
    ]

    newly_extracted_frames = sum(
        int(result["frame_count"])
        for result in completed_results
    )

    skipped_existing_frames = sum(
        int(result["frame_count"])
        for result in skipped_results
    )

    report_path = save_csv_report(
        results=results,
        output_root=output_root,
    )

    print("\n" + "=" * 72)
    print("FINAL REPORT")
    print("=" * 72)
    print(f"Completed videos       : {len(completed_results)}")
    print(f"Skipped videos         : {len(skipped_results)}")
    print(f"Failed videos          : {len(failed_results)}")
    print(f"New frames extracted   : {newly_extracted_frames}")
    print(f"Existing skipped frames: {skipped_existing_frames}")
    print(f"Total processing time  : {format_duration(total_batch_seconds)}")
    print(f"CSV report             : {report_path}")
    print("=" * 72)

    return 1 if failed_results else 0


if __name__ == "__main__":
    raise SystemExit(main())
