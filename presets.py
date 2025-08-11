# Format presets for common conversion scenarios

CONVERSION_PRESETS = {
    "Web Optimized (MP4)": {
        "format": ".mp4",
        "codec": "libx264",
        "resolution": (1280, 720),
        "bitrate": "1000k",
        "description": "Optimized for web streaming and social media"
    },
    "High Quality (MP4)": {
        "format": ".mp4",
        "codec": "libx264",
        "resolution": None,  # Keep original
        "bitrate": "5000k",
        "description": "High quality for archival purposes"
    },
    "Mobile Friendly": {
        "format": ".mp4",
        "codec": "libx264",
        "resolution": (854, 480),
        "bitrate": "500k",
        "description": "Small file size for mobile devices"
    },
    "YouTube Upload": {
        "format": ".mp4",
        "codec": "libx264",
        "resolution": (1920, 1080),
        "bitrate": "2000k",
        "description": "Optimized for YouTube uploads"
    },
    "Instagram Story": {
        "format": ".mp4",
        "codec": "libx264",
        "resolution": (1080, 1920),  # 9:16 aspect ratio
        "bitrate": "1500k",
        "description": "Vertical format for Instagram stories"
    },
    "DVD Quality": {
        "format": ".avi",
        "codec": "mpeg4",
        "resolution": (720, 480),
        "bitrate": "1500k",
        "description": "Standard DVD quality"
    },
    "Ultra Compressed": {
        "format": ".mp4",
        "codec": "libx264",
        "resolution": (640, 360),
        "bitrate": "250k",
        "description": "Maximum compression for minimal file size"
    }
}

def get_preset_names():
    """Return list of preset names"""
    return list(CONVERSION_PRESETS.keys())

def get_preset_settings(preset_name):
    """Get settings for a specific preset"""
    return CONVERSION_PRESETS.get(preset_name, None)

def get_preset_description(preset_name):
    """Get description for a specific preset"""
    preset = CONVERSION_PRESETS.get(preset_name, {})
    return preset.get("description", "No description available")

