import rich_click as click
import yaml
import random
import shutil
from pathlib import Path
from mutagen import File
from typing import List, Tuple, Union


def load_config(config_file: str = "config.yaml") -> Tuple[str, str, List[str], int]:
    """Load configuration from YAML file."""
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    source_dir: str = config.get("source_directory", "")
    destination_dir: str = config.get("destination_directory", "")
    exclude_dirs: List[str] = config.get("exclude_directories", [])
    destination_space_gb: int = config.get("destination_space_gb", int)

    return source_dir, destination_dir, exclude_dirs, destination_space_gb


def get_music_files(source_dir: str, exclude_dirs: List[str]) -> List[Path]:
    """Get list of all music files in the source directory, excluding certain
    subdirectories.
    """
    source_path = Path(source_dir).resolve()

    music_files: List[Path] = []
    for file in source_path.rglob("*.*"):
        if file.suffix.lower() in {".mp3", ".wav", ".flac"}:
            if not any([dir in file.parts for dir in exclude_dirs]):
                music_files.append(file)

    return music_files


def get_song_title(file: Path) -> str:
    """Get the song title from metadata or fallback to the filename."""
    audio: Union[File, None] = File(file)
    if audio and ("title" in audio):
        # Extract title from metadata
        title = audio["title"][0]
    else:
        # Fallback to filename without extension
        title = file.stem
    return title


def copy_music_files(
    music_files: List[Path], usb_mount_point: str, destination_space_gb: int
):
    """Copy random music files to the USB drive, organized by artist."""
    usb_path: Path = Path(usb_mount_point).resolve()

    if not usb_path.is_dir():
        raise ValueError(
            f"The USB mount point {usb_mount_point} is not a valid directory."
        )

    total_size: int = 0
    for file in random.sample(music_files, len(music_files)):
        file_size: int = file.stat().st_size
        if (
            total_size + file_size > destination_space_gb * 1024**3
        ):  # Assuming USB key size limit (4GB example)
            break

        # Extract artist and song title
        artist: str = file.parents[1].name
        song_title: str = get_song_title(file) + file.suffix

        # Create artist directory if it doesn't exist
        artist_dir: Path = usb_path / artist
        artist_dir.mkdir(parents=True, exist_ok=True)

        # Copy the file to the artist directory
        dest_file: Path = artist_dir / song_title
        shutil.copy2(file, dest_file)
        total_size += file_size
        print(f"Copied {file} to {dest_file}")


@click.command()
@click.option(
    "--config",
    default="config.yaml",
    type=click.Path(exists=True, readable=True),
    help="Configuration file for directories to exclude.",
)
def main(config):
    """Randomly copy music files from SOURCE_DIR to USB_MOUNT_POINT, excluding
    directories specified in CONFIG, and organize by artist.
    """
    source_dir, usb_mount_point, exclude_dirs, destination_space_gb = load_config(
        config
    )
    music_files: List[Path] = get_music_files(source_dir, exclude_dirs)

    if not music_files:
        print("No music files found after applying exclusions.")
        return

    copy_music_files(music_files, usb_mount_point, destination_space_gb)


if __name__ == "__main__":
    main()
