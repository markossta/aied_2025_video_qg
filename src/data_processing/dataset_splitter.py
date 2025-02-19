import json
import random
import pandas as pd


def count_khan_questions(data, idx):
    amount_questions = 0
    for key in idx:
        amount_questions += len(data[key])
    return amount_questions


def count_teded_questions(data, idx):
    amount_questions = 0
    amount_multiple = 0
    amount_open = 0
    for key in idx:
        amount_questions += len(data[key])
        for question in data[key]:
            if question["question_type"] == "multiple-choices":
                amount_multiple +=1
            else:
                amount_open += 1
    return amount_questions, amount_multiple, amount_open


def data_split(path, name, train_percent=0.8, validate_percent=0.1):
    with open(path, 'r') as f:
        js = json.load(f)
        keys = list(js.keys())
        random.shuffle(keys)
        m = len(keys)
        train_end = int(train_percent * m)
        validate_end = int(validate_percent * m) + train_end
        train = keys[:train_end]
        validate = keys[train_end:validate_end]
        test = keys[validate_end:]
        # store dict
        split_dict = {"train": train, "val": validate, "test": test}
        with open(f'./{name}_datasplit.txt', 'w') as s:
            json.dump(split_dict, s, indent=4)
        # get statistics
        print(f"Statistics for {name}:")
        if (name == 'khan'):
            train_questions = count_khan_questions(js, train)
            val_questions = count_khan_questions(js, validate)
            test_questions = count_khan_questions(js, test)
        else:
            train_questions, train_multiple, train_open = count_teded_questions(js, train)
            val_questions, val_multiple, val_open = count_teded_questions(js, validate)
            test_questions, test_multiple, test_open = count_teded_questions(js, test)

        print("Amount train videos:", len(train), "Amount val videos:", len(validate), "Amount test videos:", len(test))
        print("Amount train questions:", train_questions, "Amount val questions:", val_questions, "Amount test questions:", test_questions)
        if (name != 'khan'):
            print("Amount train multiple:", train_multiple, "Amount train open:", train_open, "Amount val multiple:", val_multiple, "Amount val open:", val_open, "Amount test multiple:", test_multiple, "Amount test open:", test_open)
        print()
        


# set seed for reproduction
seed = 1234
random.seed(seed)
# Make data splits for khan
data_split('./khan_filtered_questions.txt', 'khan')
# Make data splits for teded
data_split('./teded_filtered_questions.txt', 'teded')
