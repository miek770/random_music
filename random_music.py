import rich_click as click
import yaml
import random
import shutil
from pathlib import Path
from mutagen import File

# Load configuration from YAML file
def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    
    source_dir = config.get('source_directory', '')
    destination_dir = config.get('destination_directory', '')
    exclude_dirs = config.get('exclude_directories', [])
    
    return source_dir, destination_dir, exclude_dirs

# Get list of all music files in the source directory, excluding certain subdirectories
def get_music_files(source_dir, exclude_dirs):
    source_path = Path(source_dir).resolve()
    
    music_files = []
    for file in source_path.rglob('*.*'):
        if file.suffix.lower() in {'.mp3', '.wav', '.flac'}:
            if not any([dir in file.parts for dir in exclude_dirs]):
                music_files.append(file)
    
    return music_files

# Get the song title from metadata or fallback to the filename
def get_song_title(file):
    audio = File(file)
    if audio and ('title' in audio):
        # Extract title from metadata
        title = audio['title'][0]
    else:
        # Fallback to filename without extension
        title = file.stem
    return title

# Copy random music files to the USB drive, organized by artist
def copy_music_files(music_files, usb_mount_point):
    usb_path = Path(usb_mount_point).resolve()
    
    if not usb_path.is_dir():
        raise ValueError(f"The USB mount point {usb_mount_point} is not a valid directory.")
    
    total_size = 0
    for file in random.sample(music_files, len(music_files)):
        file_size = file.stat().st_size
        if total_size + file_size > 29.7 * 1024**3:  # Assuming USB key size limit (4GB example)
            break
        
        # Extract artist and song title
        relative_path = file.relative_to(file.parents[1])
        artist = file.parents[1].name
        song_title = get_song_title(file) + file.suffix
        
        # Create artist directory if it doesn't exist
        artist_dir = usb_path / artist
        artist_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy the file to the artist directory
        dest_file = artist_dir / song_title
        shutil.copy2(file, dest_file)
        total_size += file_size
        print(f"Copied {file} to {dest_file}")

@click.command()
@click.option('--config', default='config.yaml', type=click.Path(exists=True, readable=True), help="Configuration file for directories to exclude.")
def main(config):
    """Randomly copy music files from SOURCE_DIR to USB_MOUNT_POINT, excluding directories specified in CONFIG, and organize by artist."""
    source_dir, usb_mount_point, exclude_dirs = load_config(config)
    music_files = get_music_files(source_dir, exclude_dirs)
    
    if not music_files:
        print("No music files found after applying exclusions.")
        return
    
    copy_music_files(music_files, usb_mount_point)

if __name__ == "__main__":
    main()
