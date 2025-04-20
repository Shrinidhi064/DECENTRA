import requests
from PIL import Image
import io

# Convert image to grayscale before sending
def preprocess_image(image_path):
    img = Image.open(image_path).convert("L")
    
    img.show()  # Display the image
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")  # Save image in bytes format
    img_bytes.seek(0)  # Reset the pointer to the beginning of the bytes
    return img_bytes

url = "http://127.0.0.1:8000/api/predict_similarity/"

files = {
    "image1": ("img1.png", preprocess_image("C:/Users/HP/Pictures/Screenshots/test1.png"), "image/png"),
    "image2": ("img2.png", preprocess_image("C:/Users/HP/Pictures/Screenshots/test1.png"), "image/png"),
}

response = requests.post(url, files=files)
print(response.text)
