import requests
from PIL import Image
import io

# Convert image to grayscale before sending
def preprocess_image(image_path_or_url):
    if image_path_or_url.startswith("http"):  # Check if it's a URL
        response = requests.get(image_path_or_url)
        img = Image.open(io.BytesIO(response.content)).convert("L")
        img.show()
    else:  # Otherwise, treat it as a file path
        img = Image.open(image_path_or_url).convert("L")
        img.show()
    # Display the image for verification
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")  # Save image in bytes format
    img_bytes.seek(0)  # Reset pointer to the start
    return img_bytes

url = "http://127.0.0.1:8000/api/predict_similarity/"

# Example Pinata IPFS link
pinata_ipfs_link = "https://ipfs.io/ipfs/bafkreiezuc56p5uor5llx3sb6pjg6pn35wf4shl4jlxlivfs4n7brxoh6m"

files = {
    "image2": ("img2.png", preprocess_image("C:/Users/HP/Pictures/Screenshots/test1.png"), "image/png"),
    "image1": ("img1.png", preprocess_image(pinata_ipfs_link), "image/png"),
}

response = requests.post(url, files=files)
print(response.text)
