"""
YouTube Subtitle Automation - CLI Entry Point

Usage:
    python main.py -i video.mp4
    python main.py -i video.mp4 -o output.mp4 --model medium --language hi --words 4
    python main.py --help
"""

import argparse
import os
import sys
from extract_and_transcribe_audio import extract_and_transcribe_audio
from add_subtitles_to_video import add_subtitles_to_video


SUPPORTED_FORMATS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"}


def parse_args():
    parser = argparse.ArgumentParser(
        prog="youtube-subtitle-automation",
        description=(
            "Automatically generate and burn subtitles into a video using "
            "OpenAI Whisper for transcription and FFmpeg for rendering."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -i video.mp4
  python main.py -i video.mp4 -o subtitled.mp4
  python main.py -i video.mp4 --model medium --language hi
  python main.py -i lecture.mp4 --words 6 --font-size 18 --font-color white
        """,
    )

    # --- Required ---
    parser.add_argument(
        "-i", "--input",
        required=True,
        metavar="INPUT_VIDEO",
        help="Path to the input video file (mp4, avi, mov, mkv, webm, flv).",
    )

    # --- Optional ---
    parser.add_argument(
        "-o", "--output",
        metavar="OUTPUT_VIDEO",
        default=None,
        help=(
            "Path for the output video with burned subtitles. "
            "Defaults to <input_name>_subtitled.mp4 in the same directory."
        ),
    )
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help=(
            "Whisper model size. Larger = more accurate but slower. "
            "Recommended: 'base' for speed, 'medium' for accuracy. (default: base)"
        ),
    )
    parser.add_argument(
        "--language",
        default=None,
        metavar="LANG_CODE",
        help=(
            "Language code for transcription, e.g. 'en', 'hi', 'es', 'fr'. "
            "If omitted, Whisper auto-detects the language."
        ),
    )
    parser.add_argument(
        "--words",
        type=int,
        default=4,
        metavar="N",
        help="Maximum number of words per subtitle chunk. (default: 4)",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=15,
        metavar="SIZE",
        help="Font size for subtitles. (default: 15)",
    )
    parser.add_argument(
        "--font-color",
        default="white",
        choices=["white", "yellow", "cyan", "green"],
        help="Subtitle text color. (default: white)",
    )
    parser.add_argument(
        "--margin-bottom",
        type=int,
        default=50,
        metavar="PX",
        help="Bottom margin for subtitle position in pixels. (default: 50)",
    )
    parser.add_argument(
        "--keep-srt",
        action="store_true",
        help="Keep the generated .srt file alongside the output video.",
    )

    return parser.parse_args()


def validate_input(input_path: str) -> None:
    """Validate that the input file exists and is a supported format."""
    if not os.path.exists(input_path):
        print(f"[ERROR] Input file not found: '{input_path}'")
        print("        Please check the path and try again.")
        sys.exit(1)

    if not os.path.isfile(input_path):
        print(f"[ERROR] '{input_path}' is a directory, not a file.")
        sys.exit(1)

    ext = os.path.splitext(input_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        print(f"[ERROR] Unsupported file format: '{ext}'")
        print(f"        Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}")
        sys.exit(1)


def check_ffmpeg() -> None:
    """Check that FFmpeg is available on PATH."""
    import shutil
    if shutil.which("ffmpeg") is None:
        print("[ERROR] FFmpeg is not installed or not found on your PATH.")
        print("        Install it and try again:")
        print("          Linux : sudo apt-get install ffmpeg")
        print("          macOS : brew install ffmpeg")
        print("          Windows: choco install ffmpeg  (or download from ffmpeg.org)")
        sys.exit(1)


def resolve_output_path(input_path: str, output_path: str | None) -> str:
    """Derive a sensible default output path if none was specified."""
    if output_path:
        return output_path
    base, _ = os.path.splitext(input_path)
    return f"{base}_subtitled.mp4"


def main():
    args = parse_args()

    # --- Validation ---
    validate_input(args.input)
    check_ffmpeg()

    output_path = resolve_output_path(args.input, args.output)

    # Warn if output would overwrite input
    if os.path.abspath(args.input) == os.path.abspath(output_path):
        print("[ERROR] Output path is the same as input path. Choose a different output name.")
        sys.exit(1)

    audio_path = output_path.rsplit(".", 1)[0] + "_temp_audio.wav"

    print(f"\n{'='*55}")
    print(f"  YouTube Subtitle Automation")
    print(f"{'='*55}")
    print(f"  Input    : {args.input}")
    print(f"  Output   : {output_path}")
    print(f"  Model    : {args.model}")
    print(f"  Language : {args.language or 'auto-detect'}")
    print(f"  Words/chunk: {args.words}")
    print(f"{'='*55}\n")

    try:
        # Step 1: Extract audio and transcribe
        print("[1/2] Extracting audio and transcribing with Whisper...")
        segments = extract_and_transcribe_audio(
            videopath=args.input,
            audio_path=audio_path,
            model_size=args.model,
            language=args.language,
        )
        print(f"      ✓ Transcription complete — {len(segments)} segment(s) found.")

        # Step 2: Burn subtitles into video
        print("[2/2] Burning subtitles into video with FFmpeg...")
        srt_path = add_subtitles_to_video(
            videopath=args.input,
            segments=segments,
            outputpath=output_path,
            max_words=args.words,
            font_size=args.font_size,
            font_color=args.font_color,
            margin_bottom=args.margin_bottom,
            keep_srt=args.keep_srt,
        )
        print(f"      ✓ Video saved to: {output_path}")

        if args.keep_srt and srt_path:
            print(f"      ✓ SRT file saved to: {srt_path}")

        print(f"\n  Done! 🎬\n")

    except KeyboardInterrupt:
        print("\n[ABORTED] Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred:\n  {e}")
        sys.exit(1)
    finally:
        # Always clean up the temp audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == "__main__":
    main()
