import cv2
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the image
image_path = "C:/Users/HP/Downloads/cheque3.jpeg"  # Replace with the path to your image
image = cv2.imread(image_path)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis('off')
plt.show()

# Step 2: Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray_image, cmap='gray')
plt.title('Grayscale Image')
plt.axis('off')
plt.show()

# Step 3: Apply Advanced Denoising using Non-Local Means Denoising
denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 8, 7, 21)
plt.imshow(denoised_image, cmap='gray')
plt.title('Denoised Image (Non-Local Means)')
plt.axis('off')
plt.show()

# Step 4: Sharpening using Unsharp Masking
gaussian_blurred = cv2.GaussianBlur(denoised_image, (3, 3), 0)
sharpened_image = cv2.addWeighted(denoised_image, 2.0, gaussian_blurred, -1.0, 0)  # Increased sharpening effect
plt.imshow(sharpened_image, cmap='gray')
plt.title('Sharpened Image (Increased Effect)')
plt.axis('off')
plt.show()

# Step 5: Increase brightness (Add constant value to pixel intensities)
brightness_increased_image = cv2.convertScaleAbs(sharpened_image, alpha=1, beta=50)  # alpha=1, beta=50 adjusts brightness
plt.imshow(brightness_increased_image, cmap='gray')
plt.title('Brightness Increased Image')
plt.axis('off')
plt.show()

