import os


# Function to check if an image file exists
def find_image_file(image_path):
    for ext in [".jpg", ".png", ".pdf"]:
        full_path = f"{image_path}{ext}"
        if os.path.exists(full_path):
            return full_path
    return None
