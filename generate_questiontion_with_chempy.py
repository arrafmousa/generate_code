import random
import re

import chempy
from chemlib import Compound
import pubchempy as pcp

# -------- \begin constants ----------------------
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
not_a_compound_list = ["the", "was", "and", "get", "of", "in", "as", "an"]


# -------- \end constants ----------------------


# -------- \begin question types ----------------------
def if_the_temprature_passes(row):
    if re.search("If the temperature passes", row["context"]) is None:
        return None, None, None, None
    else:
        additional_info = re.search(
            "If the temperature passes \d+ degrees when heating .* for more than \d+ seconds .*", row["context"])
        temp_threshold_str = re.findall("\d+ degrees", additional_info.group())
        heat_duration_str = re.findall("\d+ seconds", additional_info.group())
        loss_str = re.findall("loss of (\D*\d+\.?\d* [grams|milligrams|\%]+)", additional_info.group())
        name = re.findall(" when heating (.*) for more", additional_info.group())

        return temp_threshold_str, loss_str, heat_duration_str, name


def We_discovered_that_if_the_amount_of(row):
    if re.search("We discovered that if the amount of", row["context"]) is None:
        return None, None
    else:
        additional_info = re.search(
            "We discovered that if the amount of .*", row["context"])
        quantity_threshold = re.findall("above (\D*\d+\.?\d* [grams|milligrams|\%]+)", additional_info.group())
        threshold_comp_name = re.findall("the amount of (.*) in", additional_info.group())
        temp_threshold_str = re.findall("the temperature is less than (\D*\d+\.?\d* degrees)", additional_info.group())
        loss_str = re.findall("the product of the process decreases by (\d+\%)", additional_info.group())
        return temp_threshold_str, loss_str, quantity_threshold, threshold_comp_name


def overheat_the(row):
    if re.search("Overheat the .*", row["context"]) is None:
        return None, None, None
    else:
        additional_info = re.search(
            "Overheat the .*", row["context"])
        temp_threshold_str = re.findall("the temperature is above (\D*\d+\.?\d* degrees)", additional_info.group())
        decrease_ratio_str = re.findall("for each (\d+\.\d+ [second|hour]+)", additional_info.group())
        loss_str = re.findall("a loss of (\D*\d+\.?\d* [grams|milligrams|ml|ML\%]+)", additional_info.group())
        product_name = re.findall("Overheat the (.*) will result", additional_info.group())

        return temp_threshold_str, loss_str, decrease_ratio_str, product_name


def if_we_heat(row):
    if re.search("If we heat .*", row["context"]) is None:
        return None, None
    else:
        additional_info = re.search(
            "If we heat .*", row["context"])
        temp_threshold_str = re.findall("to temperature higher than (\D*\d+\.?\d* degrees)", additional_info.group())
        loss_str = re.findall("at a rate of (\D*\d+\.?\d* [grams|milligrams|milliliters|\%]+) per minute.",
                              additional_info.group())
        name = re.findall("If we heat (.*) to tem", additional_info.group())
        return temp_threshold_str, loss_str, name


def stirring_the_mixture_longer(row):
    if re.search("stirring the mixture longer.*", row["context"]) is None:
        return None, None
    else:
        additional_info = re.search(
            "stirring the mixture longer.*", row["context"])
        loss_str = re.findall("will cause a loss of (\D*\d+\.?\d* [grams|milligrams|milliliters|\%]+)",
                              additional_info.group())
        decrease_ratio_str = re.findall("for each (minute|hour) above the original time",
                                        additional_info.group())
        name = ["the mixture"]
        return loss_str, decrease_ratio_str, name


def if_the_temperature_exceed(row):
    if re.search(" If the temperature exceed .*", row["context"]) is None:
        return None, None
    else:
        additional_info = re.search(
            "If the temperature exceed .*", row["context"])
        temp_threshold_str = re.findall("If the temperature exceed (\D*\d+\.?\d* degrees)",
                                        additional_info.group())
        decrease_ratio_str = re.findall("it will result in (\d+\% decrease) in the final products",
                                        additional_info.group())
        name = re.findall("when heating (.*) it will result", additional_info.group())
        return temp_threshold_str, decrease_ratio_str, name


