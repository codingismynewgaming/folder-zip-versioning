"""Generate new app icon using OpenRouter API"""
import requests
import base64
import os

API_KEY = "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"

prompt = "A modern professional app icon for a folder zip utility application, blue gradient folder icon with visible zipper running down the middle, clean minimalist design, white background, software icon style, high quality, 1024x1024"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "google/gemini-3-pro-image-preview",
    "prompt": prompt,
    "n": 1,
    "size": "1024x1024",
    "response_format": "url"
}

response = requests.post(
    "https://openrouter.ai/api/v1/images/generations",
    headers=headers,
    json=data
)

if response.status_code == 200:
    result = response.json()
    if "data" in result and len(result["data"]) > 0:
        image_url = result["data"][0]["url"]
        print(f"✓ Image generated: {image_url}")
        
        # Download the image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            output_path = "D:/personaldata/vibe-coding-projekte/zip-folder-automation/app-files/app_icon.png"
            with open(output_path, "wb") as f:
                f.write(img_response.content)
            print(f"✓ Icon saved to: {output_path}")
        else:
            print(f"❌ Error downloading image: {img_response.status_code}")
    else:
        print(f"❌ Error: No image data in response: {result}")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
