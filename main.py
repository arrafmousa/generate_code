import csv
import os
import random
import re
from tqdm import tqdm

import pandas as pd

from generate_questiontion_with_chempy import generate_question_type1, generate_question_type2, generate_question_type3, \
    generate_question_type4, get_reactors_and_output, generate_question_type5, generate_question_type6, \
    generate_question_type7
from function_calls import *
import tkinter as tk
from tkinter import messagebox

import tkinter as tk
from tkinter import messagebox

from popupwindow import create_popup


def formulate_code(entry):
    code = ""
    code += 'import pubchempy as pcp\n'
    code += 'import function_calls'
    code += '\n'
    code += "def generated_code():\n"
    for code_line in entry.split("[EOL]"):
        code_line = code_line.replace("pcp.get_compounds( '", "pcp.get_compounds( \"")
        code_line = code_line.replace("needed_reactors_for_100g_product", "have_components")
        code_line = code_line.replace("' , 'name')[0]", "\" , 'name')[0]")
        code_line = code_line.replace("[EOL]", "\n")
        code_line = code_line.replace("[TAB]", "\t")

        if len(code_line) > 0 and code_line[0] == "▁":
            code_line = code_line[1:]
        code_line = code_line.replace("▁", " ")
        code += "\t"
        code += code_line
        code += '\n'
    code += "ret_vale = generated_code()"
    return code


def append_to_csv(filename, data):
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='',encoding="utf8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['context', 'question1', 'code1', 'answer1', 'question2', 'code2', 'answer2',
                             'question3', 'code3', 'answer3', 'question4', 'c  ode4', 'answer4', 'question5', 'code5',
                             'answer5',
                             'question6', 'code6', 'answer6', 'question7', 'code7', 'answer7'])
        try:
            writer.writerow(data)
        except Exception as e:
            print(e)
            exit(99999)
            print(data)


for file in ["train", "test", "val"]:
    df = pd.read_csv(r"data/" + file + ".csv")
    data_set = df[["context"]]


    def generate_question(ds: pd.DataFrame, i):
        df_dict = {"train": []}
        counter = 0
        df = {'context': [], 'question1': [], 'code1': [], 'answer1': [], 'question2': [], 'code2': [], 'answer2': [],
              'question3': [], 'code3': [], 'answer3': [], 'question4': [], 'code4': [], 'answer4': [], 'question5': [],
              'code5': [], 'answer5': [], 'question6': [], 'code6': [], 'answer6': [], 'question7': [], 'code7': [],
              'answer7': [], }
        for idx, row in tqdm(ds.iterrows()):
            if i > 0:
                i -= 1
                continue
            # print()
            # print(row["context"], "\t:")
            vars_and_vals = get_reactors_and_output(row)
            vars_and_vals = create_popup(row["context"], vars_and_vals[0])
            if vars_and_vals is None:
                continue
            try:
                vars_and_vals = vars_and_vals, vars_and_vals[-1][1]
            except:
                print(vars_and_vals)
                continue

            entry = [row["context"]]

            if vars_and_vals[0] is None or len(vars_and_vals[0]) == 0:
                continue

            is_good = True
            for ii, (name, val) in enumerate(vars_and_vals[0]):
                if 'ml' in val:
                    vars_and_vals[0][ii] = [vars_and_vals[0][ii][0], vars_and_vals[0][ii][1].replace('ml', 'mL')]
            for ii, (name, val) in enumerate(vars_and_vals[0]):
                # if 'ml' in val:
                #     vars_and_vals[0][ii] = vars_and_vals[0][ii][0], vars_and_vals[0][ii][1].replace('ml', 'mL')
                if ("mg" not in val) and ("g" not in val) and ("mL" not in val) and (
                        "ml" not in val):  # TODO : and ("mmol" not in val):
                    counter += 1
                    is_good = False
                    break

            if is_good:
                df["context"].append(row["context"])

                q, c = generate_question_type1(row)
                df["question1"].append(q)
                df["code1"].append(c)
                entry.append(q)
                entry.append(c)
                loc = {}
                try:
                    exec(formulate_code(c), globals(), loc)
                except:
                    loc["ret_vale"] = None
                    print("ERROR")
                    print(formulate_code(c))

                df["answer1"].append(loc["ret_vale"])
                entry.append(loc["ret_vale"])

                q, c = generate_question_type2(row)
                df["question2"].append(q)
                df["code2"].append(c)
                entry.append(q)
                entry.append(c)

                loc = {}
                try:
                    exec(formulate_code(c), globals(), loc)
                except:
                    loc["ret_vale"] = None
                    print("ERROR")
                    print(formulate_code(c))

                df["answer2"].append(loc["ret_vale"])
                entry.append(loc["ret_vale"])

                q, c = generate_question_type3(row)
                df["question3"].append(q)
                df["code3"].append(c)
                entry.append(q)
                entry.append(c)

                loc = {}
                try:
                    exec(formulate_code(c), globals(), loc)
                except:
                    loc["ret_vale"] = None
                    print("ERROR")
                    print(formulate_code(c))

                df["answer3"].append(loc["ret_vale"])
                entry.append(loc["ret_vale"])

                q, c = generate_question_type4(row)
                df["question4"].append(q)
                df["code4"].append(c)
                entry.append(q)
                entry.append(c)

                if q is not None:
                    loc = {}
                    try:
                        exec(formulate_code(c), globals(), loc)
                    except:
                        loc["ret_vale"] = None
                        print("ERROR")
                        print(formulate_code(c))

                    df["answer4"].append(loc["ret_vale"])
                    entry.append(loc["ret_vale"])

                else:
                    df["answer4"].append(None)
                    entry.append(None)

                q, c = generate_question_type5(row)
                df["question5"].append(q)
                df["code5"].append(c)
                entry.append(q)
                entry.append(c)

                if len(q) != 0:
                    loc = {}
                    try:
                        exec(formulate_code(c), globals(), loc)
                    except:
                        loc["ret_vale"] = None
                        print("ERROR")
                        print(formulate_code(c))

                    df["answer5"].append(loc["ret_vale"])
                    entry.append(loc["ret_vale"])

                else:
                    df["answer5"].append(None)
                    entry.append(None)

                q, c = generate_question_type6(row)
                df["question6"].append(q)
                df["code6"].append(c)
                entry.append(q)
                entry.append(c)

                if len(q) != 0:
                    loc = {}
                    try:
                        exec(formulate_code(c), globals(), loc)
                    except:
                        loc["ret_vale"] = None
                        print("ERROR")
                        print(formulate_code(c))

                    df["answer6"].append(loc["ret_vale"])
                    entry.append(loc["ret_vale"])
                else:
                    df["answer6"].append(None)
                    entry.append(None)

                q, c = generate_question_type7(row)
                df["question7"].append(q)
                df["code7"].append(c)
                entry.append(q)
                entry.append(c)

                if len(q) != 0:
                    loc = {}
                    try:
                        exec(formulate_code(c), globals(), loc)
                    except:
                        loc["ret_vale"] = None
                        print("ERROR")
                        print(formulate_code(c))

                    df["answer7"].append(loc["ret_vale"])
                    entry.append(loc["ret_vale"])
                else:
                    df["answer7"].append(None)
                    entry.append(None)


            else:
                print(row["context"])

            append_to_csv(file + "data_handwritten.csv", entry)


    generate_question(data_set, 37)

