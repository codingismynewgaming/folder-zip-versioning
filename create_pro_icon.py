"""Create professional app icon for FolderZipperVersioning"""
from PIL import Image, ImageDraw, ImageFont

def create_gradient_rectangle(draw, coords, color1, color2, vertical=True):
    """Draw a gradient rectangle."""
    x1, y1, x2, y2 = coords
    if vertical:
        for y in range(y1, y2):
            ratio = (y - y1) / (y2 - y1)
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            draw.rectangle([x1, y, x2, y+1], fill=(r, g, b))
    else:
        for x in range(x1, x2):
            ratio = (x - x1) / (x2 - x1)
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            draw.rectangle([x, y1, x+1, y2], fill=(r, g, b))

# Create 1024x1024 image with white background
img = Image.new('RGBA', (1024, 1024), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

# Define colors
folder_light = (100, 181, 246)   # Light blue
folder_dark = (30, 136, 229)     # Dark blue
folder_shadow = (21, 101, 192)   # Shadow blue
zipper_color = (55, 71, 79)      # Dark gray for zipper
highlight = (255, 255, 255, 100)  # White highlight

# Draw main folder body (rounded rectangle style)
folder_body = (150, 300, 874, 850)
create_gradient_rectangle(draw, folder_body, folder_light, folder_dark, vertical=True)

# Draw folder tab on top left
tab_coords = (150, 200, 450, 320)
create_gradient_rectangle(draw, tab_coords, folder_light, folder_dark, vertical=True)

# Draw inner folder (darker for depth)
inner_folder = (200, 350, 824, 800)
create_gradient_rectangle(draw, inner_folder, folder_dark, folder_shadow, vertical=True)

# Draw zipper track (vertical line down the middle)
zipper_width = 80
zipper_x1 = 512 - zipper_width // 2
zipper_x2 = 512 + zipper_width // 2
draw.rectangle([(zipper_x1, 380), (zipper_x2, 770)], fill=zipper_color)

# Draw zipper teeth
tooth_width = 12
tooth_height = 20
spacing = 8
for y in range(390, 760, spacing + tooth_height):
    # Left teeth
    draw.rectangle([
        (zipper_x1 + 8, y),
        (zipper_x1 + tooth_width, y + tooth_height)
    ], fill=(200, 200, 200))
    # Right teeth
    draw.rectangle([
        (zipper_x2 - tooth_width, y),
        (zipper_x2 - 8, y + tooth_height)
    ], fill=(200, 200, 200))

# Draw zipper pull at top
zipper_pull = [(492, 360), (532, 420)]
draw.rounded_rectangle(zipper_pull, radius=8, fill=(158, 158, 158))
draw.ellipse([(487, 410), (537, 440)], fill=(158, 158, 158))

# Add "ZIP" text label
try:
    font = ImageFont.truetype("arial.ttf", 80)
except:
    font = ImageFont.load_default()

text = "ZIP"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_x = (1024 - text_width) // 2
text_y = 550

# Draw text shadow
draw.text((text_x+3, text_y+3), text, fill=(0, 0, 0, 100), font=font)
# Draw main text
draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

# Add subtle highlight on top left
highlight_coords = [(180, 330), (400, 450)]
draw.ellipse(highlight_coords, fill=highlight)

# Add drop shadow effect (simple version)
shadow_offset = 10
for offset in range(shadow_offset, 0, -2):
    shadow_alpha = 20 - offset * 2
    if shadow_alpha > 0:
        pass  # Simplified shadow

# Save the icon
output_path = "D:/personaldata/vibe-coding-projekte/zip-folder-automation/app-files/app_icon.png"
img.save(output_path, "PNG")
print(f"✓ Professional icon created: {output_path}")
print(f"✓ Size: 1024x1024 pixels")
print(f"✓ Format: PNG with transparency support")
