import requests
from bs4 import BeautifulSoup
import os

# Function to download an image from a URL
def download_image(url, folder_name, image_name):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            image_path = os.path.join(folder_name, image_name)
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image {image_name} downloaded successfully.")
        else:
            print(f"Failed to retrieve image {image_name}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image {image_name}: {e}")

# Function to search and download images based on a keyword
def fetch_images(keyword, limit=10):
    # Create the folder to save the images
    folder_name = keyword.replace(" ", "_")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Search for images on Google
    search_url = f"https://www.google.com/search?q={keyword}&tbm=isch"
    headers = {
        "User-Agent": 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img', limit=limit)

    if not images:
        print("No images found.")
        return

    # Download the found images
    for i, img in enumerate(images):
        img_url = img['src']
        image_name = f"{keyword}_{i + 1}.jpg"
        download_image(img_url, folder_name, image_name)

# Using the function to search and download images
keyword = str(input("Enter the keyword to search: "))
fetch_images(keyword, limit=20)
