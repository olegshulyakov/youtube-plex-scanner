import os
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound

PLEX_URL = 'http://localhost:32400'  # Update with your Plex server URL
PLEX_TOKEN = 'your_plex_token'      # Update with your Plex API token

plex = PlexServer(PLEX_URL, PLEX_TOKEN)

def scan_youtube_videos(base_path):
    for artist in os.listdir(base_path):
        artist_path = os.path.join(base_path, artist)
        if os.path.isdir(artist_path):
            for playlist in os.listdir(artist_path):
                playlist_path = os.path.join(artist_path, playlist)
                if os.path.isdir(playlist_path):
                    for video_file in os.listdir(playlist_path):
                        video_path = os.path.join(playlist_path, video_file)
                        if os.path.isfile(video_path) and video_path.endswith('.mp4'):
                            title = os.path.splitext(video_file)[0]
                            add_video_to_plex(video_path, title, artist, playlist)

def add_video_to_plex(file_path, title, artist, playlist):
    library = plex.library.section('Videos')
    if not library:
        print("No 'Videos' library found.")
        return

    try:
        video = library.search(title=title)[0]
        print(f"Video '{title}' already exists in Plex.")
    except NotFound:
        # Create a new folder structure
        artist_folder, playlist_folder = create_folder_structure(library, artist, playlist)
        # Add the video to the new folder
        artist_folder.addItems([file_path])
        print(f"Added video '{title}' to {artist} -> {playlist}")

def create_folder_structure(library, artist, playlist):
    root_section = library.search(title=artist)[0] if library.search(title=artist) else library.createFolder(artist)
    playlist_section = root_section.search(title=playlist)[0] if root_section.search(title=playlist) else root_section.createFolder(playlist)
    return root_section, playlist_section

if __name__ == "__main__":
    base_path = '/path/to/your/videos'  # Update with your base path
    scan_youtube_videos(base_path)
