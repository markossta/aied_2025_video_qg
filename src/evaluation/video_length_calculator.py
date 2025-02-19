import cv2
import datetime
from os import listdir
from os.path import isfile, join
import subprocess
import json

khan_folder = '/data/learningq_videos/downloaded_khan/' 
teded_folder = '/data/learningq_videos/downloaded_teded/'
khan_files = [f for f in listdir(khan_folder) if isfile(join(khan_folder, f))]
teded_files = [f for f in listdir(teded_folder) if isfile(join(teded_folder, f))]

# khan analysis
min_khan = 9999999999999999
average_khan = 0
max_khan = 0
all_khan = 0
for i, khan_file in enumerate(khan_files):
    print(f"Process video {i} of {len(khan_files)}")
    data = cv2.VideoCapture(khan_folder + khan_file)
    # count the number of frames 
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT) 
    fps = data.get(cv2.CAP_PROP_FPS) 
  
    # calculate duration of the video 
    seconds = round(frames / fps) 
    if seconds < min_khan:
        min_khan = seconds
    if seconds > max_khan:
        max_khan = seconds
    all_khan += seconds

average_khan = round(all_khan / len(khan_files)) 
print("Khan videos statistics:")
print("Min:", datetime.timedelta(seconds=min_khan), "Average:", datetime.timedelta(seconds=average_khan), "Max:", datetime.timedelta(seconds=max_khan))
print()

# teded analysis
min_teded = 999999999999999999
averaged_teded = 0
max_teded = 0
all_teded = 0
amount_neg = 0
for i, teded_file in enumerate(teded_files):
    print(f"Process video {i} of {len(teded_files)}")
    data = cv2.VideoCapture(teded_folder + teded_file)

    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)
    
    # calculate duration of the video
    if fps == 0:
        amount_neg += 1
        continue
    seconds = round(frames / fps)
    if seconds < min_teded: 
        min_teded = seconds
    if seconds > max_teded:
        max_teded = seconds
    all_teded += seconds

average_teded = round(all_teded / len(teded_files) - amount_neg)

print("Teded videos statistics:")
print("Min:", datetime.timedelta(seconds=min_teded), "Average:", datetime.timedelta(seconds=average_teded), "Max:", datetime.timedelta(seconds=max_teded))
print()

