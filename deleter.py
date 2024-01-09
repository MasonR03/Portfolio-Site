import os
from PIL import Image

def is_portrait(image_path):
    with Image.open(image_path) as img:
        return img.height > img.width

def delete_non_portrait_images(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                if not is_portrait(image_path):
                    os.remove(image_path)
                    print(f"Deleted: {image_path}")

# Replace with your folder path
folder_path = '/home/raspberry/Desktop/Portfolio Site/images/display/Compressed'
delete_non_portrait_images(folder_path)