def if_we_cool_the_mixture(row):
    if re.search("If we cool the mixture.*", row["context"]) is None:
        return None, None
    else:
        additional_info = re.search(
            "If we cool the mixture.*", row["context"])
        temp_threshold_str = re.findall("below (\D*\d+\.?\d* degrees)",
                                        additional_info.group())
        decrease_ratio_str = re.findall("the product of the process decreases by (\d+\%)",
                                        additional_info.group())
        name = ["the mixture"]
        return temp_threshold_str, decrease_ratio_str, name


# -------- \end question types ----------------------


# --------- \begin function for generating the question -------
def randomize_product_amount(vars_and_vals):
    weight_units = ['gr', 'mg', 'kg']
    volume_units = ['mL', 'L']

    product_amount = vars_and_vals[1]
    amount_unit_split = product_amount.split()
    amount_unit_split[0] = float(amount_unit_split[0]) * (random.uniform(0, 2))
    amount_unit_split[1] = random.choice(weight_units) if amount_unit_split[1] in weight_units else \
        amount_unit_split[1]
    amount_unit_split[1] = random.choice(weight_units) if amount_unit_split[1] in volume_units else \
        amount_unit_split[1]
    return "{:.2f}".format(amount_unit_split[0]) + " " + amount_unit_split[1]


def generate_reactors(components):
    available_reactors = ""
    reactors_list = []
    for comp in components:
        if comp[0].startswith("("):
            comp[0] = comp[0][1:]
        if random.random() < 0.2:  # w.p. 20% change the units
            weight_units = ['gr', 'mg', 'kg']
            volume_units = ['mL', 'L']
            amount_unit_split = comp[1].split()
            if amount_unit_split[1] == 'g':
                amount_unit_split[1] = 'gr'
            amount_unit_split[1] = random.choice(weight_units) if amount_unit_split[1] in weight_units else \
                amount_unit_split[1]
            amount_unit_split[1] = random.choice(weight_units) if amount_unit_split[1] in volume_units else \
                amount_unit_split[1]
            amount_unit_split[0] = str(float(amount_unit_split[0]) * (random.uniform(0, 2)))
            available_reactors += amount_unit_split[0] + " " + amount_unit_split[1] + " of " + comp[0] + ", "
            reactors_list.append([amount_unit_split[0], amount_unit_split[1]])
        else:
            available_reactors += comp[1] + " of " + comp[0] + ", "
            reactors_list.append([comp[1], comp[0]])
    return available_reactors, reactors_list


def get_vars_from_question(q_vars):
    variables = q_vars.split(", ")
    code_vars = "["
    for var in variables[:-1]:
        amount_name = var.split(" of ")
        amount_name[1] = amount_name[1].replace("'", "")
        amount_name[0] = amount_name[0].replace("'", "")
        code_vars += f"( ' {amount_name[1]} ' , ' {amount_name[0]} ' ) ,"
    return code_vars + "]"


