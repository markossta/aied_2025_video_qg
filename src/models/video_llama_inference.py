import argparse
import os
import random
import json

import numpy as np
import torch
import torch.backends.cudnn as cudnn

from video_llama.common.config import Config
from video_llama.common.dist_utils import get_rank
from video_llama.common.registry import registry
from video_llama.conversation.conversation_video import Chat, Conversation, default_conversation,SeparatorStyle,conv_llava_llama_2
from PIL import Image

# imports modules for registration
from video_llama.datasets.builders import *
from video_llama.models import *
from video_llama.processors import *
from video_llama.runners import *
from video_llama.tasks import *
import decord
decord.bridge.set_bridge('torch')


def parse_args():
    parser = argparse.ArgumentParser()
    # load config file for with/ without audio processing
    parser.add_argument("--cfg-path", default='eval_configs/video_llama_eval_withaudio.yaml', help="path to configuration file.")
    #parser.add_argument("--cfg-path", default='eval_configs/video_llama_eval_only_vl.yaml', help="path to configuration file.")
    parser.add_argument("--gpu-id", type=int, default=0, help="specify the gpu to load the model.")
    parser.add_argument("--model_type", type=str, default='vicuna', help="The type of LLM")
    parser.add_argument(
        "--options",
        nargs="+",
        help="override some settings in the used config, the key-value pair "
        "in xxx=yyy format will be merged into config file (deprecate), "
        "change to --cfg-options instead.",
    )
    args = parser.parse_args()
    return args


def setup_seeds(seed=1234):

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    cudnn.benchmark = False
    cudnn.deterministic = True

def videos_iterator(name, dataname, video_paths, gt, args):
    # Initialize the model
    print("init model")
    cfg = Config(args)

    model_config = cfg.model_cfg
    model_config.device_8bit = args.gpu_id
    model_cls = registry.get_model_class(model_config.arch)
    model = model_cls.from_config(model_config).to('cuda:{}'.format(args.gpu_id))
    model.eval()
    vis_processor_cfg = cfg.datasets_cfg.webvid.vis_processor.train
    vis_processor = registry.get_processor_class(vis_processor_cfg.name).from_config(vis_processor_cfg)
    chat = Chat(model, vis_processor, device='cuda:{}'.format(args.gpu_id))

    # Iterate over each sample in the ground truth file
    index = 0
    questions = [
        "Create a question about the video content.",
        "Develop a question that tests comprehension of the video's main idea.",
        "Generate a question to assess the knowledge acquired from the video."
    ]
    video_answers = {}
    for i, video_path in enumerate(video_paths):
        print("current video:", f"{i} of {len(video_paths)}", video_path)
        chat_state = conv_llava_llama_2.copy()
        chat_state.messages = []
        chat_state.system = "You are able to understand the visual content that the user provides. Follow the instructions carefully and explain your answers in detail."
        img_list = []
        chat = Chat(model, vis_processor, device='cuda:{}'.format(args.gpu_id))
        generation = []
        video_name = video_path.split('/')[-1][:-4]
        print('video_name:', video_name, "path:", video_path)
        try:
            # CHOOSE between video with or without audio (frames only)
            #llm_message = chat.upload_video_without_audio(video_path, chat_state, img_list)
            llm_message = chat.upload_video(video_path, chat_state, img_list)
            print("Upload message:", llm_message)
            old_chat_state = chat_state.copy()
            #print(img_list)
            #img_list = [Image.new("RGB", (336, 336), (0, 0, 0)) for i in range(len(img_list))] # black frames
            for question in questions:
                chat_state = old_chat_state.copy()
                for i in range(len(gt[video_name])):
                    #img_list = [] # remove images
                    # Run inference on the video and add the output to the list
                    chat.ask(question, chat_state)
                    output = chat.answer(conv=chat_state,
                                         img_list=img_list,
                                         max_new_tokens=300,
                                         max_length=5000)[0]
                    print('question: ', question)
                    print('pred_output: ', output)
                    print()
                    if not output:
                        output = ""
                    generation.append({
                        "prompt": question,
                        "question": output
                        })
                    if i == 0:
                        question = question.replace("a question", "an additional question")

        except Exception as e:
            print(f"Error processing video file '{video_name}': {e}")

        video_answers[video_path] = generation

    # store results
    with open(f'./zeroshot_video_llama_13B_{name}_{dataname}.txt', 'w') as f:
        json.dump(video_answers, f, indent = 4)

    del chat, vis_processor, model
    torch.cuda.empty_cache()

# ========================================
#             Get Ground Truth Videos
# ========================================
def get_video_list(dataset, set_name, folder):
    video_paths = []
    for videokey in dataset[set_name]:
        video_paths.append(folder + videokey + '.mp4')
    return video_paths
    

# ========================================
#             Model Initialization
# ========================================
setup_seeds()
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
print('Initializing Chat')
args = parse_args()
print("calculate for khan:")
videos_iterator('khan', 'test', video_paths_khan, khan_gt_json, args)
print("calculate for teded:")
print(video_paths_teded)
videos_iterator('teded', 'test', video_paths_teded, teded_gt_json, args)

