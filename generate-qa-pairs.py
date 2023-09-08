import csv
import re
import json
import random

from tqdm import tqdm
import pubchempy as pcp
from utils import randomize_product_amount, randomize_ingredients, make_ingredients_list, make_ingredients_string, \
    generate_duration, execute_code

from function_calls import to_stu

atoms_list = ["	Hydrogen	",
              "	Helium	",
              "	Lithium	",
              "	Beryllium	",
              "	Boron	",
              "	Carbon	",
              "	Nitrogen	",
              "	Oxygen	",
              "	Fluorine	",
              "	Neon	",
              "	Sodium	",
              "	Magnesium	",
              "	Aluminium	",
              "	Silicon	",
              "	Phosphorus	",
              "	Sulfur	",
              "	Chlorine	",
              "	Argon	",
              "	Potassium	",
              "	Calcium	",
              "	Scandium	",
              "	Titanium	",
              "	Vanadium	",
              "	Chromium	",
              "	Manganese	",
              "	Iron	",
              "	Cobalt	",
              "	Nickel	",
              "	Copper	",
              "	Zinc	",
              "	Gallium	",
              "	Germanium	",
              "	Arsenic	",
              "	Selenium	",
              "	Bromine	",
              "	Krypton	",
              "	Rubidium	",
              "	Strontium	",
              "	Yttrium	",
              "	Zirconium	",
              "	Niobium	",
              "	Molybdenum	",
              "	Technetium	",
              "	Ruthenium	",
              "	Rhodium	",
              "	Palladium	",
              "	Silver	",
              "	Cadmium	",
              "	Indium	",
              "	Tin	",
              "	Antimony	",
              "	Tellurium	",
              "	Iodine	",
              "	Xenon	",
              "	Cesium	",
              "	Barium	",
              "	Lanthanum	",
              "	Cerium	",
              "	Praseodymium	",
              "	Neodymium	",
              "	Promethium	",
              "	Samarium	",
              "	Europium	",
              "	Gadolinium	",
              "	Terbium	",
              "	Dysprosium	",
              "	Holmium	",
              "	Erbium	",
              "	Thulium	",
              "	Ytterbium	",
              "	Lutetium	",
              "	Hafnium	",
              "	Tantalum	",
              "	Tungsten	",
              "	Rhenium	",
              "	Osmium	",
              "	Iridium	",
              "	Platinum	",
              "	Gold	",
              "	Mercury	",
              "	Thallium	",
              "	Lead	",
              "	Bismuth	",
              "	Polonium	",
              "	Astatine	",
              "	Radon	",
              "	Francium	",
              "	Radium	",
              "	Actinium	",
              "	Thorium	",
              "	Protactinium	",
              "	Uranium	",
              "	Neptunium	",
              "	Plutonium	",
              "	Americium	",
              "	Curium	",
              "	Berkelium	",
              "	Californium	",
              "	Einsteinium	",
              "	Fermium	",
              "	Mendelevium	",
              "	Nobelium	",
              "	Lawrencium	",
              "	Rutherfordium	",
              "	Dubnium	",
              "	Seaborgium	",
              "	Bohrium	",
              "	Hassium	",
              "	Meitnerium	",
              "	Darmstadtium	",
              "	Roentgenium	",
              "	Copernicium	",
              "	Nihonium	",
              "	Flerovium	",
              "	Moscovium	",
              "	Livermorium	",
              "	Tennessine	",
              "	Oganesson	",
              ]


def formulate_code(entry):
    code = ""
    code += 'import pubchempy as pcp\n'
    code += 'from function_calls import *'
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
    return code


# Open the CSV file
def get_next_entry():
    with open('gpt4-parsed-uspto.json', 'r') as json_file:
        # Create a CSV reader object
        file = json.load(json_file)
        # Iterate over each row in the CSV file
        for file_entry in file:
            yield file_entry


def generate_question_type1(entry) -> (str, str, str, str):
    desired_output = randomize_product_amount(entry["product"]["quantity"])
    question = f"how much do we need from each of the reactors to get {desired_output} of the final product ?"
    code = f"desired_product = to_stu( \" {desired_output} \" )[EOL]" \
           f"components = {[[components['reactant'], components['quantity']] for components in entry['reactants']]} [EOL]" \
           f"product_described = to_stu( \" {entry['product']['quantity']} \" )[EOL]" \
           f"portions_needed = desired_product / product_described [EOL]" \
           f"needed_reactors = [[reactor [ 0 ] , to_stu( reactor [ 1 ] ) * portions_needed] for reactor in components] [EOL]" \
           f"result = needed_reactors [EOL]"
    code = formulate_code(code)
    answer = execute_code(code)
    return entry['contexts'], question, code, answer


