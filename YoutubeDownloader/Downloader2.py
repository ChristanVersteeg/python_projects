import os
from pathlib import Path
import yt_dlp
from moviepy import VideoFileClip  # MoviePy 2.x style import

# === CONFIG ===
VIDEO_URL = "https://youtu.be/EA0Bx2OeDj8"
DOWNLOAD_DIR = "."      # current folder
TRIM_DURATION = 30      # seconds


def download_video(url: str, output_dir: str = ".") -> str:
    """
    Download the video via yt-dlp and return the path to the downloaded file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Output template: <dir>/<title>.<ext>
    outtmpl = str(output_dir / "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "format": "mp4/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "noplaylist": True,
        "quiet": False,   # set True if you want less console output
    }

    print("Downloading video with yt-dlp...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # yt-dlp gives us the filename:
        downloaded_path = ydl.prepare_filename(info)

    # Sometimes the extension can be something else; normalize to what exists.
    downloaded_file = Path(downloaded_path)
    if not downloaded_file.exists():
        # Try common extensions if the template got changed
        for ext in (".mp4", ".mkv", ".webm"):
            candidate = downloaded_file.with_suffix(ext)
            if candidate.exists():
                downloaded_file = candidate
                break

    print(f"Downloaded file: {downloaded_file}")
    return str(downloaded_file)


def trim_first_n_seconds(input_path: str, seconds: int = 30,
                         output_path: str | None = None) -> str:
    """
    Trim the video to the first `seconds` seconds and save.
    Returns the output file path.
    """
    input_path = Path(input_path)

    if output_path is None:
        base, ext = os.path.splitext(str(input_path))
        output_path = f"{base}_first{seconds}s{ext}"

    print(f"Trimming first {seconds} seconds...")

    # MoviePy 2.x usage
    with VideoFileClip(str(input_path)) as clip:
        end_time = min(seconds, clip.duration)
        trimmed = clip.subclipped(0, end_time)
        trimmed.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
        )

    print(f"Trimmed video saved as: {output_path}")
    return output_path


if __name__ == "__main__":
    try:
        downloaded_file = download_video(VIDEO_URL, DOWNLOAD_DIR)
        trimmed_file = trim_first_n_seconds(downloaded_file, TRIM_DURATION)
        print("All done!")
    except Exception as e:
        print(f"Error: {e}")
