import requests
import os

SORA_API_URL = "https://sora.com/api/video"
SORA_API_KEY = os.getenv("SORA_API_KEY")

def generate_video(prompt):
    """Generates a short AI video using Sora API."""
    response = requests.post(SORA_API_URL, json={"prompt": prompt}, headers={"Authorization": f"Bearer {SORA_API_KEY}"})
    return response.json().get("video_url")

if __name__ == "__main__":
    print(generate_video("A chaotic Holi celebration at Mumbai beach with colorful water splashes."))