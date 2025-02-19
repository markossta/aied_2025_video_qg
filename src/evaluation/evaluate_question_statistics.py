import json
import os
import textstat


def calc_flesch(question):
    score = textstat.flesch_reading_ease(question)
    #print("flesch score:", score)
    return score


def count_question_statements_empty(result_file):
    questions_1 = 0
    statements_1 = 0
    empty_1 = 0
    questions_2 = 0
    statements_2 = 0
    empty_2 = 0
    questions_3 = 0
    statements_3 = 0
    empty_3 = 0
    all_1 = 0
    all_2 = 0
    all_3 = 0
    question_form_1 = {"where": 0, "who": 0, "when": 0, "what": 0, "why": 0, "whose": 0, "whom": 0, "which": 0, "how": 0, "other": 0}
    question_form_2 = {"where": 0, "who": 0, "when": 0, "what": 0, "why": 0, "whose": 0, "whom": 0, "which": 0, "how": 0, "other": 0}
    question_form_3 = {"where": 0, "who": 0, "when": 0, "what": 0, "why": 0, "whose": 0, "whom": 0, "which": 0, "how": 0, "other": 0}
    question_form_all = {"where": 0, "who": 0, "when": 0, "what": 0, "why": 0, "whose": 0, "whom": 0, "which": 0, "how": 0, "other": 0}
    word_length_1 = 0
    min_length_1 = 9999999
    max_length_1 = 0
    word_length_2 = 0
    min_length_2 = 9999999
    max_length_2 = 0
    word_length_3 = 0
    min_length_3 = 9999999
    max_length_3 = 0
    word_length_all = 0
    min_length_all = 0
    max_length_all = 0
    readability_1 = 0
    readability_2 = 0
    readability_3 = 0
    readability_all = 0
    print("amount videos:", len(result_file))
    for key in result_file:
        values = result_file[key]
        for d in values:
            prompt = d["prompt"]
            value = d["question"]
            words = d["question"].lower().split(" ")
            if 'Create a question about the video content' in prompt or 'Create an additional question about the video content' in prompt:
                if not value:
                    empty_1 += 1
                elif "?" in value:
                    questions_1 += 1
                    for key in question_form_1:
                        if key in words or key == "other":
                            question_form_1[key] += 1
                            break
                    # sentence length
                    word_length_1 += len(words)
                    if min_length_1 > len(words):
                        min_length_1 = len(words)
                    if max_length_1 < len(words):
                        max_length_1 = len(words)
                    # readability
                    readability_1 += calc_flesch(value)
                else:
                    statements_1 += 1
                all_1 += 1
            elif 'Develop' in prompt:
                if not value:
                    empty_2 += 1
                elif "?" in value:
                    questions_2 += 1
                    for key in question_form_2:
                        if key in words or key == "other":
                            question_form_2[key] += 1
                            break
                    # sentence length
                    word_length_2 += len(words)
                    if min_length_2 > len(words): 
                        min_length_2 = len(words)
                    if max_length_2 < len(words):
                        max_length_2 = len(words)
                    # readability
                    readability_2 += calc_flesch(value)

                else:
                    statements_2 += 1
                all_2 += 1
            else:
                if not value:
                    empty_3 += 1
                elif "?" in value:
                    questions_3 += 1
                    for key in question_form_3:
                        if key in words or key == "other":
                            question_form_3[key] += 1
                            break
                    # sentence length
                    word_length_3 += len(words)
                    if min_length_3 > len(words): 
                        min_length_3 = len(words)
                    if max_length_3 < len(words):
                        max_length_3 = len(words)
                    # readability
                    readability_3 += calc_flesch(value)


                else:
                    statements_3 += 1
                all_3 += 1
    results = {"questions_1": questions_1, "statements_1": statements_1, "empty_1": empty_1, "all_1": all_1, "questions_2": questions_2, "statements_2": statements_2, "empty_2": empty_2, "all_2": all_2, 
               "questions_3": questions_3, "statements_3": statements_3, "empty_3": empty_3, "all_3": all_3, 
               "word_length_1": word_length_1, "min_length_1": min_length_1, "max_length_1": max_length_1, "readability_1": readability_1, 
               "word_length_2": word_length_2, "min_length_2": min_length_2, "max_length_2": max_length_2, "readability_2": readability_2,
               "word_length_3": word_length_3, "min_length_3": min_length_3, "max_length_3": max_length_3, "readability_3": readability_3}
    return results, [question_form_1, question_form_2, question_form_3]


