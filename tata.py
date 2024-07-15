import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import VideoFileClip, ImageClip
from moviepy.video.fx.all import resize

# Function to get filename from JSON data
def get_filename_from_data(data_json):
    path = data_json.get('file_path', None)
    if path and os.path.isfile(path):
        return path
    return None

# Function to convert bytes to human-readable format
def humanbytes(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1048576:
        return f"{size / 1024:.2f} KB"
    elif size < 1073741824:
        return f"{size / 1048576:.2f} MB"
    else:
        return f"{size / 1073741824:.2f} GB"

# Function to add a custom thumbnail
def add_thumbnail(video_file, thumbnail_file, output_file):
    clip = VideoFileClip(video_file)
    thumbnail = ImageClip(thumbnail_file)
    thumbnail = thumbnail.set_duration(clip.duration)
    video = clip.set_duration(thumbnail.duration)
    video = video.set_audio(clip.audio)
    thumbnail = thumbnail.set_duration(video.duration)
    thumbnail = thumbnail.resize(height=video.h)  # Resize thumbnail to match video height
    final_clip = video.set_thumbnail(thumbnail)
    final_clip.write_videofile(output_file, codec='libx264')

# Function to download playback and handle multi-audio selection and video quality
async def download_playback_catchup(channel, date, data_json, app, message):
    filename = get_filename_from_data(data_json)
    if filename is None:
        await message.reply("Error: filename is None")
        return
    
    if not os.path.isfile(filename):
        await message.reply(f"Error: File {filename} does not exist")
        return
    
    size = humanbytes(os.path.getsize(filename))
    
    # Fetch available qualities and audio tracks
    video_url = data_json.get('video_url', None)
    audio_urls = data_json.get('audio_urls', [])
    available_qualities = data_json.get('video_qualities', [])
    
    await message.reply(f"Video Size: {size}")
    await message.reply(f"Available Qualities: {', '.join(available_qualities)}")
    await message.reply(f"Available Audio Tracks: {', '.join([url.split('/')[-1] for url in audio_urls])}")

    # Ask user for quality and audio selection
    await message.reply("Please reply with the video quality and audio track you want to download (format: quality,audio_track).")
    
    # Collect user response
    user_response = await app.listen(message.chat.id, filters.text, timeout=30)
    quality, audio_choice = user_response.text.split(',')
    
    if quality not in available_qualities:
        await message.reply(f"Error: Selected quality '{quality}' is not available")
        return
    
    if audio_choice not in [url.split('/')[-1] for url in audio_urls]:
        await message.reply(f"Error: Selected audio track '{audio_choice}' is not available")
        return
    
    # Download the selected audio
    audio_url = [url for url in audio_urls if audio_choice in url][0]
    au
