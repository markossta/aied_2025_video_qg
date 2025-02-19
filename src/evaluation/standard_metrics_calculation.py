
from nltk.translate.bleu_score import sentence_bleu
from sacrebleu.metrics import BLEU
from bleu import list_bleu
from rouge_score import rouge_scorer
import bert_score
import pymeteor.pymeteor as pymeteor
import json
import os
import numpy as np


def calculate_rouge(scorer, reference, sentence):
    score = scorer.score(reference, sentence)
    return score['rougeL'].precision


def calculate_meteor(reference, sentence):
    score = pymeteor.meteor(reference, sentence)
    return score

def calculate_bert(reference, sentence):
    score, a, b = bert_score.score(sentence, reference, lang='en', model_type='roberta-large', rescale_with_baseline=True)
    return round(np.average(score.numpy()), 2)


def calculate(khan_results, teded_results, khan_gt, teded_gt):

    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    test_keys_khan = [key.split('/')[-1][:-4] for key in khan_results.keys()]
    test_keys_teded = [key.split('/')[-1][:-4] for key in teded_results.keys()]

    rouge1_khan = 0
    rouge1_teded = 0
    bert1_teded = 0
    bert1_khan = 0
    amount1_khan = 0
    amount1_teded = 0

    rouge2_khan = 0
    rouge2_teded = 0
    bert2_khan = 0
    bert2_teded = 0
    amount2_khan = 0
    amount2_teded = 0

    rouge3_khan = 0
    rouge3_teded = 0
    bert3_khan = 0
    bert3_teded = 0
    amount3_khan = 0
    amount3_teded = 0

    rouge_all_khan = 0
    rouge_all_teded = 0
    bert_all_khan = 0
    bert_all_teded = 0
    amount_all_khan = 0
    amount_all_teded = 0

    bert1_sentence_khan = []
    bert1_sentence_teded = []
    bert1_gt_khan = []
    bert1_gt_teded = []

    bert2_sentence_khan = []
    bert2_sentence_teded = []
    bert2_gt_khan = []
    bert2_gt_teded = []

    bert3_sentence_khan = []
    bert3_sentence_teded = []
    bert3_gt_khan = []
    bert3_gt_teded = []

    for video, gt_questions in teded_gt.items():
        if not video in test_keys_teded:
            continue
        questions = teded_results["/data/learningq_videos/downloaded_teded/" + video + '.mp4']
        for q in questions:
            rouge_1_values = []
            rouge_2_values = []
            rouge_3_values = []
            gt_sentences = []
            prompt = q['prompt']
            question = q['question']
            for gt_o in gt_questions:
                gt = gt_o['quiz_description']
                bleu_teded = calculate_bleu_new(gt, question)
                com_bleu_teded = calculate_4_cumulative_bleu(gt, question)
                rouge_teded = calculate_rouge(scorer, gt, question)
                bert_teded = calculate_bert(gt, question)
                amount_teded = 1
                gt_sentences.append(gt)
                if "Create a question." in prompt:
                    bert1_sentence_teded.append(question)
                    bert1_gt_teded.append(gt)
                    rouge1_teded += rouge_teded
                    bert1_teded += bert_teded
                    amount1_teded += amount_teded
                    bleu_1_values.append(bleu_teded)
                    com_bleu_1_values.append(com_bleu_teded)
                    rouge_1_values.append(rouge_teded)
                    meteor_1_values.append(meteor_teded)
                    bert1_teded += bert_teded

                elif "Create a question about the video content." in prompt:
                    bert2_sentence_teded.append(question)
                    bert2_gt_teded.append(gt)
                    rouge2_teded += rouge_teded
                    bert2_teded += bert_teded
                    amount2_teded += amount_teded
                    rouge_2_values.append(rouge_teded)
                else:
                    bert3_sentence_teded.append(question)
                    bert3_gt_teded.append(gt)
                    rouge3_teded += rouge_teded
                    bert3_teded += bert_teded
                    amount3_teded += amount_teded
                    rouge_3_values.append(rouge_teded)

                rouge_all_teded += rouge_teded
                bert_all_teded += bert_teded
                amount_all_teded += amount_teded 
            # calculate values on maximum basis
            if "Create a question." in prompt:
                rouge1_teded += max(rouge_1_values)
                bert1_sentence_teded.append(question)
                bert1_gt_teded.append(gt_sentences)
                amount1_teded += 1

                rouge_all_teded += max(rouge_1_values)
                amount_all_teded += 1
            elif "Create a question about the video content." in prompt:
                rouge2_teded += max(rouge_2_values)
                bert2_sentence_teded.append(question)
                bert2_gt_teded.append(gt_sentences)
                amount2_teded += 1

                rouge_all_teded += max(rouge_2_values)
                amount_all_teded += 1
            else:
                rouge3_teded += max(rouge_3_values)
                bert3_sentence_teded.append(question)
                bert3_gt_teded.append(gt_sentences)
                amount3_teded += 1

                rouge_all_teded += max(rouge_3_values)
                amount_all_teded += 1
        
    print("length:", len(bert1_gt_teded))
    print("Caluclated teded BertScore1:")
    bert1_teded = calculate_bert(bert1_gt_teded, bert1_sentence_teded)
    print("Caluclated teded BertScore2:")
    bert2_teded = calculate_bert(bert2_gt_teded, bert2_sentence_teded)
    print("Sentences original:", bert2_gt_teded)
    print()
    print("Created sentences:", bert2_sentence_teded)
    print("Len sentences:", len(bert2_gt_teded), len(bert2_sentence_teded))
    print("result:", bert2_teded)
    print("Caluclated teded BertScore3:")
    bert3_teded = calculate_bert(bert3_gt_teded, bert3_sentence_teded)
    print("Caluclated teded BertScore_all:")
    bert_all_teded = round((bert1_teded + bert2_teded + bert3_teded) / 3, 2)
    print("teded done")
    #return
    for video, gt_questions in khan_gt.items():
        if not video in test_keys_khan:
            print("is not")
            continue
        questions = khan_results["/data/learningq_videos/downloaded_khan/" + video + ".mp4"]
        for q in questions:
            rouge_1_values = []
            rouge_2_values = []
            rouge_3_values = []
            gt_sentences = []
            prompt = q['prompt']
            question = q['question']
            for gt in gt_questions:
                rouge_khan = calculate_rouge(scorer, gt, question)
                bert_khan = calculate_bert(gt, question)
                amount_khan = 1
        
                gt_sentences.append(gt)
                if "Create a question." in prompt:
                    bert1_sentence_khan.append(question)
                    bert1_gt_khan.append(gt)
                    rouge1_khan += rouge_khan
                    bert1_khan += bert_khan
                    amount1_khan += amount_khan
                    rouge_1_values.append(rouge_khan)
                    meteor_1_values.append(meteor_khan)
                    bert1_khan += bert_khan

                elif "Create a question about the video content." in prompt:
                    bert2_sentence_khan.append(question)
                    bert2_gt_khan.append(gt)
                    rouge2_khan += rouge_khan
                    bert2_khan += bert_khan
                    amount2_khan += amount_khan
                    rouge_2_values.append(rouge_khan)
                    meteor_2_values.append(meteor_khan)
                else:
                    bert3_sentence_khan.append(question)
                    bert3_gt_khan.append(gt)
                    rouge3_khan += rouge_khan
                    bert3_khan += bert_khan
                    amount3_khan += amount_khan
                    bleu_3_values.append(bleu_khan)
                    com_bleu_3_values.append(com_bleu_khan)
                    rouge_3_values.append(rouge_khan)
                    meteor_3_values.append(meteor_khan)

                rouge_all_khan += rouge_khan
                amount_all_khan += amount_khan
                bert_all_khan += bert_khan     
            # calculate values on maximum basis
            if "Create a question." in prompt:
                rouge1_khan += max(rouge_1_values)
                bert1_sentence_khan.append(question)
                bert1_gt_khan.append(gt_sentences)
                amount1_khan += 1

                rouge_all_khan += max(rouge_1_values)
                amount_all_khan += 1
            elif "Create a question about the video content." in prompt:
                rouge2_khan += max(rouge_2_values)
                meteor2_khan += max(meteor_2_values)
                bert2_sentence_khan.append(question)
                bert2_gt_khan.append(gt_sentences)
                amount2_khan += 1

                bleu_all_khan += max(bleu_2_values)
                com_bleu_all_khan += max(com_bleu_2_values)
                rouge_all_khan += max(rouge_2_values)
                meteor_all_khan += max(meteor_2_values)
                amount_all_khan += 1
            else:
                bleu3_khan += max(bleu_3_values)
                com_bleu3_khan += max(com_bleu_3_values)
                rouge3_khan += max(rouge_3_values)
                meteor3_khan += max(meteor_3_values)
                bert3_sentence_khan.append(question)
                bert3_gt_khan.append(gt_sentences)
                amount3_khan += 1

                bleu_all_khan += max(bleu_3_values)
                com_bleu_all_khan += max(com_bleu_3_values)
                rouge_all_khan += max(rouge_3_values)
                meteor_all_khan += max(meteor_3_values)
                amount_all_khan += 1

    print("Caluclated khan BertScore1:")
    bert1_khan = calculate_bert(bert1_gt_khan, bert1_sentence_khan)
    print("Caluclated khan BertScore2:")
    bert2_khan = calculate_bert(bert2_gt_khan, bert2_sentence_khan)
    print("khan score bert2:", bert2_khan)
    print("Caluclated khan BertScore3:")
    bert3_khan = calculate_bert(bert3_gt_khan, bert3_sentence_khan)
    print("Caluclated khan BertScore_all:")
    bert_all_khan = round((bert1_khan + bert2_khan + bert3_khan) / 3, 2)
    
    print("khan  done")
    print("Khan:")
    print("ROUGE:", round(rouge_all_khan / max(amount_all_khan, 1), 2))
    print("TEDED:")
    print("ROUGE:", round(rouge_all_teded / max(amount_all_teded,1), 2))
    print("BOTH:") 
    #print("ROUGE2:", round((rouge2_teded + rouge2_khan) / max((amount2_teded + amount2_khan),1), 2), "BERT2:", round((bert2_teded + bert2_khan) / 2, 2))
    print("ROUGE1:", round((rouge1_teded + rouge1_khan) / max((amount1_teded + amount1_khan),1), 2), "BERT1:", round((bert1_teded + bert1_khan) / 2, 2),
          "\n", "ROUGE2:", round((rouge2_teded + rouge2_khan) / max((amount2_teded + amount2_khan),1), 2), "BERT2:", round((bert2_teded + bert2_khan) / 2, 2), 
          "\n", "ROUGE3:", round((rouge3_teded + rouge3_khan) / max((amount3_teded + amount3_khan),1), 2), "BERT3:", round((bert3_teded + bert3_khan) / 2, 2),
          "\n", "ROUGE:", round((rouge_all_teded + rouge_all_khan) / max((amount_all_teded + amount_all_khan),1), 2), "BERT:", round((bert_all_teded + bert_all_khan) / 2, 2))