def merged_results(khan, question_forms_khan, teded, question_forms_teded, model_name):
    if khan['all_1'] + teded['all_1'] != 0:
        questions_1 = (khan['questions_1'] + teded['questions_1']) / (khan['all_1'] + teded['all_1'])
        statements_1 = (khan['statements_1'] + teded['statements_1']) / (khan['all_1'] + teded['all_1'])
        empty_1 = (khan['empty_1'] + teded['empty_1']) / (khan['all_1'] + teded['all_1'])
        word_length_1 = (khan["word_length_1"] + teded["word_length_1"]) / (khan['questions_1'] + teded['questions_1'])
        min_length_1 = min([khan["min_length_1"], teded["min_length_1"]])
        max_length_1 = max([khan["max_length_1"], teded["max_length_1"]])
        readability_1 = (khan["readability_1"] + teded["readability_1"]) / (khan['questions_1'] + teded['questions_1'])

    else:
        questions_1 = 0.0
        statements_1 = 0.0
        empty_1 = 0.0
        word_length_1 = 0.0
        min_length_1 = 0.0
        max_length_1 = 0.0
        readability_1 = 0.0

    print("questions_1:", round(questions_1 * 100, 2), "statements_1:", round(statements_1 * 100, 2), "empty_1:", round(empty_1 * 100, 2), "word_length_1:", word_length_1,
          "min_length_1:", min_length_1, "max_length_1:", max_length_1, "readability_1:", round(readability_1,2))
    if khan['all_2'] + teded['all_2'] != 0:
        questions_2 = (khan['questions_2'] + teded['questions_2']) / (khan['all_2'] + teded['all_2'])
        statements_2 = (khan['statements_2'] + teded['statements_2']) / (khan['all_2'] + teded['all_2'])
        empty_2 = (khan['empty_2'] + teded['empty_2']) / (khan['all_2'] + teded['all_2'])
        word_length_2 = (khan["word_length_2"] + teded["word_length_2"]) / (khan['questions_2'] + teded['questions_2'])
        min_length_2 = min([khan["min_length_2"], teded["min_length_2"]])
        max_length_2 = max([khan["max_length_2"], teded["max_length_2"]])
        readability_2 = (khan["readability_2"] + teded["readability_2"]) / (khan['questions_2'] + teded['questions_2'])


    else:
        questions_2 = 0.0
        statements_2 = 0.0
        empty_2 = 0.0
        word_length_2 = 0.0
        min_length_2 = 0.0
        max_length_2 = 0.0
        readability_2 = 0.0

    print("questions_2:", round(questions_2 * 100, 2), "statements_2:", round(statements_2 * 100, 2), "empty_2:", round(empty_2 * 100, 2), "word_length_2:", word_length_2, 
          "min_length_2:", min_length_2, "max_length_2:", max_length_2, "readability_2:", round(readability_2,2))
    if khan['all_3'] + teded['all_3'] != 0:
        questions_3 = (khan['questions_3'] + teded['questions_3']) / (khan['all_3'] + teded['all_3'])
        statements_3 = (khan['statements_3'] + teded['statements_3']) / (khan['all_3'] + teded['all_3'])
        empty_3 = (khan['empty_3'] + teded['empty_3']) / (khan['all_3'] + teded['all_3'])
        word_length_3 = (khan["word_length_3"] + teded["word_length_3"]) / (khan['questions_3'] + teded['questions_3'])
        min_length_3 = min([khan["min_length_3"], teded["min_length_3"]])
        max_length_3 = max([khan["max_length_3"], teded["max_length_3"]])
        readability_3 = (khan["readability_3"] + teded["readability_3"]) / (khan['questions_3'] + teded['questions_3'])


    else:
        questions_3 = 0.0
        statements_3 = 0.0
        empty_3 = 0.0
        word_length_3 = 0.0
        min_length_3 = 0.0
        max_length_3 = 0.0
        readability_3 = 0.0

    print("questions_3:", round(questions_3 * 100, 2), "statements_3:", round(statements_3 * 100, 2), "empty_3:", round(empty_3 * 100, 2), "word_length_3:", word_length_3,
          "min_length_3:", min_length_3, "max_length_3:", max_length_3, "readability_3:", round(readability_3,2))
    if (khan['all_1'] + teded['all_1'] + khan['all_2'] + teded['all_2'] + khan['all_3'] + teded['all_3']) != 0:
        questions = (khan['questions_1'] + teded['questions_1'] + khan['questions_2'] + teded['questions_2'] + khan['questions_3'] + teded['questions_3']) / (khan['all_1'] + teded['all_1'] + khan['all_2'] + teded['all_2'] + khan['all_3'] + teded['all_3'])
        statements = (khan['statements_1'] + teded['statements_1'] + khan['statements_2'] + teded['statements_2'] + khan['statements_3'] + teded['statements_3']) / (khan['all_1'] + teded['all_1'] + khan['all_2'] + teded['all_2'] + khan['all_3'] + teded['all_3'])
        empty = (khan['empty_1'] + teded['empty_1'] + khan['empty_2'] + teded['empty_2'] + khan['empty_3'] + teded['empty_3']) / (khan['all_1'] + teded['all_1'] + khan['all_2'] + teded['all_2'] + khan['all_3'] + teded['all_3']) 
    else:
        questions = 0.0
        statements = 0.0
        empty = 0.0
    print("question:", round(questions * 100, 2), "statements:", round(statements * 100, 2), "empty:", round(empty * 100, 2), "word_length:", round((word_length_1 + word_length_2 + word_length_3) / 3, 2), 
          "min_length:", min([min_length_1, min_length_2, min_length_3]), "max_length:", max([max_length_1, max_length_2, max_length_3]), "readability:", round((readability_1 + readability_2 + readability_3) / 3, 2))
    # calculate questions
    question_forms = {"where": 0, "who": 0, "when": 0, "what": 0, "why": 0, "whose": 0, "whom": 0, "which": 0, "how": 0, "other": 0}
    complete_amount = 0
    for key in question_forms:
        question_forms[key] = question_forms_khan[0][key] + question_forms_khan[1][key] + question_forms_khan[2][key] + question_forms_teded[0][key] + question_forms_teded[1][key] + question_forms_teded[2][key]
        complete_amount += question_forms_khan[0][key] + question_forms_khan[1][key] + question_forms_khan[2][key] + question_forms_teded[0][key] + question_forms_teded[1][key] + question_forms_teded[2][key]
        #if question_forms[key]:
        #    question_forms[key] = question_forms[key] / (khan['questions_1'] + teded['questions_1'] + khan['questions_2'] + teded['questions_2'] + khan['questions_3'] + teded['questions_3'])
    for key in question_forms:
        if complete_amount:
            question_forms[key] = round((question_forms[key] / complete_amount) * 100,2)
    # make dictionary - question type and store it 
    type_dict = {"questions_1": round(questions_1 * 100, 2), "statements_1": round(statements_1 * 100, 2), "empty_1": round(empty_1 * 100, 2), "word_length_1": word_length_1,
          "min_length_1": min_length_1, "max_length_1": max_length_1, "readability_1": round(readability_1,2), "questions_2": round(questions_2 * 100, 2), "statements_2": round(statements_2 * 100, 2), "empty_2": round(empty_2 * 100, 2), "word_length_2": word_length_2, 
          "min_length_2": min_length_2, "max_length_2": max_length_2, "readability_2": round(readability_2,2), "questions_3": round(questions_3 * 100, 2), "statements_3": round(statements_3 * 100, 2), "empty_3": round(empty_3 * 100, 2), "word_length_3": word_length_3,
          "min_length_3": min_length_3, "max_length_3": max_length_3, "readability_3": round(readability_3,2), "question": round(questions * 100, 2), "statements": round(statements * 100, 2), "empty": round(empty * 100, 2), "word_length": round((word_length_1 + word_length_2 + word_length_3) / 3, 2), 
          "min_length": min([min_length_1, min_length_2, min_length_3]), "max_length": max([max_length_1, max_length_2, max_length_3]), "readability": round((readability_1 + readability_2 + readability_3) / 3, 2)}
    # store as file
    with open(f"./{model_name}_sentence_type.json", "w") as sentence_type:
        print("dict:", type_dict)
        json.dump(type_dict, sentence_type)
    with open(f"./{model_name}_questionforms.json", "w") as questions_data:
        print("dict:", question_forms)
        json.dump(question_forms, questions_data)


