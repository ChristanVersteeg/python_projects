import os
import math
import subprocess
from pathlib import Path

# ====== CONFIG ======
TARGET_SIZE_MB = 10           # Max size per output file
AUDIO_BITRATE = 64_000        # 64 kbps audio (smaller than 128k to save space)
START_CRF = 24                # Initial CRF (lower = better quality, larger file)
CRF_STEP = 2                  # Increase CRF by this each attempt
MAX_CRF = 40                  # Max CRF we allow (40 is already quite compressed)
MAX_WIDTH = 1920              # Max output width
MAX_HEIGHT = 1080             # Max output height
MAX_FPS = 30                  # Cap FPS to 30 to save bits
# =====================

SCRIPT_DIR = Path(__file__).resolve().parent
FFMPEG_DIR = SCRIPT_DIR / "ffmpeg-8.0.1-full_build" / "bin"

# Make sure ffmpeg/ffprobe are found
os.environ["PATH"] = str(FFMPEG_DIR) + os.pathsep + os.environ.get("PATH", "")


def run_cmd(cmd):
    """Run a shell command and return (stdout, stderr). Raise on failure."""
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=True
        )
        return result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        raise RuntimeError(
            f"Command not found: {cmd[0]}. "
            f"Make sure ffmpeg/ffprobe exist in {FFMPEG_DIR}"
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n"
            f"stdout:\n{e.stdout}\n\nstderr:\n{e.stderr}"
        )


def get_resolution(path: Path):
    """Return (width, height) of the first video stream."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=s=x:p=0",
        str(path),
    ]
    out, _ = run_cmd(cmd)
    try:
        w_str, h_str = out.split("x")
        return int(w_str), int(h_str)
    except Exception:
        raise RuntimeError(f"Could not parse resolution from ffprobe output: {out!r}")


def calc_scaled_size(width, height):
    """
    Scale to fit inside MAX_WIDTH x MAX_HEIGHT while keeping aspect ratio.
    Return (new_width, new_height). If already small enough, returns original.
    """
    if width <= MAX_WIDTH and height <= MAX_HEIGHT:
        return width, height

    scale_factor = min(MAX_WIDTH / width, MAX_HEIGHT / height)
    new_w = int(2 * round((width * scale_factor) / 2))
    new_h = int(2 * round((height * scale_factor) / 2))
    return new_w, new_h


def compress_video(input_path: Path):
    """Compress a single MP4 to be as close as possible to TARGET_SIZE_MB."""
    print(f"\nProcessing: {input_path.name}")

    target_bytes = TARGET_SIZE_MB * 1024 * 1024
    current_size = input_path.stat().st_size

    if current_size <= target_bytes:
        print(f"  Already <= {TARGET_SIZE_MB} MB, skipping.")
        return

    # Figure out scaling
    width, height = get_resolution(input_path)
    new_w, new_h = calc_scaled_size(width, height)
    if (new_w, new_h) != (width, height):
        print(f"  Downscaling from {width}x{height} -> {new_w}x{new_h}")
        vf_filter = f"scale={new_w}:{new_h}"
    else:
        print(f"  Keeping resolution {width}x{height}")
        vf_filter = None

    stem = input_path.stem
    crf = START_CRF
    best_output = None
    best_size = None

    while crf <= MAX_CRF:
        tmp_output = input_path.with_name(f"{stem}_tmp_crf{crf}.mp4")
        if tmp_output.exists():
            tmp_output.unlink()

        print(f"  Encoding with CRF {crf}...")
        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", str(crf),
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", str(AUDIO_BITRATE),
            "-movflags", "+faststart",
            "-r", str(MAX_FPS),  # cap FPS
        ]
        if vf_filter is not None:
            cmd.extend(["-vf", vf_filter])

        cmd.append(str(tmp_output))
        run_cmd(cmd)

        size = tmp_output.stat().st_size
        mb_size = size / (1024 * 1024)
        print(f"    -> {mb_size:.2f} MB")

        if best_size is None or size < best_size:
            if best_output is not None and best_output.exists():
                best_output.unlink()
            best_output = tmp_output
            best_size = size
        else:
            tmp_output.unlink()

        if size <= target_bytes:
            break

        crf += CRF_STEP

    if best_output is None or not best_output.exists():
        print("  Failed to create a compressed file.")
        return

    final_output = input_path.with_name(f"{stem}_compressed_{TARGET_SIZE_MB}MB.mp4")
    if final_output.exists():
        final_output.unlink()
    best_output.rename(final_output)

    print(f"  Final file: {final_output.name} ({best_size / (1024 * 1024):.2f} MB)")


def main():
    mp4_files = sorted(SCRIPT_DIR.glob("*.mp4"))
    if not mp4_files:
        print("No .mp4 files found in the script directory.")
        return

    print(f"Found {len(mp4_files)} MP4 file(s) in {SCRIPT_DIR}")
    for mp4 in mp4_files:
        if mp4.name.endswith(f"_compressed_{TARGET_SIZE_MB}MB.mp4"):
            continue
        compress_video(mp4)


if __name__ == "__main__":
    main()