# CHOOSE files
# Video-LLaVA (zero-shot)
khan_results = json.load(open('/data/models_output/zero_shot_seed_results_full_video_llava_khan_test.txt', 'r'))
teded_results =json.load(open('/data/models_output/zero_shot_seed_results_full_video_llava_teded_test.txt', 'r'))

# PG-Video-LLaVA (zero-shot, fine-tuned, frames only, audio only)
#khan_results = json.load(open('/data/models_output/patched_new_prompts_store_zeroshot_13b_results_pg_video_llava_khan_test_1234.txt'', 'r'))
#teded_results = json.load(open('/data/models_output/patched_new_prompts_store_zeroshot_13b_results_pg_video_llava_teded_test_1234.txt'', 'r'))
#khan_results = json.load(open('/data/models_output/patched_new_prompts_store_finetune_13b_results_pg_video_llava_khan_test_1234.txt', 'r'))
#teded_results = json.load(open('/data/models_output/patched_new_prompts_store_finetune_13b_results_pg_video_llava_teded_test_1234.txt', 'r'))
#khan_results = json.load(open('/data/models_output/patched_frames_only_new_prompts_store_finetune_13b_results_pg_video_llava_khan_test_1234.txt', 'r'))
#teded_results = json.load(open('/data/models_output/patched_frames_only_new_prompts_store_finetune_13b_results_pg_video_llava_teded_test_1234.txt', 'r'))
#khan_results = json.load(open('/data/models_output/patched_audio_only_new_prompts_store_finetune_13b_results_pg_video_llava_khan_test_1234.txt' , 'r'))
#teded_results = json.load(open('/data/models_output/patched_audio_only_new_prompts_store_finetune_13b_results_pg_video_llava_teded_test_1234.txt', 'r'))

