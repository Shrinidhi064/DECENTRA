import tempfile
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import requests
from django.conf import settings
import cv2
import os,io
import numpy as np
import matplotlib.pyplot as plt
import google.generativeai as genai
import warnings
import torch
import torchvision.transforms as transforms
from PIL import Image
from gemini_app.models import model,device
warnings.filterwarnings("ignore")

# Configure Google API with your API Key
os.environ['GOOGLE_API_KEY'] = settings.GEMINI_API_KEY
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def process_image(image_path):
    image = cv2.imread(image_path)
    
    # Step 2: Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply Advanced Denoising using Non-Local Means Denoising
    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 8, 7, 21)

    # Step 4: Sharpening using Unsharp Masking
    gaussian_blurred = cv2.GaussianBlur(denoised_image, (3, 3), 0)
    sharpened_image = cv2.addWeighted(denoised_image, 2.0, gaussian_blurred, -1.0, 0)  # Increased sharpening effect

    # Step 5: Increase brightness (Add constant value to pixel intensities)
    brightness_increased_image = cv2.convertScaleAbs(sharpened_image, alpha=1, beta=50)  # alpha=1, beta=50 adjusts brightness

    # Plotting all the intermediate results in a grid layout
    plt.figure(figsize=(12, 8))
    
    # Original Image
    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    # Grayscale Image
    plt.subplot(2, 3, 2)
    plt.imshow(gray_image, cmap='gray')
    plt.title('Grayscale Image')
    plt.axis('off')

    # Denoised Image
    plt.subplot(2, 3, 3)
    plt.imshow(denoised_image, cmap='gray')
    plt.title('Denoised Image')
    plt.axis('off')

    # Sharpened Image
    plt.subplot(2, 3, 4)
    plt.imshow(sharpened_image, cmap='gray')
    plt.title('Sharpened Image')
    plt.axis('off')

    # Brightness Increased Image
    plt.subplot(2, 3, 5)
    plt.imshow(brightness_increased_image, cmap='gray')
    plt.title('Brightness Increased Image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Return the final processed image (brightness increased)
    return brightness_increased_image

@csrf_exempt
def process_cheque(request):
    if request.method == 'POST' and 'file' in request.FILES:
        try:
            # Get the uploaded cheque image
            uploaded_file = request.FILES['file']

            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

                temp_file_path = temp_file.name  # Path of the temporary file
            
            # Process the image
            processed_image = process_image(temp_file_path)

            # Save the processed image temporarily
            processed_image_path = temp_file_path.replace(".png", "_processed.png")
            cv2.imwrite(processed_image_path, processed_image)

            # Upload the processed image to the Google API
            uploaded_image_response = genai.upload_file(
                path=processed_image_path,  # Path of the processed image
                display_name=uploaded_file.name  # Display the original file name
            )

            if uploaded_image_response:
                # After successfully uploading, create a Generative Model
                model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

                # Generate the text response using the image and the prompt
                reconstructed_prompt = "Extract all the text (both Hindi and English) from the cheque image in such a way that highlight the important fields like payee name, amount in number, amount in words, IFSC code, bank name, branch, MICR code, account number, sappm number (if present), date rest all you give it as other fields:"
                response_data = model.generate_content(
                    [uploaded_image_response, reconstructed_prompt]
                )

                # Extract the text from the response
                extracted_text = response_data.text if hasattr(response_data, 'text') else "No text found."

                return JsonResponse({"extractedText": extracted_text})

            else:
                return JsonResponse({"error": "Failed to upload the processed image to the API."}, status=500)

        except Exception as e:
            return JsonResponse({"error": "An error occurred", "details": str(e)}, status=500)

    else:
        return JsonResponse({"error": "File is required."}, status=400)
@csrf_exempt  
def upload_cheque(request): 
    if request.method == "POST" and request.FILES.get("cheque_image"):
        cheque_image = request.FILES["cheque_image"]

        # Ensure "uploads" folder exists
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Generate cheque image path
        cheque_filename = cheque_image.name
        cheque_path = os.path.join(upload_dir, cheque_filename)

        # Ensure cheque_path is a file, not a folder
        if os.path.exists(cheque_path) and os.path.isdir(cheque_path):
            os.rmdir(cheque_path)  # Remove incorrect folder

        # Save the uploaded cheque image
        with open(cheque_path, "wb") as f:
            for chunk in cheque_image.chunks():
                f.write(chunk)

        # Read image using OpenCV
        img = cv2.imread(cheque_path)
        if img is None:
            return JsonResponse({"error": "Invalid image file"}, status=400)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on size and location
        signature_contours = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 50 and h > 20 and y > gray.shape[0] // 2:  # Signature is usually in the lower half
                signature_contours.append((x, y, w, h))

        # Sort detected contours by y-position (to pick the lowest one)
        signature_contours = sorted(signature_contours, key=lambda b: b[1], reverse=True)

        # If we found at least one possible signature region, crop it
        if signature_contours:
            x, y, w, h = signature_contours[0]  # Select the lowest detected region
            signature = img[y:y+h, x:x+w]

            # Save cropped signature
            signature_filename = f"cropped_signature_{cheque_filename}"
            signature_path = os.path.join(upload_dir, signature_filename)
            cv2.imwrite(signature_path, signature)

            # Generate URL for the frontend
            signature_url = request.build_absolute_uri(settings.MEDIA_URL + "uploads/" + signature_filename)

            return JsonResponse({"signature_url": signature_url})

        else:
            return JsonResponse({"error": "No signature detected. Try adjusting threshold values."}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)
def generate_content(request):
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = JsonResponse({"message": "Preflight OK"})
        response['Allow'] = 'POST, OPTIONS'
        return response

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(settings.GEMINI_API_KEY)  # Log the Gemini API key for debugging

            query_text = data.get('queryText')

            if not query_text:
                return JsonResponse({"error": "Query text is required."}, status=400)

            gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"

            payload = {
                "contents": [{
                    "parts": [{
                        "text": query_text
                    }]
                }]
            }

            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.post(gemini_api_url, json=payload, headers=headers)
            print(f"Gemini API response: {response.json()}")

            # Handle the Gemini API response
            if response.status_code == 200:
                api_response = response.json()
                # Extract the generated text
                candidates = api_response.get("candidates", [])
                if candidates:
                    generated_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "No content generated.")
                else:
                    generated_text = "No candidates found in the API response."

                return JsonResponse({"generatedContent": generated_text})

            else:
                # Handle API errors
                return JsonResponse({"error": "Failed to generate content", "details": response.text}, status=response.status_code)

        except Exception as e:
            # Handle any unexpected errors
            print(f"Error occurred: {e}")
            return JsonResponse({"error": "An error occurred", "details": str(e)}, status=500)

    else:
        # If the method is not POST, return a 405 Method Not Allowed
        return JsonResponse({"error": "Invalid request method"}, status=405)