def evaluate_video_llava():
    #khan = '/data/models_output/zero_shot_results_video_llava_khan_test.txt'
    #teded = '/data/models_output/zero_shot_results_video_llava_teded_test.txt'
    khan = '/data/models_output/zero_shot_seed_results_full_video_llava_khan_test.txt'
    teded = '/data/models_output/zero_shot_seed_results_full_video_llava_teded_test.txt'

    khan_json = json.load(open(khan, 'r'))
    teded_json = json.load(open(teded, 'r'))
    results_khan, question_forms_khan = count_question_statements_empty(khan_json)
    results_teded, question_forms_teded = count_question_statements_empty(teded_json)
    merged_results(results_khan, question_forms_khan, results_teded, question_forms_teded)


def evaluate_pg_video_llava(model='zeroshot'):
    khan = '/data/models_output/zeroshot_13b_results_pg_video_llava_khan_test_1234.txt'
    teded = '/data/models_output/zeroshot_13b_results_pg_video_llava_teded_test_1234.txt'
    if model == 'finetuned-7b':
        khan = '/data/models_output/finetune_7b_results_pg_video_llava_khan_test.txt'
        teded = '/data/models_output/finetune_7b_results_pg_video_llava_teded_test.txt'
    elif model == 'finetuned-13b':
        khan = '/data/models_output/finetune_all_13b_results_pg_video_llava_khan_test_1234.txt'
        teded = '/data/models_output/finetune_all_13b_results_pg_video_llava_teded_test_1234.txt'
    elif model == 'finetuned-13b-visual':
        khan = '/data/models_output/finetune_no_transcript_all_13b_results_pg_video_llava_khan_test_1234.txt'
        teded = '/data/models_output/finetune_no_transcript_all_13b_results_pg_video_llava_teded_test_1234.txt'
    elif model == 'finetuned-13b-audio':
        khan = '/data/models_output/finetune_no_frame_all_13b_results_pg_video_llava_khan_test_1234.txt' 
        teded = '/data/models_output/finetune_no_frame_all_13b_results_pg_video_llava_teded_test_1234.txt'
    khan_json = json.load(open(khan, 'r'))
    teded_json = json.load(open(teded, 'r'))
    results_khan, question_forms_khan = count_question_statements_empty(khan_json)
    results_teded, question_forms_teded = count_question_statements_empty(teded_json)
    merged_results(results_khan, question_forms_khan, results_teded, question_forms_teded)


