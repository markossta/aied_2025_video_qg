import json


"""
            question_dict[1]["own"].append(own_sim)
            question_dict[1]["other_max"].append(max_similarity)
            question_dict[1]["diff_max"].append(own_sim - max_similarity)

            question_dict[1]["other_min"].append(min_similarity)
            question_dict[1]["diff_min"].append(own_sim - min_similarity)

            question_dict[1]["other_avg"].append(avg_similarity)
            question_dict[1]["diff_avg"].append(own_sim - avg_similarity)
        elif 'Develop' in prompt:
            question_dict[2]["own"].append(own_sim)
            question_dict[2]["other_max"].append(max_similarity)
            question_dict[2]["diff_max"].append(own_sim - max_similarity)

            question_dict[2]["other_min"].append(min_similarity)
            question_dict[2]["diff_min"].append(own_sim - min_similarity)

            question_dict[2]["other_avg"].append(avg_similarity)
            question_dict[2]["diff_avg"].append(own_sim - avg_similarity)
        else:
            question_dict[3]["own"].append(own_sim)
            question_dict[3]["other_max"].append(max_similarity)
            question_dict[3]["diff_max"].append(own_sim - max_similarity)

            question_dict[3]["other_min"].append(min_similarity)
            question_dict[3]["diff_min"].append(own_sim - min_similarity)

            question_dict[3]["other_avg"].append(avg_similarity)
            question_dict[3]["diff_avg"].append(own_sim - avg_similarity)"""

def calc_min(question_dict):
    prompt1 = question_dict["1"]
    prompt1_min_own = sum(prompt1["own"]) / len(prompt1["own"])
    prompt1_min_other = sum(prompt1["other_min"]) / len(prompt1["other_min"])    
    prompt1_min_diff = sum(prompt1["diff_min"]) / len(prompt1["diff_min"])
    # prompt 2
    prompt2 = question_dict["2"]
    prompt2_min_own = sum(prompt2["own"]) / len(prompt2["own"])
    prompt2_min_other = sum(prompt2["other_min"]) / len(prompt2["other_min"])    
    prompt2_min_diff = sum(prompt2["diff_min"]) / len(prompt2["diff_min"])
    # prompt 3
    prompt3 = question_dict["3"]
    prompt3_min_own = sum(prompt3["own"]) / len(prompt3["own"])
    prompt3_min_other = sum(prompt3["other_min"]) / len(prompt3["other_min"]) 
    prompt3_min_diff = sum(prompt3["diff_min"]) / len(prompt3["diff_min"])
    # min all
    prompt_min_own = round((prompt1_min_own + prompt2_min_own + prompt3_min_own) / 3, 2)
    prompt_min_other = round((prompt1_min_other + prompt2_min_other + prompt3_min_other) / 3, 2)
    prompt_min_diff = round((prompt1_min_diff + prompt2_min_diff + prompt3_min_diff) / 3, 2)
    print("1 own similarity is:", round(prompt1_min_own, 2), "1 other similarity is:", prompt1_min_other, "1 diff similarity is:", round(prompt1_min_diff, 2))
    print("2 own similarity is:", round(prompt2_min_own, 2), "2 other similarity is:", prompt2_min_other, "2 diff similarity is:", round(prompt2_min_diff, 2))
    print("3 own similarity is:", round(prompt3_min_own, 2), "3 other similarity is:", prompt3_min_other, "3 diff similarity is:", round(prompt3_min_diff, 2))    
    print("Avg own similarity is:", round(prompt_min_own, 2), "Avg other similarity is:", prompt_min_other, prompt_min_own, "Avg diff similarity is:", prompt_min_diff)


