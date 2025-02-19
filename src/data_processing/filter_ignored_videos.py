import json
from os import listdir
from os.path import isfile, join


def load_files(path_list):
    complete_list = []
    for path in path_list:
        with open(path, 'r') as f:
            lines = f.read().splitlines()
            complete_list += lines
    complete_list = [value.replace('https://www.youtube.com/watch?v=', '') for value in complete_list]
    complete_list = [value.replace('youtube.com/watch?v=', '') for value in complete_list]
    return complete_list
            

def filter_teded(ignored_list):
    teded_path = './learningQ/teded/crawled_data/videos'
    information_paths= [f for f in listdir(teded_path) if isfile(join(teded_path, f))]
    complete_jsonl = {}
    amount_before = 0
    amount_after = 0
    amount_videos = 0
    missing_questions = 0
    ignored_video = 0
    without_question = 0
    amount_multiple = 0
    amount_open = 0
    print("Amount files:", len(information_paths))
    for information_path in information_paths:
        with open(teded_path + '/' + information_path, 'r') as teded:
            new_teded = {}
            teded_json = json.load(teded)
            ted_ed_keys = list(teded_json.keys())
            # skip if video has no tasks
            if not "quizzes" in ted_ed_keys:
                missing_questions += 1
                continue
            video_name= teded_json["video_youtube_link"].replace('https://www.youtube.com/watch?v=', '')
            quizzes = teded_json["quizzes"]
            questions = []
            for quiz in quizzes:
                amount_before += 1
                if not "?" in quiz["quiz_description"]:
                    without_question += 1
                    continue
                else:
                    if not video_name in ignored_list:
                        if quiz["question_type"] == "multiple-choices":
                            amount_multiple += 1
                        else:
                            amount_open += 1
                        amount_after += 1
                        questions.append(quiz)
            if video_name in ignored_list:
                ignored_video += 1
                continue
            complete_jsonl[video_name] = questions
            amount_videos += 1

    print("Amount videos:", len(information_paths), "Amount after videos:", amount_videos, "Amount before:", amount_before, "Amount after:", amount_after, "Avg before:", amount_before / amount_videos, "Avg after:", amount_after / amount_videos)
    print("Missing questions in videos:", missing_questions, "Ignored Videos:", ignored_video, "Task without question:", without_question)
    print("amount open:", amount_open, "amount multiple:", amount_multiple)
    with open ('./teded_filtered_questions.txt', 'w') as filtered:
        json.dump(complete_jsonl, filtered, indent=4)



def filter_khan(ignored_list):
    khan_path = '/data/learningQ/khan/predicted_video_questions'
    with open(khan_path, 'r') as khan:
        new_khan = {}
        khan_json = json.load(khan)
        print("Keys before filtering khan:", len(list(khan_json.keys())))
        amount_before = 0
        amount_after = 0
        for key, value in khan_json.items():
            amount_before += len(value)
            if key in ignored_list:
                continue
            else:
                # filter questions
                value = [v for v in value if "?" in v]
                if (len(value)):
                    amount_after += len(value)
                    new_khan[key] = value
        print("Keys after filtering khan:", len(list(new_khan.keys())))
        print("Amount before:", amount_before, "Amount after:", amount_after, "Avg before:", amount_before / len(list(khan_json.keys())), "Avg after:", amount_after / len(list(new_khan.keys())))
        with open ('./khan_filtered_questions.txt', 'w') as filtered:
            json.dump(new_khan, filtered, indent=4)



path_list = ['./restricted_videos_khan.txt']

khan_list = load_files(path_list)
print("count missing videos:")
print("Missing videos khan:", len(khan_list))
teded_list = load_files(['./restricted_videos_teded.txt'])
print("Missing videos teded:", len(set(teded_list)))
print()
print("Remove questions from missing videos:")
print("Remaining questions from khan:")
filter_khan(khan_list)
print("Remaining tasks from teded:")
filter_teded(teded_list)
print("amount ignored:", len(teded_list))
print()