def generate_question_type2(entry) -> [str, str, str]:  # debugged
    available_components = [[component['reactant'], randomize_product_amount(component["quantity"])] for component
                            in entry["reactants"]]
    question2 = f"we have {available_components}, how can we minimize the residual components ?"  # TODO V2 : add an environmental conditions
    q_list = None
    code = f"components = {make_ingredients_list(entry['reactants'])} [EOL]" \
           f"have_components = {available_components} [EOL]" \
           f"min_portion = float( 'inf' ) [EOL]" \
           f"for component, needed in zip ( components , have_components ) : [EOL]" \
           f"[TAB]portions = to_stu( component [ 1 ] ) / to_stu( needed [ 1 ] ) [EOL]" \
           "[TAB]if portions < min_portion : [EOL]" \
           "[TAB][TAB]min_portion = portions [EOL]" \
           "optimized = [] [EOL]" \
           "for need, have in zip ( components , have_components ) : [EOL]" \
           "[TAB]optimized.append( [ have[0] , to_stu( have [1] ) - to_stu ( need [1] ) * min_portion ] ) [EOL]" \
           "result = optimized [EOL]"
    code = formulate_code(code)
    answer = execute_code(code)
    return entry['contexts'], question2, code, answer


def generate_question_type3(entry) -> [str, str, str]:
    randomized_ingredients = randomize_ingredients(entry["reactants"])
    question = f"we have {make_ingredients_string(randomized_ingredients)}, how much can we create of the final product?"  # TODO V2 : add an environmental conditions
    code = f"available_reactors = {make_ingredients_list(randomized_ingredients)} [EOL]" \
           f"original_reactors =  {make_ingredients_list(entry['reactants'])} [EOL]" \
           f"product_described = to_stu( \" {entry['product']['quantity']} \" ) [EOL]" \
           f"minimal_product_portion = float( 'inf' ) [EOL]" \
           f"for needed, have in zip ( original_reactors , available_reactors ): [EOL]" \
           f"[TAB]tmp_min_portion = to_stu( have [ 1 ] ) / to_stu( needed[1] ) [EOL]" \
           f"[TAB]if tmp_min_portion < minimal_product_portion : [EOL]" \
           f"[TAB][TAB]minimal_product_portion = tmp_min_portion [EOL]" \
           f"result = minimal_product_portion * product_described [EOL]"
    code = formulate_code(code)
    answer = execute_code(code)
    return entry['contexts'], question, code, answer


def get_time_from_question(question):
    return re.findall(", for (.*),", question)[0]


def generate_question_type4(entry) -> [str, str, str]:
    desired_output = randomize_product_amount(entry["product"]["quantity"])
    generated_temp, temp_threshold_str, loss_str, generated_duration, heat_duration_str, name, question = generate_duration(
        entry["contexts"], desired_output)
    code = f"time = to_minute( \" {get_time_from_question(question)} \" ) [EOL]" \
           f"loss = \'{loss_str[0]}\' [EOL]" \
           f"components = {make_ingredients_list(entry['reactants'])} [EOL]" \
           f"described_product_amount = to_stu( \" {desired_output} \" ) [EOL]" \
           f"threshold_duration = to_minute( \" {heat_duration_str} \" ) [EOL]" \
           f"temprature = {generated_temp} [EOL]" \
           f"threshold_temp = {temp_threshold_str} [EOL]" \
           f"final_product_amount = described_product_amount [EOL]" \
           f"for t in range( time ): [EOL]" \
           f"[TAB]if t > threshold_duration and temprature > threshold_temp: [EOL]" \
           f"[TAB][TAB]final_product_amount = compensate_for_loss( loss= loss[0], current_value= final_product_amount) [EOL]" \
           f"portions = final_product_amount / described_product_amount [EOL]" \
           f"result = [[component[0], to_stu(component[1]) * portions] for component in components] [EOL]"
    code = formulate_code(code)
    answer = execute_code(code)
    return entry['contexts'], question, code, answer


def generate_question_type5(entry) -> [str, str, str]:
    question = "how many moles of the product does the process yield ?"
    code = f"molar_mass = pcp.get_compounds( \"{entry['product']['product']}\", 'name')[0].exact_mass [EOL]" \
           f"molar_mass = float ( molar_mass ) [EOL]" \
           f"yielded_grams = to_stu(\" {entry['product']['quantity']} \") [EOL]" \
           f"result =  yielded_grams  /  molar_mass  [EOL]"
    code = formulate_code(code)
    answer = execute_code(code)
    return entry['contexts'], question, code, answer


