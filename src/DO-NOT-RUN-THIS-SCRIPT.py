import time
import requests
import os
import re

def get_next_image_number(folder, prefix="image_", extension=".jpg"):
    existing_files = [f for f in os.listdir(folder) if f.startswith(prefix) and f.endswith(extension)]
    numbers = []
    for f in existing_files:
        match = re.match(rf"{prefix}(\d+){extension}", f)
        if match:
            numbers.append(int(match.group(1)))
    if numbers:
        return max(numbers) + 1
    else:
        return 1

def download_picsum_images(count=15, width=1920, height=1080, blur=1):
    folder = "picsum_images"
    os.makedirs(folder, exist_ok=True)
    base_url = f"https://picsum.photos/{width}/{height}/?blur={blur}&tstamp="
    start_num = get_next_image_number(folder)
    
    for i in range(start_num, start_num + count):
        timestamp = str(int(time.time() * 1000))
        url = base_url + timestamp
        
        print(f"Downloading image {i} from {url}")
        response = requests.get(url)
        
        if response.status_code == 200:
            filename = os.path.join(folder, f"image_{i}.jpg")
            try:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Saved {filename}")
            except PermissionError:
                print(f"Permission denied: cannot write to {filename}")
                break
        else:
            print(f"Failed to download image {i} (status code: {response.status_code})")
        
        time.sleep(0.1)

def ask_for_count():
    while True:
        user_input = input("How many images would you like to download? (default 15): ").strip()
        if user_input == "":
            return 15
        if user_input.isdigit() and int(user_input) > 0:
            return int(user_input)
        print("Please enter a positive integer or press Enter for default.")

def ask_for_aspect_ratio():
    while True:
        user_input = input("Enter aspect ratio WIDTH/HEIGHT (default 1920/1080): ").strip()
        if user_input == "":
            return 1920, 1080
        parts = user_input.split("/")
        if len(parts) == 2 and all(p.isdigit() and int(p) > 0 for p in parts):
            return int(parts[0]), int(parts[1])
        print("Invalid format. Please enter in WIDTH/HEIGHT format with positive integers.")

if __name__ == "__main__":
    count = ask_for_count()
    width, height = ask_for_aspect_ratio()
    download_picsum_images(count=count, width=width, height=height)
