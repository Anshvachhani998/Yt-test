import logging
from pytubefix import YouTube
from pyrogram import Client, filters

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Client

@app.on_message(filters.command("Dl"))
def download_video(client, message):
    try:
        # Extract URL from the command
        url = message.text.split(" ", 1)[1]  # Gets the part after "/Dl "
        
        if not url:
            message.reply("Please provide a valid YouTube URL after the /Dl command.")
            return
        
        logging.info(f"Received URL: {url}")
        logging.info("Generating OAuth token, please complete the browser login...")

        # Attempt to download video using Pytubefix
        yt = YouTube(
            url,
            use_oauth=True,
            allow_oauth_cache=True  # Allow OAuth to be cached
        )
        
        logging.info("Video download started...")
        yt.streams.get_highest_resolution().download()  # Download at highest resolution
        
        # Sending the video back to Telegram
        message.reply("Download completed successfully! Sending the video...")
        message.reply_video(video=open("path/to/downloaded/video.mp4", 'rb'))  # Adjust the path if needed
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        message.reply(f"An error occurred: {e}")