def evaluate_video_llama(model='zeroshot'):
    khan = '/data/models_output/zero_shot_results_video_llama_khan_test.txt'
    teded = '/data/models_output/zero_shot_results_video_llama_teded_test.txt'
    if model == 'finetuned':
        khan = '/data/models_output/finetune_new_results_seed_video_llama_13B_khan_test.txt'
        teded = '/data/models_output/finetune_new_results_seed_video_llama_13B_teded_test.txt'
    elif model == 'finetuned-visual':
        khan = '/data/models_output/finetune_no_audio_results_seed_video_llama_13B_khan_test.txt'
        teded = '/data/models_output/finetune_no_audio_results_seed_video_llama_13B_teded_test.txt'
    elif model == 'finetuned-audio':
        khan = '/data/models_output/finetune_no_frames_results_seed_video_llama_13B_khan_test.txt'
        teded = '/data/models_output/finetune_no_frames_results_seed_video_llama_13B_teded_test.txt'
    khan_json = json.load(open(khan, 'r'))
    teded_json = json.load(open(teded, 'r'))
    results_khan, question_forms_khan = count_question_statements_empty(khan_json)
    results_teded, question_forms_teded = count_question_statements_empty(teded_json)
    merged_results(results_khan, question_forms_khan, results_teded, question_forms_teded)


def evaluate_video_llava2():
    khan = '/data/models_output/patched_zero_shot_seed_results_full_video_llava_khan_test.txt'
    teded = '/data/models_output/patched_zero_shot_seed_results_full_video_llava_teded_test.txt'

    khan_json = json.load(open(khan, 'r'))
    teded_json = json.load(open(teded, 'r'))
    results_khan, question_forms_khan = count_question_statements_empty(khan_json)
    results_teded, question_forms_teded = count_question_statements_empty(teded_json)
    merged_results(results_khan, question_forms_khan, results_teded, question_forms_teded, "video_llava_zeroshot")


