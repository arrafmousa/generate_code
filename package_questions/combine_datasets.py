import json
import random
import re

from aaa import parse_API

# Define the file names
file_names = ["astropy.json", "bio.json", "pcp.json", r"gpt4-parsed-simapi.json"]

# Placeholder for combined data
combined_data = []

# Read each file and add an identifier
for file_name in file_names:
    with open(file_name, "r") as f:
        data = json.load(f)
        print(f"{file_name} has {len(data)} entries")
        for entry in data:
            entry["source_file"] = file_name
        combined_data.extend(data)

# Shuffle the combined list
random.shuffle(combined_data)

import ast


class APIDetector(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.api_calls = []

    def visit_Call(self, node):
        func_name = ast.get_source_segment(self.source_code, node.func)
        args = [ast.get_source_segment(self.source_code, a) for a in node.args]

        self.api_calls.append({
            "api": func_name,
            "args": args
        })
        self.generic_visit(node)


def tag_apis_in_code(code):
    detector = APIDetector(code)
    detector.visit(ast.parse(code))

    for call in detector.api_calls:
        api_name = re.escape(call["api"]).replace("\\ ", "\\s*")
        args_with_tags = ', '.join([f'<ARG>{arg}</ARG>' for arg in call["args"]])

        # Build a regex pattern for the arguments
        arg_pattern = '\\s*,\\s*'.join([re.escape(arg) for arg in call["args"]])
        original_call_pattern = f"{api_name}\\s*\\(\\s*{arg_pattern}\\s*\\)"

        tagged_call = f"<API>{api_name}</API>({args_with_tags})"
        code = re.sub(original_call_pattern, tagged_call, code, count=1)

    return code


# Add "parsed_api" entries to the dataset
for entry in combined_data:
    try:
        entry["parsed_api"] = tag_apis_in_code(entry["code"])
    except Exception as e:
        print(e)
        print(e)

# Save to a new JSON file (optional)
with open("combined_shuffled.json", "w") as f:
    json.dump(combined_data, f, indent=4)

print("")