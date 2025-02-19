import torch
import json
from videollava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from videollava.conversation import conv_templates, SeparatorStyle
from videollava.model.builder import load_pretrained_model
from videollava.utils import disable_torch_init
from videollava.mm_utils import tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria


# for seeds
import random
import torch.backends.cudnn as cudnn
import numpy as np


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


def videos_iterator(name, dataname, video_paths, gt):
    # load model
    addition_text = 'The question has not yet been generated.'
    model_path = 'LanguageBind/Video-LLaVA-7B'
    cache_dir = 'cache_dir'
    device = 'cuda'
    load_4bit, load_8bit = True, False
    model_name = get_model_name_from_path(model_path)
    tokenizer, model, processor, _ = load_pretrained_model(model_path, None, model_name, load_8bit, load_4bit, device=device, cache_dir=cache_dir)
    video_processor = processor['video']
    conv_mode = "llava_v1"
    conv = conv_templates[conv_mode].copy()
    roles = conv.roles
    # structure {"videokey": [{"prompt:" "", "question": ""}]}
    video_answers = {}
    # list of prompts
    inps  = [
        "Create a question about the video content.",
        "Develop a question that tests comprehension of the video's main idea.",
        "Generate a question to assess the knowledge acquired from the video."
    ]
    # get list of videos

    # iterate through each video to get an answer
    for video_path in video_paths:
        video_name = video_path.split('/')[-1][:-4]
        print("video:", video_path, video_name)
        generation = []
        # process video
        video_tensor = video_processor(video_path, return_tensors='pt')['pixel_values']
        if type(video_tensor) is list:
            tensor = [video.to(model.device, dtype=torch.float16) for video in video_tensor]
        else:
            tensor = video_tensor.to(model.device, dtype=torch.float16)
        for inp in inps:
            old_inp = inp
            inp = ' '.join([DEFAULT_IMAGE_TOKEN] * model.get_video_tower().config.num_frames) + '\n' + inp
            for i in range(len(gt[video_name])):
                conv = conv_templates[conv_mode].copy()
                print(f"{roles[1]}: {inp}")
                if i == 0:
                    conv.append_message(conv.roles[0], inp)
                else:
                    conv.append_message(conv.roles[0], inp.replace("a question", "an additional question"))
                conv.append_message(conv.roles[1], None)
                prompt = conv.get_prompt()
                input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()
                stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
                keywords = [stop_str]
                stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
                with torch.inference_mode():
                    use_cache = False
                    if i != 0:
                        use_cache = True
                    output_ids = model.generate(
                        input_ids,
                        images=tensor,
                        do_sample=True,
                        temperature=0.1,
                        max_new_tokens=1024,
                        use_cache=use_cache,
                        stopping_criteria=[stopping_criteria])
                    # store output
                    outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip().replace('</s>', '')
                    print("Prompt:", old_inp, "Answer:", outputs)
                    generation.append({
                        "prompt": old_inp,
                        "question": outputs
                    })
        video_answers[video_path] = generation
    # store results
    with open(f'./patched_zero_shot_seed_results_full_video_llava_{name}_{dataname}.txt', 'w') as f:
        json.dump(video_answers, f, indent = 4)


def main():
    disable_torch_init()
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
    print("calculate for khan:")
    videos_iterator('khan', 'test', video_paths_khan, khan_gt_json)
    print("calculate for teded:")
    videos_iterator('teded', 'test', video_paths_teded, teded_gt_json)


if __name__ == '__main__':
    main()