def get_reactors_and_output(row):
    context = row["context"]
    check2switch = "\(\d+\.?\d* mmol, \d+\.?\d* mg\)|\(\d+\.?\d* mmol, \d+\.?\d* g\)\(\d+\.?\d* mmol, \d+\.?\d* mL\)\(\d+\.?\d* mmol, \d+\.?\d* gr\)\(\d+\.?\d* mmol, \d+\.?\d* ml\)"
    while re.search(check2switch, context) is not None:
        cc = re.search(check2switch, context)
        split_to_reorder = re.split("\(|,|\)", cc.group())
        context = context.replace(cc.group(), "( " + split_to_reorder[2] + ", " + split_to_reorder[1] + " )")
    split_by_sentence = context.split(". ")
    if len(split_by_sentence[-1]) == 0:
        dropped_additional = context.replace(split_by_sentence[-2], '')
        # dropped_additional = dropped_additional.replace(split_by_sentence[-3], '')
        start_search = -3
    else:
        dropped_additional = context.replace(split_by_sentence[-1], '')
        # dropped_additional = dropped_additional.replace(split_by_sentence[-2], '')
        start_search = -2

    succeed = False
    while not succeed:
        try:
            product_amount = re.search("(\d+\.?\d* g)|(\d+\.?\d* mg)|(\d+\.?\d* mL)|(\d+\.?\d* ml)",
                                       split_by_sentence[start_search]).group()
        except:
            if start_search < -20:
                return None, None
            start_search -= 1
            continue
        succeed = True

    vars_and_vals_list = re.split("(\d+\.?\d* g)|(\d+\.?\d* mg)|(\d+\.?\d* mL)|(\d+\.?\d* ml)", dropped_additional)
    vars_and_vals_list = [i for i in vars_and_vals_list if i is not None and i is not '']
    for item in vars_and_vals_list:
        if re.search("[a-z]+", item) is None:
            vars_and_vals_list.remove(item)
    vars_and_vals = []
    for i in range(len(vars_and_vals_list) // 2):
        if re.search("(\d+\.?\d* g)|(\d+\.?\d* mg)|(\d+\.?\d* mL)|(\d+\.?\d* ml)",
                     vars_and_vals_list[2 * i]) is not None:
            prev_sentence = vars_and_vals_list[2 * i + 1].split()
            vars_and_vals.append(
                [prev_sentence[0] if len(prev_sentence) == 1 else (
                    prev_sentence[1][1:] if prev_sentence[1].startswith("(") else prev_sentence[1]),
                 vars_and_vals_list[2 * i]])
        else:
            idx = -1
            comp_name = ""
            prev_parts = vars_and_vals_list[2 * i].split()
            while re.search("[a-z|0-9]+", comp_name) is None:
                comp_name += prev_parts[idx]
                idx -= 1
            vars_and_vals.append(
                [comp_name[1:] if comp_name.startswith("(") else comp_name, vars_and_vals_list[2 * i + 1]])
    return vars_and_vals, product_amount


def get_time_from_question(question):
    return re.findall(", for (.*),", question)[0]


def generate_duration(row, desired_output):
    # function_lists = [if_the_temprature_passes, We_discovered_that_if_the_amount_of, overheat_the, if_we_heat,
    #                   stirring_the_mixture_longer, if_the_temperature_exceed, if_we_cool_the_mixture]
    generated_temp, temp_threshold_str, loss_str, generated_duration, heat_duration_str, name = None, None, None, None, None, None
    unit = None

    if None not in if_the_temprature_passes(row):
        temp_threshold_str, loss_str, heat_duration_str, name = if_the_temprature_passes(row)
        generated_temp = float(temp_threshold_str[0].split()[0]) + random.randint(-100, 100)
        generated_duration = float(re.findall("(\d+)", heat_duration_str[0])[0]) + random.randint(0, 10)
        unit = random.choice(["minutes", "hours"])
        question = f"if we heat to {generated_temp} degrees, for {generated_duration} {unit}, how much of the initial reactors to get {desired_output} of the final product?"

    if None not in We_discovered_that_if_the_amount_of(row):
        temp_threshold_str, loss_str, quantity_threshold, threshold_comp_name = We_discovered_that_if_the_amount_of(row)
        generated_temp = float(temp_threshold_str[0].split()[0]) + random.randint(-100, 100)
        generated_duration = random.randint(0, 10)
        generate_quantity = float(quantity_threshold[0].split()[0]) + random.uniform(
            float(quantity_threshold[0].split()[0]), 10)
        unit = random.choice(["minutes", "hours"])
        question = f"if the {threshold_comp_name[0]} was over {generate_quantity}, we cool the mixture to {generated_temp} degrees, for {generated_duration} {unit}, how much of the initial reactors to get {desired_output} of the final product?"

    if None not in overheat_the(row):
        temp_threshold_str, loss_str, decrease_ratio_str, product_name = overheat_the(row)
        generated_temp = float(temp_threshold_str[0].split()[0]) + random.randint(-100, 100)
        generated_duration = random.randint(0, 10)
        unit = random.choice(["minutes", "hours"])
        question = f"if we heat the {product_name[0]} to {generated_temp} degrees, for {generated_duration} {unit}, how much of the initial reactors to get {desired_output} of the final product?"

    if None not in if_we_heat(row):
        temp_threshold_str, loss_str, name = if_we_heat(row)
        generated_temp = float(temp_threshold_str[0].split()[0]) + random.randint(-100, 100)
        generated_duration = random.randint(0, 10)
        unit = random.choice(["minutes", "hours"])
        question = f"if we heat the {name[0]} to {generated_temp} degrees, for {generated_duration} {unit}, how much of the initial reactors to get {desired_output} of the final product?"

    if None not in stirring_the_mixture_longer(row):
        loss_str, _, name = stirring_the_mixture_longer(row)
        name = name[0]
        generated_temp = random.randint(-100, 100)
        unit = random.choice(["minutes", "hours"])
        generated_duration = random.randint(1, 10) if unit == "hours" else random.choice([30 * i for i in range(20)])
        question = f"if we heat the {name} to {generated_temp} degrees, for {generated_duration} {unit}, how much of the initial reactors to get {desired_output} of the final product?"

    if None not in if_the_temperature_exceed(row):
        temp_threshold_str, loss_str, name = if_the_temperature_exceed(row)
        unit = random.choice(["minutes", "hours"])
        generated_duration = random.randint(1, 10) if unit == "hours" else random.choice([30 * i for i in range(20)])
        generated_temp = float(temp_threshold_str[0].split()[0]) + random.randint(-100, 100)
        question = f"if we heat the {name} to {generated_temp} degrees, for {generated_duration} {unit}, how much of the initial reactors to get {desired_output} of the final product?"

    if None not in if_we_cool_the_mixture(row):
        temp_threshold_str, loss_str, name = if_we_cool_the_mixture(row)
        unit = random.choice(["minutes", "hours"])
        generated_duration = random.randint(1, 10) if unit == "hours" else random.choice([30 * i for i in range(20)])
        generated_temp = float(temp_threshold_str[0].split()[0]) + random.randint(-50, 50)
        question = f"if we cool the {name} to {generated_temp} degrees, for {generated_duration} {unit}, how much of the initial reactors to get {desired_output} of the final product?"

    return generated_temp, temp_threshold_str, loss_str, str(
        generated_duration) + " " + unit, heat_duration_str, name, question


# ---------  \end function for generating the question -------


def generate_question_type5(row):
    vars_and_vals = get_reactors_and_output(row)
    question = "how many moles of the product does the process yield ?"
    try:
        if vars_and_vals[0][-1][0] in not_a_compound_list:
            raise NameError
        validity_check = pcp.get_compounds(vars_and_vals[0][-1][0], 'name')[0].exact_mass
    except:
        return "", ""
    code = f"molar_mass = pcp.get_compounds( \"{vars_and_vals[0][-1][0]}\", 'name')[0].exact_mass [EOL]" \
           f"molar_mass = float ( molar_mass ) [EOL]" \
           f"yielded_grams = to_gr(\" {vars_and_vals[0][-1][1]} \") [EOL]" \
           f"return  yielded_grams  /  molar_mass  [EOL]"
    return question, code


def generate_question_type6(row):  # debugged
    vars_and_vals = get_reactors_and_output(row)
    product_quantity = vars_and_vals[0][-1]
    desired_output = randomize_product_amount(vars_and_vals)
    try:
        reactor_chosen = random.choice(vars_and_vals[0][:-1])
    except:
        return "", ""
    reactor_name = reactor_chosen[0]
    reactor_weight = reactor_chosen[1]
    try:
        if reactor_name in not_a_compound_list:
            raise NameError
        validity_check = pcp.get_compounds({reactor_name}, 'name')[0].exact_mass
    except:
        return "", ""
    question = f"how many moles of {reactor_name} do we need to get {desired_output} of the product ?"
    code = f"desired_product = to_gr( ' {desired_output} ' ) [EOL]" \
           f"product_described = to_gr( ' {product_quantity[1]} ' ) [EOL]" \
           f"described_component = to_gr( ' {reactor_weight} ') [EOL]" \
           f"needed_reactor = desired_product / product_described * described_component [EOL]" \
           f"reactor_molar_weight = pcp.get_compounds( \"{reactor_name}\" , 'name')[0].exact_mass [EOL]" \
           f"return ( needed_reactor / float( reactor_molar_weight ) ) [EOL]"
    return question, code


def generate_question_type7(row):  # debugged
    vars_and_vals = get_reactors_and_output(row)
    chosen_atom = random.choice(atoms_list).strip()
    compound_name = vars_and_vals[0][-1][0].replace('.', '')
    try:
        if compound_name in not_a_compound_list:
            raise NameError
        validity_check = pcp.get_compounds(compound_name, 'name')[0].elements
    except:
        return "", ""
    print("detected compound : ", compound_name)
    question = f"Is {chosen_atom} present in the product ?"
    code = f"chosen_atom = pcp.get_compounds( \" {chosen_atom} \" , 'name')[0].molecular_formula [EOL]" \
           f"product_elements = pcp.get_compounds( \"{compound_name}\" , 'name')[0].elements [EOL]" \
           f"return chosen_atom in product_elements [EOL]"
    return question, code


def generate_question_type1(row):  # debugged
    vars_and_vals = get_reactors_and_output(row)
    desired_output = randomize_product_amount(vars_and_vals)
    question_1 = f"how much do we need from each of the reactors to get {desired_output} of the final product ?"  # TODO V2 : add an environmental condtion
    code_1 = f"desired_product = to_gr( \" {desired_output} \" )[EOL]" \
             f"components = {vars_and_vals[0][:-1]} [EOL]" \
             f"product_described = to_gr( \" {vars_and_vals[1]} \" )[EOL]" \
             f"portions_needed = ( desired_product ) /100 [EOL]" \
             f"needed_reactors = [[reactor [ 0 ] , to_gr( reactor [ 1 ] ) * portions_needed] for reactor in components] [EOL]" \
             f"return needed_reactors [EOL]"
    return question_1, code_1


def generate_question_type2(row): # debugged
    vars_and_vals = get_reactors_and_output(row)
    q_vars, q_list = generate_reactors(vars_and_vals[0][:-1])
    q_list = [[q[1],q[0]] for q in q_list]
    if len(vars_and_vals[0][:-1]) < 1:
        return "", ""
    question2 = f"we have {q_vars}, how can we optimize the process?"  # TODO V2 : add an environmental conditions
    code2 = f"components = {vars_and_vals[0][:-1]} [EOL]" \
            f"have_components = {q_list} [EOL]" \
            f"min_portion = float( 'inf' ) [EOL]" \
            f"for component, needed in zip ( components , have_components ) : [EOL]" \
            f"[TAB]portions = to_gr( component [ 1 ] ) / to_gr( needed [ 1 ] ) [EOL]" \
            "[TAB]if portions < min_portion : [EOL]" \
            "[TAB][TAB]min_portion = portions [EOL]" \
            "optimized = [] [EOL]" \
            "for need, have in zip ( components , have_components ) : [EOL]" \
            "[TAB]optimized.append( [ have[0] , to_gr( have [1] ) - to_gr ( need [1] ) * min_portion ] ) [EOL]" \
            "return optimized [EOL]"
    return question2, code2


def generate_question_type3(row):  # debugged
    vars_and_vals = get_reactors_and_output(row)
    q_vars, q_list = generate_reactors(vars_and_vals[0][:-1])
    question_3 = f"we have {q_vars} how much can we create of the final product?"  # TODO V2 : add an environmental conditions
    code_3 = f"available_reactors = {get_vars_from_question(q_vars)} [EOL]" \
             f"components =  {vars_and_vals[0][:-1]} [EOL]" \
             f"product_described = to_gr( \" {vars_and_vals[1]} \" ) [EOL]" \
             f"minimal_product_portion = float( 'inf' ) [EOL]" \
             f"for needed, have in zip ( components , available_reactors ): [EOL]" \
             f"[TAB]tmp_min_portion = to_gr( have [ 1 ] ) / to_gr( needed[1] ) [EOL]" \
             f"[TAB]if tmp_min_portion < minimal_product_portion : [EOL]" \
             f"[TAB][TAB]minimal_product_portion = tmp_min_portion [EOL]" \
             f"return minimal_product_portion * product_described [EOL]"
    return question_3, code_3


def generate_question_type4(row): # CONTINUE HEREEEE
    vars_and_vals = get_reactors_and_output(row)
    desired_output = randomize_product_amount(vars_and_vals)
    generated_temp, temp_threshold_str, loss_str, generated_duration, heat_duration_str, name, question_4 = generate_duration(
        row, desired_output)
    if heat_duration_str is None:
        return None, None
    code_4 = f"time = to_minute( \" {get_time_from_question(question_4)} \" ) [EOL]" \
             f"loss = \'{loss_str[0]}\' [EOL]" \
             f"components = {vars_and_vals[0][:-1]} [EOL]" \
             f"described_product_amount = to_gr( \" {desired_output} \" ) [EOL]" \
             f"threshold_duration = to_minute( \" {heat_duration_str} \" ) [EOL]" \
             f"temprature = {generated_temp} [EOL]" \
             f"threshold_temp = {temp_threshold_str} [EOL]" \
             f"final_product_amount = described_product_amount [EOL]" \
             f"for t in range( time ): [EOL]" \
             f"[TAB]if t > threshold_duration and temprature > threshold_temp: [EOL]" \
             f"[TAB][TAB]final_product_amount = compensate_for_loss( loss= loss[0], current_value= final_product_amount) [EOL]" \
             f"portions = final_product_amount / described_product_amount [EOL]" \
             f"return [[component[0], to_gr(component[1]) * portions] for component in components] [EOL]"
    return question_4, code_4

# print(pcp.get_compounds('1-chloro-2-[6-(4-fluorophenyl)indol-3-yl]ethanone', 'name')[0])
