# Configuration settings for the video converter

# Supported video formats
SUPPORTED_INPUT_FORMATS = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
SUPPORTED_OUTPUT_FORMATS = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']

# Default settings
DEFAULT_OUTPUT_FORMAT = '.mp4'
DEFAULT_CODEC = 'libx264'
DEFAULT_BITRATE = '1000k'

# Resolution presets
RESOLUTION_PRESETS = {
    'Original': None,
    '1080p (1920x1080)': (1920, 1080),
    '720p (1280x720)': (1280, 720),
    '480p (854x480)': (854, 480),
    '360p (640x360)': (640, 360),
    '240p (426x240)': (426, 240)
}

# Codec options
CODEC_OPTIONS = {
    'H.264 (libx264)': 'libx264',
    'H.265 (libx265)': 'libx265',
    'VP9': 'libvpx-vp9',
    'VP8': 'libvpx',
    'MPEG-4': 'mpeg4'
}

# Bitrate presets
BITRATE_PRESETS = {
    'Low (500k)': '500k',
    'Medium (1000k)': '1000k',
    'High (2000k)': '2000k',
    'Very High (5000k)': '5000k',
    'Ultra (10000k)': '10000k'
}

