from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess

def download_video(url, output_path, format="mp4"):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"Downloading: {yt.title}")
        
        if format == "mp4":
            stream = yt.streams.get_highest_resolution()
            downloaded_path = stream.download(output_path=f"{output_path}/mp4")
            print(f"Video downloaded to: {downloaded_path}")
        elif format == "mp3":
            stream = yt.streams.get_audio_only()
            downloaded_path = stream.download(output_path=f"{output_path}/mp3")
            # Convert to mp3 using ffmpeg
            base, ext = os.path.splitext(downloaded_path)
            mp3_path = base + ".mp3"
            try:
                # Use ffmpeg to convert the audio file to mp3
                subprocess.run(['ffmpeg', '-i', downloaded_path, '-codec:a', 'libmp3lame', '-q:a', '2', mp3_path], check=True)
                # Remove the original file after successful conversion
                os.remove(downloaded_path)
                print(f"Audio downloaded and converted to: {mp3_path}")
                downloaded_path = mp3_path
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                print(f"Error converting to MP3: {e}")
                print("Make sure ffmpeg is installed on your system")
                return downloaded_path
        return downloaded_path
    except Exception as e:
        print(f"Error downloading: {e}")
        return None
if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    format_choice = input("Enter format (mp4/mp3): ").lower()
    if format_choice == "":
        format_choice = "mp4"
    while format_choice not in ["mp4", "mp3"]:
        format_choice = input("Invalid choice. Enter format (mp4/mp3): ").lower()
    
    download_video(url, "video-element", format=format_choice)
    