# Video-LLaMA (zero-shot, fine-tuned, frames only, audio only)
#khan_results = json.load(open('/data/models_output/patched_new_prompts_store_zeroshot_seed_video_llama_13B_khan_test.txt', 'r'))
#teded_results = json.load(open('/data/models_output/patched_new_prompts_store_zeroshot_seed_video_llama_13B_teded_test.txt', 'r'))
#khan_results = json.load(open('/data/models_output/patched_new_prompts_store_finetuned_seed_video_llama_13B_khan_test.txt', 'r'))
#teded_results = json.load(open('/data/models_output/patched_new_prompts_store_finetuned_seed_video_llama_13B_teded_test.txt', 'r'))
#khan_results = json.load(open('/data/models_output/patched_frames_only_new_prompts_store_finetune_seed_video_llama_13B_khan_test.txt', 'r'))
#teded_results = json.load(open('/data/models_output/patched_frames_only_new_prompts_store_finetune_seed_video_llama_13B_teded_test.txt', 'r'))
#khan_results = json.load(open('/data/models_output/patched_audio_only_new_prompts_store_finetune_seed_video_llama_13B_khan_test.txt', 'r'))
#teded_results = json.load(open('/data/models_output/patched_audio_only_new_prompts_store_finetune_seed_video_llama_13B_teded_test.txt', 'r'))

# Mistral-7B (instruct version, zero-shot)
#khan_results = json.load(open('data/models_output/patched_new_prompts_store_zeroshot_7b_results_mistral_khan_test_1234.txt', 'r'))
#teded_results = json.load(open('/data/models_output/patched_new_prompts_store_zeroshot_7b_results_mistral_teded_test_1234.txt', 'r'))  

khan_gt = json.load(open('/data/learningq_questions/khan_filtered_questions.txt', 'r'))
teded_gt = json.load(open('data/learningq_questions/teded_filtered_questions.txt', 'r'))
calculate(khan_results, teded_results, khan_gt, teded_gt)
#print("no frame")
 
