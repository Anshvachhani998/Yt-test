import logging
import os
from pytubefix import YouTube
from pyrogram import Client, filters

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Client

@app.on_message(filters.command("Dl"))
def download_video(client, message):
    try:
        # Extract URL from the command
        if len(message.text.split(" ", 1)) < 2:
            message.reply("Please provide a valid YouTube URL after the /Dl command.")
            return
        
        url = message.text.split(" ", 1)[1]  # Gets the part after "/Dl "
        
        logging.info(f"Received URL: {url}")
        logging.info("Generating OAuth token, please complete the browser login...")

        # Attempt to download video using Pytubefix
        yt = YouTube(
            url,
            use_oauth=True,
            allow_oauth_cache=True  # Allow OAuth to be cached
        )

        # Check if OAuth token file is created
        oauth_path = os.path.expanduser("~/.cache/pytubefix/oauth_token.json")
        if os.path.exists(oauth_path):
            logging.info(f"OAuth token saved successfully at {oauth_path}")
        else:
            logging.warning("OAuth token was not saved! Please ensure the OAuth process is completed properly.")

        logging.info("Video download started...")

        # Download the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path="~/downloads")  # Adjust the path if needed

        # Sending the video back to Telegram
        video_path = os.path.join(os.path.expanduser("~"), "downloads", video_stream.default_filename)
        logging.info(f"Download completed successfully! Sending the video...")

        message.reply_video(video=open(video_path, 'rb'))  # Adjust the path if needed

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        message.reply(f"An error occurred: {e}")


