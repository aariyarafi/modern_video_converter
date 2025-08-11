# Modern Video Converter

A user-friendly video conversion application built with Python and PyQt5, featuring a modern dark theme interface and support for multiple video formats.

## Features

- **Modern GUI**: Clean, dark-themed interface with tabbed navigation
- **Multiple Formats**: Support for MP4, AVI, MKV, MOV, WMV, FLV, WebM, and M4V
- **Single & Batch Conversion**: Convert individual videos or process multiple files at once
- **Conversion Presets**: Pre-configured settings for common scenarios (Web, YouTube, Mobile, etc.)
- **Progress Tracking**: Real-time conversion progress with detailed logging
- **Flexible Settings**: Customizable resolution, codec, and bitrate options

## Supported Formats

### Input Formats
- MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V

### Output Formats
- MP4, AVI, MKV, MOV, WMV, FLV, WebM

### Codecs
- H.264 (libx264)
- H.265 (libx265)
- VP9 (libvpx-vp9)
- VP8 (libvpx)
- MPEG-4

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (system-wide installation required)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add to PATH.

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Single Video Conversion

1. Go to the "Single Conversion" tab
2. Click "Browse" to select your input video file
3. Choose output directory
4. Configure format, resolution, codec, and bitrate settings
5. Click "Convert Video"

### Batch Conversion

1. Go to the "Batch Conversion" tab
2. Click "Add Files" to select multiple video files
3. Choose output directory
4. Settings from the "Single Conversion" tab will be applied to all files
5. Click "Convert All Files"

### Using Presets

1. Go to the "Presets" tab
2. Select a preset from the list to view its details
3. Click "Apply Preset to Single Conversion" to use the preset
4. Switch to "Single Conversion" tab to see applied settings

## Available Presets

- **Web Optimized (MP4)**: 720p, 1000k bitrate - Perfect for web streaming
- **High Quality (MP4)**: Original resolution, 5000k bitrate - For archival
- **Mobile Friendly**: 480p, 500k bitrate - Small file size for mobile
- **YouTube Upload**: 1080p, 2000k bitrate - Optimized for YouTube
- **Instagram Story**: 1080x1920, 1500k bitrate - Vertical format
- **DVD Quality**: 720x480, 1500k bitrate - Standard DVD quality
- **Ultra Compressed**: 360p, 250k bitrate - Maximum compression

## Project Structure

```
video_converter/
├── main.py              # Application entry point
├── gui.py               # GUI implementation
├── converter.py         # Video conversion logic
├── config.py            # Configuration settings
├── utils.py             # Utility functions
├── presets.py           # Conversion presets
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technical Details

- **GUI Framework**: PyQt5 for cross-platform native interface
- **Video Processing**: MoviePy library with FFmpeg backend
- **Threading**: Separate thread for conversion to keep UI responsive
- **Progress Tracking**: Real-time progress updates and logging

## Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**
   - Ensure FFmpeg is installed and available in system PATH
   - Test with `ffmpeg -version` in terminal

2. **"Module not found" errors**
   - Install required dependencies: `pip install -r requirements.txt`
   - Ensure you're using Python 3.8+

3. **GUI doesn't appear**
   - Check if display is available (for Linux servers, may need X11 forwarding)
   - Try running with `python main.py` instead of background execution

4. **Conversion fails**
   - Check input file format is supported
   - Ensure sufficient disk space in output directory
   - Check conversion log for detailed error messages

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Acknowledgments

- Built with [PyQt5](https://pypi.org/project/PyQt5/) for the GUI
- Video processing powered by [MoviePy](https://pypi.org/project/moviepy/)
- Uses [FFmpeg](https://ffmpeg.org/) for video encoding/decoding

