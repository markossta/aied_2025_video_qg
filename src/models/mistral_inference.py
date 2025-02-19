import os
import argparse
import json
from huggingface_hub import login
# mistral
from transformers import AutoModelForCausalLM, AutoTokenizer

# for seeds
import random
import torch
import torch.backends.cudnn as cudnn
import numpy as np
import logging
from PIL import Image


logger = logging.getLogger(__name__)


def get_video_list(dataset, set_name, folder):
    video_paths = []
    for videokey in dataset[set_name]:
        video_paths.append(folder + videokey + '.mp4')
    return video_paths
    

def set_seed(seed=1234):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    cudnn.benchmark = False
    cudnn.deterministic = True

def create_shot_string():
    return


def videos_iterator(name, dataname, video_paths, gt):
    # load model
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3",device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")

    # Iterate over each sample in the ground truth file
    index = 0
    questions = [
        "Create a question about the video content.",
        "Develop a question that tests comprehension of the video's main idea.",
        "Generate a question to assess the knowledge acquired from the video."
    ]
    video_answers = {}
    for video_path in video_paths:
        # change path to transcript
        video_path = video_path.replace("downloaded_khan", "transcripts_khan").replace("downloaded_teded", "transcripts_teded").replace(".mp4", ".txt")
        generation = []
        video_name = video_path.split('/')[-1][:-4]
        print('video_name:', video_name)
        # load transcript 
        print("video path:", video_path)
        with open(video_path, 'r') as file:
            data = file.read().replace('\n', '')
            transcript = " Transcript: " + data
        try:
            for question in questions:
                already_output = []
                for i in range(len(gt[video_name])):
                    extend = ''
                    if i > 0:
                        extend = "The following questions were already generated:"
                        for i, q in enumerate(already_output):
                            extend = extend + f" {i+1}. {q}"
                    # Run inference on the video and add the output to the list
                    query = question + extend + transcript
                    messages = [{"role": "user", "content": query}]
                    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
                    generated_ids = model.generate(encodeds, max_new_tokens=300, do_sample=False)
                    decoded = tokenizer.batch_decode(generated_ids)
                    print("Query: ",query)
                    print("\nResult:")
                    print(decoded[0].split('[/INST]', 1)[-1].strip().replace("</s>", ""))
                    generation.append({
                      "prompt": query,
                      "question": decoded[0].split('[/INST]', 1)[-1].strip().replace("</s>", "")
                       })
                    already_output.append(decoded[0].split('[/INST]', 1)[-1].strip().replace("</s>", ""))
                    if i == 0:
                       question = question.replace('a question', 'an additional question') 

        except Exception as e:
            print(f"Error processing video file '{video_name}': {e}")
        
        video_answers[video_path] = generation

    # store results
    with open(f'./zeroshot_7b_results_mistral_{name}_{dataname}_1234.txt', 'w') as f:
        json.dump(video_answers, f, indent = 4)


def main():
    login(token="")
    set_seed()
    khan_f = open('/data/learningq_questions/khan_datasplit.txt', 'r')
    khan_json = json.load(khan_f)
    teded_f = open('/data/learningq_questions/teded_datasplit.txt', 'r')
    teded_json = json.load(teded_f)
    video_paths_khan = get_video_list(khan_json, 'test', '/data/learningq_videos/downloaded_khan/')
    #print("Len khan is:", len(video_paths_khan))
    video_paths_teded = get_video_list(teded_json, 'test', '/data/learningq_videos/downloaded_teded/')
    #print("Len teded is:", len(video_paths_teded))
    khan_f.close()
    teded_f.close()
    # load ground truth questions
    khan_gt_f = open('/data/learningq_questions/khan_filtered_questions.txt')
    teded_gt_f = open('/data/learningq_questions/teded_filtered_questions.txt')
    khan_gt_json = json.load(khan_gt_f)
    teded_gt_json = json.load(teded_gt_f)
    khan_gt_f.close()
    teded_gt_f.close()
    #print("calculate for teded:")
    videos_iterator('teded', 'test', video_paths_teded, teded_gt_json)
    #print("calculate for khan:")
    videos_iterator('khan', 'test', video_paths_khan, khan_gt_json)


if __name__ == '__main__':
    main()
