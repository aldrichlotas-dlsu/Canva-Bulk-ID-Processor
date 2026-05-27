from PIL import Image
import os

# Set to your root folder where the script and mask.png live
base_dir = "." 
mask_filename = "mask.png"

# 1. Load the mask image
try:
    # Convert to RGBA to ensure we can read the transparency (Alpha) channel
    mask_img = Image.open(mask_filename).convert("RGBA")
    mask_width, mask_height = mask_img.size
    mask_pixels = list(mask_img.getdata()) 
except FileNotFoundError:
    print(f"Error: Could not find '{mask_filename}' in the root folder.")
    exit()

print(f"Loaded mask '{mask_filename}' ({mask_width}x{mask_height}). Processing ID folders...")

processed_count = 0

# 2. Walk through all folders and subfolders
for root, dirs, files in os.walk(base_dir):
    for filename in files:
        # Target the Front and Back images inside the person folders
        if filename.lower() in ["front.png", "back.png", "front.jpg", "back.jpg"]:
            filepath = os.path.join(root, filename)
            
            try:
                # Open target image and force it to RGBA (so it supports transparency)
                target_img = Image.open(filepath).convert("RGBA")
                
                # Failsafe: Ensure sizes match perfectly
                if target_img.size != (mask_width, mask_height):
                    print(f"Skipping {filepath}: Size mismatch! (Expected {mask_width}x{mask_height}, got {target_img.size[0]}x{target_img.size[1]})")
                    continue
                
                target_pixels = list(target_img.getdata())
                new_pixels = []
                
                # 3. Compare each pixel
                for i in range(len(target_pixels)):
                    # mask_pixels[i][3] is the Alpha (transparency) value of the mask pixel
                    # If alpha is greater than 50, it means it's the solid colored hole on your mask
                    if mask_pixels[i][3] > 50: 
                        # Set the target pixel's Alpha to 0 (Transparent)
                        r, g, b, _ = target_pixels[i]
                        new_pixels.append((r, g, b, 0))
                    else:
                        # Otherwise, keep the original pixel exactly as it is
                        new_pixels.append(target_pixels[i])
                        
                # 4. Apply new pixels and save
                target_img.putdata(new_pixels)
                
                # Save as PNG to preserve the new transparent hole
                new_filename = os.path.splitext(filename)[0] + ".png"
                new_filepath = os.path.join(root, new_filename)
                
                target_img.save(new_filepath, "PNG")
                
                # If the original was a JPG, delete the old JPG to avoid duplicates
                if filename.lower().endswith(('.jpg', '.jpeg')) and filepath != new_filepath:
                    os.remove(filepath)
                
                processed_count += 1
                
            except Exception as e:
                print(f"Could not process {filepath}: {e}")

print(f"\nDone! Successfully cut holes out of {processed_count} images.")