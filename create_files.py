import random

import pandas as pd
from tqdm import tqdm
from datasets import Dataset

train_df = pd.read_csv(r'data\generatedtrain_df.csv')
val_df = pd.read_csv(r'data\generatedval_df.csv')
test_df = pd.read_csv(r'data\generatedtest_df.csv')

df = pd.concat([train_df, val_df, test_df])

df_dict = {"context": [], "question": [], "code": [], "answer": []}
for idx, entry in tqdm(df.iterrows()):
    available = []
    # print(entry["code5"])
    if not pd.isnull(entry["code5"]):
        available.append([entry["question5"], entry["code5"], entry["answer5"]])
        # print("appending\t",[entry["question5"],entry["code5"]])
    if not pd.isnull(entry["code6"]):
        available.append([entry["question6"], entry["code6"], entry["answer6"]])
        # print("appending\t",[entry["question6"],entry["code6"]])
    if not pd.isnull(entry["code7"]):
        available.append([entry["question7"], entry["code7"], entry["answer7"]])
        # print("appending\t",[entry["question7"],entry["code7"]])
    if len(available) > 0:
        chosen_question_code = random.choice(available)
        # print(chosen_question_code)
        df_dict["context"].append(entry["context"])
        df_dict["question"].append(chosen_question_code[0])
        df_dict["code"].append(chosen_question_code[1].replace("\n", " "))
        df_dict["answer"].append(str(chosen_question_code[2]))
        continue
    if not pd.isnull(entry["question1"]) > 0:
        available.append([entry["question1"], entry["code1"], entry["answer1"]])
    if not pd.isnull(entry["question2"]) > 0:
        available.append([entry["question2"], entry["code2"], entry["answer2"]])
    if not pd.isnull(entry["question3"]) > 0:
        available.append([entry["question3"], entry["code3"], entry["answer3"]])
    if not pd.isnull(entry["question4"]) > 0:
        available.append([entry["question4"], entry["code4"], entry["answer4"]])

    chosen_question_code = random.choice(available)
    df_dict["context"].append(entry["context"].replace("\n", ""))
    df_dict["question"].append(chosen_question_code[0].strip())
    df_dict["code"].append(chosen_question_code[1].replace("\n", " "))
    df_dict["answer"].append(str(chosen_question_code[2]))

raw_dataset = Dataset.from_dict(df_dict)
raw_dataset.to_csv("simAPI.csv")

all_dataset = raw_dataset.train_test_split(train_size=0.8)
test_val_split = all_dataset["test"]
train_dataset = all_dataset["train"]
test_val_dataset = test_val_split.train_test_split(train_size=0.5)
val_dataset = test_val_dataset["train"]
test_dataset = test_val_dataset["test"]

train_dataset.to_csv("final_train.csv")
val_dataset.to_csv("final_val.csv")
test_dataset.to_csv("final_test.csv")
