from pytube import YouTube


with open('./yt_teded_links.txt', 'r') as f: # (for teded: yt_teded_links list from learningQ), change teded to khan if khan should be used
    lines = [line.rstrip() for line in f]
    #lines = lines
    restricted_videos = []
    for i, line in enumerate(lines):
        name = line.replace('https://www.youtube.com/watch?v=', '') + ".mp4"
        print(f"download {i}:", line)
        try:
            yt = YouTube(line).streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download(output_path='/data/learningq_videos/downloaded_teded', filename=name) # change teded to khan if khan videos should be downloaded
        except:
            print("Download error")
            restricted_videos.append(line)
    with open('./restricted_videos_teded.txt', 'w') as res: # change teded to khan if khan videos should be downlaoded
        res.write('\n'.join(restricted_videos))
