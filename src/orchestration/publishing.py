import requests
import os

INSTAGRAM_API_URL = "https://graph.facebook.com/v12.0/me/media"
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_API_KEY")

def publish_video(video_path, caption):
    """Uploads video to Instagram."""
    files = {"video": open(video_path, "rb")}
    data = {"caption": caption, "access_token": INSTAGRAM_ACCESS_TOKEN}
    response = requests.post(INSTAGRAM_API_URL, files=files, data=data)
    return response.json()

if __name__ == "__main__":
    print(publish_video("final_video.mp4", "🎨 Holi celebrations! #Holi2024"))