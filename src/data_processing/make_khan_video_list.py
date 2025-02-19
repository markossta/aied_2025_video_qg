import json


with open("/data/learningQ/khan/predicted_video_questions", "r") as f:  # file necessary from learningQ
    json_file = json.load(f)
    l = list(json_file.keys())
    with open("./yt_khan_links.txt", "w") as yt_list:
        for key in l:
            # create download list
            yt_link = f'youtube.com/watch?v={key}'
            print("write: ", yt_link)
            yt_list.write(yt_link + '\n')
