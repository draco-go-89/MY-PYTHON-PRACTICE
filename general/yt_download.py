import os
from importlib import import_module

try:
    YoutubeDL = import_module("yt_dlp").YoutubeDL
except ModuleNotFoundError as error:
    raise SystemExit(
        "yt-dlp is not installed. Install it with: python -m pip install yt-dlp"
    ) from error

def download_youtube_media():
    # 1. Get the YouTube URL from the user
    url = input("Enter the YouTube video URL: ").strip()
    if not url:
        print("URL cannot be empty.")
        return

    # 2. Ask the user for the preferred format
    print("\nChoose download type:")
    print("1. Audio Only (MP3)")
    choice = input("Enter 1: ").strip()

    # 3. Configure download options based on choice
    if choice == '1':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{  # Extracts audio and converts it to MP3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        print("\n⏳ Extracting and downloading audio... (Please wait)")
    else:
        print("Invalid choice. Exiting.")
        return

    # 4. Execute the download
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\nDownload completed successfully! The file is saved in your current folder.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    download_youtube_media()
