import json


def get_video_list(dataset, set_name, folder):
    video_paths = []
    for videokey in dataset[set_name]:
        video_paths.append(videokey)
    return video_paths


def convert_to_videollava(teded, khan, train_teded, train_khan):
    results = []
    counter = 0
    # teded
    for key in teded:
        if key not in train_teded:
            continue
        else:
            for q in teded[key]:
                result = {"id": counter,
                          "video": f"teded/{key}.mp4",
                          "conversations": [
                                            {"from": "human",
                                             "value": "<video>\nCreate a question about the video content."},
                                            {"from": "gpt",
                                             "value": q["quiz_description"]}
                                           ]
                        }
                results.append(result)
                counter += 1
    # khan
    for key in khan:
        if key not in train_khan:
            continue
        else:
            for q in khan[key]:
                result = {"id": counter,
                          "video": f"khan/{key}.mp4",
                          "conversations": [
                                            {"from": "human",
                                             "value": "<video>\nCreate a question about the video content."},
                                            {"from": "gpt",
                                             "value": q}
                                           ]
                        }
                results.append(result)
                counter += 1
    with open(f'./videollava_train_data.json', 'w') as f:
        json.dump(results, f, indent = 4)


def main():
    khan_f = open('./khan_datasplit.txt', 'r')
    train_khan = json.load(khan_f)["train"]
    teded_f = open('./teded_datasplit.txt', 'r')
    train_teded = json.load(teded_f)["train"]
    khan_f.close()
    teded_f.close()
    
    khan_gt_f = open('./khan_filtered_questions.txt')
    teded_gt_f = open('./teded_filtered_questions.txt')
    khan_gt_json = json.load(khan_gt_f)
    teded_gt_json = json.load(teded_gt_f)
    khan_gt_f.close()
    teded_gt_f.close()

    
    convert_to_videollava(teded_gt_json, khan_gt_json, train_teded, train_khan)




if __name__ == '__main__':
    main()
