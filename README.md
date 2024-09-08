# Random Music to USB

A Python script to randomly copy music files from a source directory to a destination (e.g.: USB drive), excluding certain directories, and organize them by artist.

## Features

- Randomly selects music files from a source directory.
- Excludes specified directories (e.g., artists or genres) based on configuration.
- Organizes music files on the USB drive by artist.
- Handles metadata to correctly name files, falling back to filenames if metadata is absent.

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management and environment setup)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/random_music.git
cd random_music
```

### 2. Install Dependencies

Install Poetry if you haven't already:

```bash
pipx install poetry
```

Use Poetry to install the project's dependencies:

```bash
poetry install
```

## Configuration

Create a `config.yaml` file in the project directory with the following structure:

```yaml
source_directory: /path/to/music
destination_directory: /path/to/usb
exclude_directories:
  - 'ArtistName1'
  - 'ArtistName2'
```

- `source_directory`: The path to the directory containing your music files.
- `destination_directory`: The path to the USB drive or target directory where music files will be copied.
- `exclude_directories`: List of subdirectories (artists, genres) to exclude from the selection.

## Usage

Activate the Poetry-managed virtual environment:

```bash
poetry shell
```

Run the script using Poetry:

```bash
poetry run python random_music.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/miek770/random_music/issues).