def evaluate_pg_video_llava2(model='zeroshot'):
    khan = '/data/models_output/patched_new_prompts_store_zeroshot_13b_results_pg_video_llava_khan_test_1234.txt'
    teded = '/data/models_output/patched_new_prompts_store_zeroshot_13b_results_pg_video_llava_teded_test_1234.txt'

    if model == 'finetuned-13b':
        khan = '/data/models_output/patched_new_prompts_store_finetune_13b_results_pg_video_llava_khan_test_1234.txt'
        teded = '/data/models_output/patched_new_prompts_store_finetune_13b_results_pg_video_llava_teded_test_1234.txt'
    elif model == 'finetuned-13b-visual':
        khan = '/data/models_output/patched_frames_only_new_prompts_store_finetune_13b_results_pg_video_llava_khan_test_1234.txt'
        teded = '/data/models_output/patched_frames_only_new_prompts_store_finetune_13b_results_pg_video_llava_teded_test_1234.txt'
    elif model == 'finetuned-13b-audio':
        khan = '/data/models_output/patched_audio_only_new_prompts_store_finetune_13b_results_pg_video_llava_khan_test_1234.txt' 
        teded = '/data/models_output/patched_audio_only_new_prompts_store_finetune_13b_results_pg_video_llava_teded_test_1234.txt'
    khan_json = json.load(open(khan, 'r'))
    teded_json = json.load(open(teded, 'r'))
    results_khan, question_forms_khan = count_question_statements_empty(khan_json)
    results_teded, question_forms_teded = count_question_statements_empty(teded_json)
    merged_results(results_khan, question_forms_khan, results_teded, question_forms_teded, f"pg_video_llava_{model}")


def evaluate_video_llama2(model='zeroshot'):
    khan = '/data/models_output/patched_new_prompts_store_zeroshot_seed_video_llama_13B_khan_test.txt'
    teded = '/data/models_output/patched_new_prompts_store_zeroshot_seed_video_llama_13B_teded_test.txt'
    if model == 'finetuned':
        khan = '/data/models_output/patched_new_prompts_store_finetuned_seed_video_llama_13B_khan_test.txt'
        teded = '/data/models_output/patched_new_prompts_store_finetune_seed_video_llama_13B_teded_test.txt'
    elif model == 'finetuned-visual':
        khan = '/data/models_output/patched_frames_only_new_prompts_store_finetune_seed_video_llama_13B_khan_test.txt'
        teded = '/data/models_output/patched_frames_only_new_prompts_store_finetune_seed_video_llama_13B_teded_test.txt'
    elif model == 'finetuned-audio':
        khan = '/data/models_output/patched_audio_only_new_prompts_store_finetune_seed_video_llama_13B_khan_test.txt'
        teded = '/data/models_output/patched_audio_only_new_prompts_store_finetune_seed_video_llama_13B_teded_test.txt'
    khan_json = json.load(open(khan, 'r'))
    teded_json = json.load(open(teded, 'r'))
    results_khan, question_forms_khan = count_question_statements_empty(khan_json)
    results_teded, question_forms_teded = count_question_statements_empty(teded_json)
    merged_results(results_khan, question_forms_khan, results_teded, question_forms_teded, f"video_llama_{model}")


def evaluate_mistral():
    khan = '/data/models_output/patched_new_prompts_store_zeroshot_7b_results_mistral_khan_test_1234.txt'
    teded = '/data/models_output/patched_new_prompts_store_zeroshot_7b_results_mistral_teded_test_1234.txt'

    khan_json = json.load(open(khan, 'r'))
    teded_json = json.load(open(teded, 'r'))
    results_khan, question_forms_khan = count_question_statements_empty(khan_json)
    results_teded, question_forms_teded = count_question_statements_empty(teded_json)
    merged_results(results_khan, question_forms_khan, results_teded, question_forms_teded, "mistral_7b_instruct")



# CHOOSE model to evaluate
#print("Results zero-shot videollava:")
#evaluate_video_llava2()

#print("Results zero-shot pgvideollava (13b):")
#evaluate_pg_video_llava2()
#print("Results finetuned pg-videollava 13b:")
#evaluate_pg_video_llava2("finetuned-13b")
#print("Results finetuned pg-videollava 13b (only visual):")
#evaluate_pg_video_llava2("finetuned-13b-visual")
#print("Results finetuned pg-videollava 13b (only speech):")
#evaluate_pg_video_llava2("finetuned-13b-audio")
#print("Results zero-shot videollama:")
#evaluate_video_llama2()
#print("Results finetuned videollama:")
#evaluate_video_llama2('finetuned')
#print("Results finetuned videollama (only visual):")
#evaluate_video_llama2('finetuned-visual')
#print("Results finetuned videollama (only speech):")
#evaluate_video_llama2('finetuned-audio')
print("Evaluate mistral:")
evaluate_mistral()
