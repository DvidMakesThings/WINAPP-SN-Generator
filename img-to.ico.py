from PIL import Image
import os

# Open your PNG file
img = Image.open("ico.png")

# Optionally, resize the image to a standard icon size (e.g., 256x256)
img = img.resize((256, 256), Image.LANCZOS)

# Save as ICO
img.save("ico.ico", format="ICO")

# Delete the original PNG file
os.remove("ico.png")
