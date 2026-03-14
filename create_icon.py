"""Create app icon for FolderZipperVersioning"""
from PIL import Image, ImageDraw, ImageFont

# Create 512x512 image with white background
img = Image.new('RGB', (512, 512), color='white')
draw = ImageDraw.Draw(img)

# Draw folder shape (blue gradient effect)
folder_color = '#4A90D9'
folder_dark = '#2E5C8A'

# Main folder body
draw.rectangle([(80, 180), (432, 460)], fill=folder_color)

# Folder tab on top left
draw.rectangle([(80, 100), (240, 180)], fill=folder_color)

# Inner folder (lighter for depth)
draw.rectangle([(120, 220), (392, 420)], fill=folder_dark)

# ZIP label background
draw.rectangle([(180, 280), (332, 380)], fill='white')

# ZIP text (simulated with rectangle blocks)
draw.rectangle([(200, 300), (230, 360)], fill='#4A90D9')  # Z left
draw.rectangle([(240, 300), (270, 360)], fill='#4A90D9')  # I
draw.rectangle([(280, 300), (310, 360)], fill='#4A90D9')  # P

# Add zipper teeth on top
for i in range(100, 400, 20):
    draw.rectangle([(i, 165), (i+10, 175)], fill='#1a3d5c')

# Add subtle shadow
draw.arc([(60, 160), (452, 480)], 0, 360, fill='#CCCCCC', width=2)

img.save('D:/personaldata/vibe-coding-projekte/zip-folder-automation/app-files/app_icon.png')
print("✓ Icon created: app-files/app_icon.png")
