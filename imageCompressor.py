import os
import sys
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageCompressorHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.process(event)

    def process(self, event):
        if event.is_directory:
            return
        if os.path.splitext(event.src_path)[1].lower() in ['.jpg', '.jpeg', '.png']:
            print(f"Detected change in: {event.src_path}")  # Debug message
            self.compress_image(event.src_path)

    def compress_image(self, filepath):
        try:
            with Image.open(filepath) as img:
                img = img.convert('RGB')
                
                # Resize the image while maintaining its aspect ratio to fit within 700x700
                max_size = (700, 700)
                img.thumbnail(max_size)
                
                img.save(filepath, "JPEG", quality=80)
            print(f"Compressed image: {filepath}")
        except Exception as e:
            print(f"Error compressing {filepath}. Reason: {e}")



if __name__ == "__main__":
    path = '/home/raspberry/Desktop/Portfolio Site/images'  # specify the full path to your images directory here

    event_handler = ImageCompressorHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print(f"Starting image compression watcher on {path}")
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
