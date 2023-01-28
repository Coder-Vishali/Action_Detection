import os
import cv2
import pafy
from moviepy.editor import *

image_height, image_width = 64, 64

##################################################
# Function to Download YouTube Videos:
##################################################

# Let us start by testing on some YouTube videos. This function will
# use pafy library to download any youtube video and return its title. We just need to pass the URL.

def download_youtube_videos(youtube_video_url, output_directory):
    # Creating a Video object which includes useful information regarding the youtube video.
    video = pafy.new(youtube_video_url)

    # Getting the best available quality object for the youtube video.
    video_best = video.getbest()

    # Constructing the Output File Path
    output_file_path = f'{output_directory}/{video.title}.mp4'

    # Downloading the youtube video at the best available quality.
    video_best.download(filepath = output_file_path, quiet = True)

    # Returning Video Title
    return video.title

################################
# Download a Test Video:
################################
# Creating The Output directories if it does not exist
output_directory = 'youtube_videos'
os.makedirs(output_directory, exist_ok = True)

# Downloading a YouTube Video
video_title = download_youtube_videos('https://www.youtube.com/watch?v=dJIp2c72PSc', output_directory)