def generate_question_type6(entry: dict):  # debugged
    randomized_desired_output = randomize_product_amount(entry["product"]["quantity"])
    reactor_name, reactor_weight, reactor_chosen = '', '', ''
    random_reactants = entry["reactants"].copy()
    random.shuffle(random_reactants)
    for reactor in random_reactants:
        reactor_chosen = reactor
        reactor_name = reactor_chosen["reactant"]
        reactor_weight = reactor_chosen["quantity"]
        try:
            validity_check = pcp.get_compounds({reactor_name}, 'name')[0].exact_mass
        except:
            # raise Exception('Safe : could not find compounds in pcp')
            pass

    question = f"how many moles of {reactor_name} do we need to get {randomized_desired_output} of the product {entry['product']['product']} ?"
    code = f"desired_product = to_stu( ' {randomized_desired_output} ' ) [EOL]" \
           f"product_described = to_stu( ' {entry['product']['quantity']} ' ) [EOL]" \
           f"described_component = to_stu( ' {reactor_weight} ') [EOL]" \
           f"needed_reactor = desired_product / product_described * described_component [EOL]" \
           f"reactor_molar_weight = pcp.get_compounds( \"{reactor_name}\" , 'name')[0].exact_mass [EOL]" \
           f"result = ( needed_reactor / float( reactor_molar_weight ) ) [EOL]"
    code = formulate_code(code)
    answer = execute_code(code)
    return entry['contexts'], question, code, answer


def generate_question_type7(entry):  # debugged
    chosen_atom = random.choice(atoms_list).strip()
    question = f"Is {chosen_atom} present in the product ?"
    code = f"chosen_atom = pcp.get_compounds( \" {chosen_atom} \" , 'name')[0].molecular_formula [EOL]" \
           f"product_elements = pcp.get_compounds( \"{entry['product']['product']}\" , 'name')[0].elements [EOL]" \
           f"result = chosen_atom in product_elements [EOL]"
    code = formulate_code(code)
    answer = execute_code(code)
    return entry['contexts'], question, code, answer


erronous = 0
success = 0
dataset = []
for entry in tqdm(get_next_entry()):
    try:
        cntx, q, c, a = generate_question_type1(entry)
        success += 1
        dataset.append(
            {
                "contex": cntx,
                "question": q,
                "code": c,
                "answer": a
            }
        )
    except Exception as e:
        # if str(e) == "Not an answer : float division by zero":
        #     continue
        erronous += 1

    try:
        cntx, q, c, a = generate_question_type2(entry)
        success += 1
        dataset.append(
            {
                "contex": cntx,
                "question": q,
                "code": c,
                "answer": a
            }
        )
    except Exception as e:
        # if str(e) == "Not an answer : float division by zero":
        #     continue
        erronous += 1

    try:
        cntx, q, c, a = generate_question_type3(entry)
        success += 1
        dataset.append(
            {
                "contex": cntx,
                "question": q,
                "code": c,
                "answer": a
            }
        )
    except Exception as e:
        # if str(e) == "Not an answer : float division by zero":
        #     continue
        erronous += 1

    try:
        cntx, q, c, a = generate_question_type4(entry)
        success += 1
        dataset.append(
            {
                "contex": cntx,
                "question": q,
                "code": c,
                "answer": a
            }
        )
    except Exception as e:
        # if str(e) == "Not an answer : float division by zero":
        #     continue
        erronous += 1

    try:
        cntx, q, c, a = generate_question_type5(entry)
        success += 1
        dataset.append(
            {
                "contex": cntx,
                "question": q,
                "code": c,
                "answer": a
            }
        )
    except Exception as e:
        # if str(e) == "Not an answer : float division by zero":
        #     continue
        erronous += 1

    try:
        cntx, q, c, a = generate_question_type6(entry)
        success += 1
        dataset.append(
            {
                "contex": cntx,
                "question": q,
                "code": c,
                "answer": a
            }
        )
    except Exception as e:
        # if str(e) == "Not an answer : float division by zero":
        #     continue
        erronous += 1

    try:
        cntx, q, c, a = generate_question_type7(entry)
        success += 1
        dataset.append(
            {
                "contex": cntx,
                "question": q,
                "code": c,
                "answer": a
            }
        )
    except Exception as e:
        # if str(e) == "Not an answer : float division by zero":
        #     continue
        erronous += 1

with open("package_questions/gpt4-parsed-simapi.json", "w") as f:
    json.dump(dataset, f, indent=4)

print(f"created a datset with {success} entries, erronous {erronous}, success rate {erronous / (erronous + success)}")
