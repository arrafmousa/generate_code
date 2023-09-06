import csv
import json

def formulate_code(entry):
    code = ""
    code += 'import pubchempy as pcp\n'
    code += 'import function_calls'
    code += '\n'
    for code_line in entry.split("[EOL]"):
        code_line = code_line.replace("pcp.get_compounds( '", "pcp.get_compounds( \"")
        code_line = code_line.replace("needed_reactors_for_100g_product", "have_components")
        code_line = code_line.replace("' , 'name')[0]", "\" , 'name')[0]")
        code_line = code_line.replace("[EOL]", "\n")
        code_line = code_line.replace("[TAB]", "\t")

        if len(code_line) > 0 and code_line[0] == "▁":
            code_line = code_line[1:]
        code_line = code_line.replace("▁", " ")
        code += code_line
        code += '\n'
    code = code.replace("return", "result = ")
    return code


def augment_price(row):
    """Increase price by 10%."""
    row['code'] = formulate_code(row['code'])
    row['code'] = row['code'].replace("to_gr","to_stu")
    row['question'] = row['context']+' '+row['question']
    del row['context']
    return row


def csv_to_json(csv_filename, json_filename):
    """Convert a CSV file to JSON format."""

    # List to hold dictionaries
    data = []

    # Read CSV file
    with open(csv_filename, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Convert each row into a dictionary and add it to data
        for row in csv_reader:
            augmented_row = augment_price(row)
            data.append(augmented_row)

    # Write JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Example usage
csv_to_json('simAPI.csv', 'package_questions/simapi.json')