# Define image preprocessing function
def preprocess_image(image_pth):

    gray = image_pth.convert("L")

    img = np.array(gray)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,2))
    morphology_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)

    blur = cv2.GaussianBlur(morphology_img, (3,3),0)

    _, binary = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    coords = cv2.findNonZero(binary)
    x, y, w, h = cv2.boundingRect(coords)

    padding = 5
    x -= padding
    y -= padding
    w += 2 * padding
    h += 2 * padding

    x = max(0, x)
    y = max(0, y)
    w = min(w, img.shape[1] - x)
    h = min(h, img.shape[0] - y)

    cropped_image = binary[y:y + h, x:x + w]

    extra_space = np.zeros((cropped_image.shape[0] + 2 * padding, cropped_image.shape[1] + 2 * padding), dtype=np.uint8) * 255
    extra_space[padding:-padding, padding:-padding] = cropped_image

    corrected = cv2.resize(extra_space,(330,175))
    resized_image = Image.fromarray(corrected)

    return resized_image
    
    
# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define a function to convert images to grayscale


# Define the get_predictions_for_single function
def get_predictions_for_single(img1, img2, model, device):
    # Ensure images are in grayscale
    img1 = preprocess_image(img1)
    img2 = preprocess_image(img2)

    # Preprocess the images
    transform = transforms.Compose([
        transforms.Resize((200,300)),
        transforms.ToTensor(),
    ])
    input1 = transform(img1).unsqueeze(0).to(device)
    input2 = transform(img2).unsqueeze(0).to(device)

    # Make predictions using the model
    model.eval()
    with torch.no_grad():
        predictions = model(input1, input2)
        print(predictions)

    # Determine the prediction label
    similarity_score = predictions.item()  # Convert tensor to scalar
    return similarity_score

# Example usage in Django API view
@csrf_exempt  
@api_view(["POST"])
def predict_similarity(request):
    try:
        if "image1" not in request.FILES or "image2" not in request.FILES:
            return JsonResponse({"error": "Both images are required"}, status=400)

        image1 = request.FILES["image1"]
        image2 = request.FILES["image2"]

        # Ensure images are in grayscale
        img1 = Image.open(image1).convert("L")
        img2 = Image.open(image2).convert("L")

        # Ensure model is defined
        if "model" not in globals():
            return JsonResponse({"error": "Model is not loaded"}, status=500)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Get similarity score
        similarity_score = get_predictions_for_single(img1, img2, model, device)

        # Define similarity threshold
        result = "Similar" if similarity_score > 0.8 else "Not Similar"

        return JsonResponse({"prediction": result, "confidence": float(similarity_score)})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)