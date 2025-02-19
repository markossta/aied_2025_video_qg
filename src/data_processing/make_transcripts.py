import os
import torch
import whisper


# folders (change khan to teded if you want to calculate transcripts for teded)
video_folders = ['/data/learningq_videos/downloaded_khan/']  # input
transcript_folders = ['/data/learningq_videos/transcripts_khan/']  # output

print("load whisper model, cuda:", torch.cuda.is_available())
model = whisper.load_model("base", device="cuda")

# create output folders if not exist
for folder in transcript_folders:
    os.makedirs(folder, exist_ok=True)

print("start transcribing")
for i, video_folder in enumerate(video_folders):
    transcript_folder = transcript_folders[i]
    # list all videos
    videos = [f for f in os.listdir(video_folder) if f.endswith(('.mp4'))]
    print("Amount videos:", len(videos))
    for i, video in enumerate(videos):
        video_path = os.path.join(video_folder, video)
        # getting transcript
        transcript_path = os.path.join(transcript_folder, video.split('.')[0] + ".txt")
        print("Start calculating transcript", i+1, "of", len(videos))
        if os.path.exists(transcript_path):
            print("Exists already:", transcript_path)
            continue
        try:
            result = model.transcribe(video_path)

            # storing as txt file
            with open(transcript_path, "w") as f:
                print("Stored transcript for video:", transcript_path)
                f.write(result["text"])
        except:
                print("Cant create transcript, store empty file!")
                with open(transcript_path, "w") as f:
                    print("Stored transcript for video:", transcript_path)
                    f.write('')


print("Creating transcripts done!")
