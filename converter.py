from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from PyQt5.QtCore import QObject, pyqtSignal

class VideoConverter(QObject):
    progress_update = pyqtSignal(str)
    conversion_progress = pyqtSignal(int)  # Progress percentage
    
    def __init__(self):
        super().__init__()

    def convert_video(self, input_path, output_path, resolution=None, bitrate=None, codec=None, progress_callback=None):
        try:
            self.progress_update.emit(f"Loading video: {os.path.basename(input_path)}")
            clip = VideoFileClip(input_path)

            if resolution:
                self.progress_update.emit(f"Resizing to {resolution[0]}x{resolution[1]}")
                clip = clip.resized(new_size=resolution)
            
            # Set output parameters
            ffmpeg_options = []
            if bitrate:
                ffmpeg_options.append(f"-b:v {bitrate}")
            if codec:
                ffmpeg_options.append(f"-c:v {codec}")

            self.progress_update.emit(f"Converting to {os.path.basename(output_path)}")
            
            # Custom progress callback for MoviePy
            def progress_bar(get_frame, t):
                if progress_callback:
                    progress_percentage = int((t / clip.duration) * 100)
                    progress_callback(progress_percentage)
                return get_frame(t)

            # Write the video file with progress tracking
            write_params = {
                'filename': output_path,
                'logger': None
            }
            
            if codec:
                write_params['codec'] = codec
            if bitrate:
                write_params['bitrate'] = bitrate
            if ffmpeg_options:
                write_params['ffmpeg_params'] = ffmpeg_options
                
            clip.write_videofile(**write_params)
            clip.close()
            
            self.progress_update.emit("Conversion completed successfully!")
            return True, "Conversion successful!"
            
        except Exception as e:
            self.progress_update.emit(f"Error: {str(e)}")
            return False, f"Conversion failed: {e}"

    def convert_batch(self, file_list, output_dir, settings, progress_callback=None):
        """
        Convert multiple videos with the same settings
        """
        total_files = len(file_list)
        successful_conversions = 0
        failed_conversions = []
        
        for i, input_path in enumerate(file_list):
            try:
                # Generate output path
                filename = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(output_dir, f"{filename}{settings['format']}")
                
                self.progress_update.emit(f"Processing {i+1}/{total_files}: {os.path.basename(input_path)}")
                
                # Convert individual video
                success, message = self.convert_video(
                    input_path, output_path,
                    settings.get('resolution'),
                    settings.get('bitrate'),
                    settings.get('codec')
                )
                
                if success:
                    successful_conversions += 1
                    self.progress_update.emit(f"✓ Completed: {os.path.basename(input_path)}")
                else:
                    failed_conversions.append((input_path, message))
                    self.progress_update.emit(f"✗ Failed: {os.path.basename(input_path)} - {message}")
                
                # Update overall progress
                if progress_callback:
                    overall_progress = int(((i + 1) / total_files) * 100)
                    progress_callback(overall_progress)
                    
            except Exception as e:
                failed_conversions.append((input_path, str(e)))
                self.progress_update.emit(f"✗ Error processing {os.path.basename(input_path)}: {str(e)}")
        
        # Summary
        summary = f"Batch conversion completed: {successful_conversions}/{total_files} successful"
        if failed_conversions:
            summary += f", {len(failed_conversions)} failed"
        
        self.progress_update.emit(summary)
        return successful_conversions, failed_conversions

if __name__ == '__main__':
    converter = VideoConverter()
    # Example usage (replace with actual paths and desired settings)
    # success, message = converter.convert_video("input.mp4", "output.avi", resolution=(640, 480), bitrate="1000k", codec="mpeg4")
    # print(message)

