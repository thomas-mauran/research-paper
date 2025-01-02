import os
from astropy.io import fits
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Directories
input_dir = "./img/"
png_dir = "./png"
os.makedirs(png_dir, exist_ok=True)

# Parameters for cropping
crop_size = 1000  # Crop dimensions (1000x1000)
center_x, center_y = 2250, 750  # Adjust to your desired center coordinates

# Gamma correction function
def gamma_correction(image, gamma=1.0):
    norm_image = image / 255.0
    corrected_image = np.power(norm_image, gamma)
    return (corrected_image * 255).astype(np.uint8)

# Crop function
def crop_center(image, center_x, center_y, crop_size):
    half_size = crop_size // 2
    start_x = max(center_x - half_size, 0)
    start_y = max(center_y - half_size, 0)
    end_x = start_x + crop_size
    end_y = start_y + crop_size
    return image[start_y:end_y, start_x:end_x]

# Font settings for frame number overlay
try:
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust if necessary
    font = ImageFont.truetype(font_path, 50)
except:
    print("Warning: Font not found, using default font.")
    font = ImageFont.load_default()  # Fallback font

# Process each FITS file
for index, filename in enumerate(sorted(os.listdir(input_dir))):  # Sort to process frames in order
    if filename.endswith(".fit"):
        filepath = os.path.join(input_dir, filename)
        
        try:
            # Open the FITS file
            with fits.open(filepath) as hdul:
                data = hdul[0].data  # Assuming the image data is in the first HDU
                
                # Use the frame number as the overlay text
                frame_number = f"Frame {index + 1}"  # Frame number starts at 1
                
                # Handle 3D data by summing along the first dimension
                if len(data.shape) == 3:
                    data = np.sum(data, axis=0)
                
                # Replace NaN values with zero
                data = np.nan_to_num(data)
                
                # Normalize the data to 0-255 for image conversion
                norm_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * 255
                norm_data = norm_data.astype(np.uint8)
                
                # Apply gamma correction
                bright_data = gamma_correction(norm_data, gamma=0.4)
                
                # Crop the image
                cropped_data = crop_center(bright_data, center_x, center_y, crop_size)
                
                # Convert to a PIL Image for overlay
                image = Image.fromarray(cropped_data)
                draw = ImageDraw.Draw(image)
                
                # Add frame number to the image (ensure compatibility with grayscale images)
                text_position = (20, 20)  # Top-left corner
                text_color = 255  # White for grayscale
                shadow_color = 0  # Black shadow for grayscale
                if image.mode != "L":  # If not grayscale, use RGB
                    text_color = (255, 255, 255)  # White
                    shadow_color = (0, 0, 0)  # Black
                
                # Draw shadow
                draw.text((text_position[0] + 1, text_position[1] + 1), frame_number, font=font, fill=shadow_color)
                # Draw frame number
                draw.text(text_position, frame_number, font=font, fill=text_color)
                
                # Save the PNG image
                png_filename = filename.replace(".fit", ".png")
                png_path = os.path.join(png_dir, png_filename)
                image.save(png_path)
                
                print(f"Converted {filename} to {png_path} with frame number overlay.")
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Conversion completed!")
