from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import pandas as pd

source_folder = r'youtube_videos\baggage'
dest_folder = r'GMS\baggage_handling'

df = pd.read_csv('utils\dataset.csv')

source_filename = []
des_filename = []
start = []
end = []

for name, values in df['filename'].iteritems():
    source_filename.append(values)

for name, values in df['start'].iteritems():
    start.append(values)

for name, values in df['end'].iteritems():
    end.append(values)

for name, values in df['finalname'].iteritems():
    des_filename.append(values)

for i in range(len(source_filename)):
    ffmpeg_extract_subclip(os.path.join(source_folder, source_filename[i]+".mp4"),
                       start[i], end[i],
                       targetname=os.path.join(dest_folder, des_filename[i]+".mp4"))