def calc_max(question_dict):
    prompt1 = question_dict["1"]
    prompt1_max_own = sum(prompt1["own"]) / len(prompt1["own"])
    prompt1_max_other = sum(prompt1["other_max"]) / len(prompt1["other_max"])    
    prompt1_max_diff = sum(prompt1["diff_max"]) / len(prompt1["diff_max"])
    # prompt 2
    prompt2 = question_dict["2"]
    prompt2_max_own = sum(prompt2["own"]) / len(prompt2["own"])
    prompt2_max_other = sum(prompt2["other_max"]) / len(prompt2["other_max"])    
    prompt2_max_diff = sum(prompt2["diff_max"]) / len(prompt2["diff_max"])
    # prompt 3
    prompt3 = question_dict["3"]
    prompt3_max_own = sum(prompt3["own"]) / len(prompt3["own"])
    prompt3_max_other = sum(prompt3["other_max"]) / len(prompt3["other_max"]) 
    prompt3_max_diff = sum(prompt3["diff_max"]) / len(prompt3["diff_max"])
    # max all
    prompt_max_own = round((prompt1_max_own + prompt2_max_own + prompt3_max_own) / 3, 2)
    prompt_max_other = round((prompt1_max_other + prompt2_max_other + prompt3_max_other) / 3, 2)
    prompt_max_diff = round((prompt1_max_diff + prompt2_max_diff + prompt3_max_diff) / 3, 2)
    print("1 own similarity is:", round(prompt1_max_own, 2), "1 other similarity is:", prompt1_max_other, "1 diff similarity is:", round(prompt1_max_diff, 2))
    print("2 own similarity is:", round(prompt2_max_own, 2), "2 other similarity is:", prompt2_max_other, "2 diff similarity is:", round(prompt2_max_diff, 2))
    print("3 own similarity is:", round(prompt3_max_own, 2), "3 other similarity is:", prompt3_max_other, "3 diff similarity is:", round(prompt3_max_diff, 2))    
    print("Avg own similarity is:", round(prompt_max_own, 2), "Avg other similarity is:", prompt_max_other, prompt_max_own, "Avg diff similarity is:", prompt_max_diff)


def calc_avg(question_dict):
    # prompt 1
    prompt1 = question_dict["1"]
    prompt1_avg_own = sum(prompt1["own"]) / len(prompt1["own"])
    prompt1_avg_other = sum(prompt1["other_avg"]) / len(prompt1["other_avg"])    
    prompt1_avg_diff = sum(prompt1["diff_avg"]) / len(prompt1["diff_avg"])
    # prompt 2
    prompt2 = question_dict["2"]
    prompt2_avg_own = sum(prompt2["own"]) / len(prompt2["own"])
    prompt2_avg_other = sum(prompt2["other_avg"]) / len(prompt2["other_avg"])    
    prompt2_avg_diff = sum(prompt2["diff_avg"]) / len(prompt2["diff_avg"])
    # prompt 3
    prompt3 = question_dict["3"]
    prompt3_avg_own = sum(prompt3["own"]) / len(prompt3["own"])
    prompt3_avg_other = sum(prompt3["other_avg"]) / len(prompt3["other_avg"]) 
    prompt3_avg_diff = sum(prompt3["diff_avg"]) / len(prompt3["diff_avg"])
    # avg all
    prompt_avg_own = round((prompt1_avg_own + prompt2_avg_own + prompt3_avg_own) / 3, 2)
    prompt_avg_other = round((prompt1_avg_other + prompt2_avg_other + prompt3_avg_other) / 3, 2)
    prompt_avg_diff = round((prompt1_avg_diff + prompt2_avg_diff + prompt3_avg_diff) / 3, 2)
    print("1 own similarity is:", round(prompt1_avg_own, 2), "1 other similarity is:", prompt1_avg_other, "1 diff similarity is:", round(prompt1_avg_diff, 2))
    print("2 own similarity is:", round(prompt2_avg_own, 2), "2 other similarity is:", prompt2_avg_other, "2 diff similarity is:", round(prompt2_avg_diff, 2))
    print("3 own similarity is:", round(prompt3_avg_own, 2), "3 other similarity is:", prompt3_avg_other, "3 diff similarity is:", round(prompt3_avg_diff, 2))    
    print("Avg own similarity is:", round(prompt_avg_own, 2), "Avg other similarity is:", prompt_avg_other, prompt_avg_own, "Avg diff similarity is:", prompt_avg_diff)


def process_values():
    # load dictionary
    print("load file")
    # Here choose specific model file with cosine similarities of embeddings
    with open("/data/models_output/patched_new_prompts_store_finetuned_seed_video_llama_13B_khan_test_cosine.txt", "r") as f:
        question_dict = json.load(f)
        print("Min Values:")
        calc_min(question_dict)
        print()
        print("Avg values:")
        calc_avg(question_dict)
        print()
        print("Max values:")
        calc_max(question_dict)
        print()


process_values()
