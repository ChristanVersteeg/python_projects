import pytube
import moviepy.editor as mp
import os

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLx7ZmhAvBjqizeG4FbI4htLZrwYPtVYgp"

# Create a playlist object
playlist = pytube.Playlist(PLAYLIST_URL)

# Directory to temporarily save downloaded videos
download_dir = "./downloads"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Iterate over all videos in the playlist
for index, video_url in enumerate(playlist.video_urls):
    yt = pytube.YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    
    # Download audio stream to the specified directory
    downloaded_file = stream.download(output_path=download_dir)
    
    # Convert to ogg
    output_file = os.path.join(download_dir, f"{yt.title}.ogg")
    clip = mp.AudioFileClip(downloaded_file)
    clip.write_audiofile(output_file)
    clip.close()
    
    # Remove original downloaded file
    os.remove(downloaded_file)
    print(f"Processed {index + 1}/{len(playlist.video_urls)}: {yt.title}")

print("All videos processed!")
