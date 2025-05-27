import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"

from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import os
import math

# === CONFIGURATION ===
mp3_folder = "D:\OG\Scrape_TSS\gtts"          # Folder for MP3 files
text_folder = "D:\OG\Scrape_TSS\stories_text" # Folder for text files
thumb_folder = "thumb"       # Folder for thumbnail images
bg_folder = "bg"             # Folder for background images

output_video = "output.mp4"
thumbnail_path = os.path.join(thumb_folder, "1s.jpg")
font_path = "C:/Windows/Fonts/Latha.ttf"  # Update with Tamil font path on your system
font_size = 36
lines_per_screen = 2

# === LOAD DATA ===
# Title from mp3 filename
mp3_filename = "111_16_6_20250519_0415_கீர்த்திகாவின்_கல்யாண_வாழ்க்கை.mp3"  # Replace with actual MP3 file name if necessary
mp3_path = os.path.join(mp3_folder, mp3_filename)
title = os.path.basename(mp3_path).split('.')[0].replace("_", " ")

base_name = os.path.splitext(mp3_filename)[0]
# Read lines from story text file
text_filename = f"{base_name}.txt"  # Replace with actual text file name
text_path = os.path.join(text_folder, text_filename)
with open(text_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Estimate how long each screen shows
audio_clip = AudioFileClip(mp3_path)
audio_duration = audio_clip.duration
total_screens = math.ceil(len(lines) / lines_per_screen)
seconds_per_screen = audio_duration / total_screens

# === FUNCTION: Create a screen clip ===
def create_text_clip(text_lines, duration):
    text = "\n".join(text_lines)
    txt_clip = TextClip(text, fontsize=font_size, font=font_path, color='white', size=(1080, None), method='label')
    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(duration)
    return txt_clip

# === BACKGROUND IMAGE ===
bg_filename = "1c.jpg"  # Replace with actual background image name
bg_path = os.path.join(bg_folder, bg_filename)
bg = ImageClip(bg_path).resize(height=1080).set_duration(audio_duration)

# === TITLE (1st line of video) ===
title_clip = TextClip(title, fontsize=font_size + 10, font=font_path, color='yellow', method='label', size=(1080, None))
title_clip = title_clip.set_position(('center', 50)).set_duration(audio_duration)

# === TEXT SCENES ===
text_clips = []
for i in range(0, len(lines), lines_per_screen):
    segment = lines[i:i+lines_per_screen]
    text_clips.append(create_text_clip(segment, seconds_per_screen))

text_overlay = concatenate_videoclips(text_clips).set_start(0)

# === FINAL VIDEO ===
final_video = CompositeVideoClip([bg, title_clip, text_overlay])
final_video = final_video.set_audio(audio_clip)

# Remove extension


# Split by underscores
parts = base_name.split('_')

# Keep only Tamil name part (after 5th underscore)
tamil_name_parts = parts[5:]  # index 0 to 4 are metadata
first_number = parts[0]       # 108

# Create new filename
output_filename = '_'.join(tamil_name_parts) + f'_{first_number}.mp4'

print(output_filename)

# === EXPORT VIDEO ===
final_video.write_videofile(
    output_filename,
    fps=6,
    codec='libx264',
    audio_codec='aac',
    ffmpeg_params=['-threads', '16'], preset='ultrafast'
)

#final_video.write_videofile(output_filename, fps=12, threads=16)

# === CREATE THUMBNAIL ===
thumb_image_path = os.path.join(thumb_folder, "thumbnail.jpg")
thumb = Image.open(thumbnail_path).resize((512, 512))
draw = ImageDraw.Draw(thumb)
font = ImageFont.truetype(font_path, 24)
draw.text((10, 10), title, font=font, fill="yellow")
thumb.save(thumb_image_path)

print("✅ Video & thumbnail created successfully.")
