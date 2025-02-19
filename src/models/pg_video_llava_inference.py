import os
import argparse
import json
from tqdm import tqdm
from video_chatgpt.eval.model_utils import initialize_model, load_video
from video_chatgpt.inference import video_chatgpt_infer
from video_chatgpt.audio_transcript.transcribe import Transcriber
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
    # Initialize the model (fine-tune version)
    # Fine-tuned (CHANGE to your path for fine-tuned model files)
    model, vision_tower, tokenizer, image_processor, video_token_len = initialize_model('/data/PG-Video-LLaVA/weights/llava/llava-v1.5-13b',
                                                                                        '/data/PG-Video-LLaVA/checkpoints/mm_projector.bin')
    # Zero-Shot (CHANGE to your path for zero-shot model files)
    #model, vision_tower, tokenizer, image_processor, video_token_len = initialize_model('/data/PG-Video-LLaVA/weights/llava/llava-v1.5-13b',
    #                                                                                    '/data/PG-Video-LLaVA/weights/llava/llava-v1.5-13b/mm_projector.bin')
    frame_size = (image_processor.crop_size['height'], image_processor.crop_size['width'])
    conv_mode = 'pg-video-llava'

    # Transcript model
    if True:
        transcript_model = Transcriber()

    # Iterate over each sample in the ground truth file
    index = 0
    questions = [
        "Create a question about the video content.",
        "Develop a question that tests comprehension of the video's main idea.",
        "Generate a question to assess the knowledge acquired from the video."
    ]
    
    video_answers = {}
    for video_path in video_paths:
        generation = []
        video_name = video_path.split('/')[-1][:-4]
        print('video_name:', video_name)
        
        try:
            # Check if the video exists
            if os.path.exists(video_path):
                video_frames = load_video(video_path, shape=frame_size)
                
            try:
                transcript_text = transcript_model.transcribe_video(video_path=video_path)
            except Exception as e:
                print("Error transcript:", e)
                transcript_text = None
            #print(transcript_text)
            # Change code for ablation study (non transcript_text := only audio; black_frames := only frames)
            #transcript_text = None
            #black = [Image.new("RGB", (336, 336), (0, 0, 0)) for i in range(len(video_frames))]
            #print("black_frame", black_frame)
            for question in questions:
                already_output = []
                for i in range(len(gt[video_name])):
                    extend = ''
                    if i > 0:
                        extend = "The following questions were already generated:"
                        for i, q in enumerate(already_output):
                            extend = extend + f" {i}. {q}"
                # Run inference on the video and add the output to the list
                    # Replace video_frames to black if you want no frames
                    output = video_chatgpt_infer(video_frames, question + extend, conv_mode, model, vision_tower,
                                             tokenizer, image_processor, video_token_len, transcript_text)
                    print('prompt: ', question + extend + '\n\n')
                    print('question: ', output)
                    generation.append({
                      "prompt": question + '\n' + extend,
                      "question": output
                       })
                    already_output.append(output)
                    #logging.info(f"Video: {video_name}, {dataname}\n prompt: {question} {extend}\n question: {output}")
                    if i == 0:
                       question = question.replace('a question', 'an additional question') 

        except Exception as e:
            print(f"Error processing video file '{video_name}': {e}")
        
        video_answers[video_path] = generation

    # store results
    with open(f'./zero_shot_13b_results_pg_video_llava_{name}_{dataname}_1234.txt', 'w') as f:
        json.dump(video_answers, f, indent = 4)
s
    del model, vision_tower, tokenizer, image_processor, video_token_len
    torch.cuda.empty_cache()


def main():
    set_seed()
    khan_f = open('/data/learningq_questions/khan_datasplit.txt', 'r')
    khan_json = json.load(khan_f)
    teded_f = open('/data/learningq_questions/teded_datasplit.txt', 'r')
    teded_json = json.load(teded_f)
    video_paths_khan = get_video_list(khan_json, 'test', '/data/learningq_videos/downloaded_khan/')
    print("Len khan is:", len(video_paths_khan))
    video_paths_teded = get_video_list(teded_json, 'test', '/data/learningq_videos/downloaded_teded/')
    print("Len teded is:", len(video_paths_teded))
    khan_f.close()
    teded_f.close()
    # load ground truth questions
    khan_gt_f = open('/data/learningq_questions/khan_filtered_questions.txt')
    teded_gt_f = open('/data/learningq_questions/teded_filtered_questions.txt')
    khan_gt_json = json.load(khan_gt_f)
    teded_gt_json = json.load(teded_gt_f)
    khan_gt_f.close()
    teded_gt_f.close()
    print("calculate for teded:")
    videos_iterator('teded', 'test', video_paths_teded, teded_gt_json)
    print("calculate for khan:")
    videos_iterator('khan', 'test', video_paths_khan, khan_gt_json)

if __name__ == '__main__':
    main()
