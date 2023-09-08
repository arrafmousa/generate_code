import random
import re
import numpy as np

from function_calls import to_stu

weight_units = ['mg', 'kg', 'g']
volume_units = ['ml', 'L', 'litre']


def randomize_product_amount(quantity):
    if quantity == 'NAV':
        return 'NAV'
    amount_unit_split = quantity.split()
    try:
        float(amount_unit_split[0])
    except Exception as e:
        raise Exception("Failed to randomize new amount of product - No product quantity")
    amount_unit_split[0] = float(amount_unit_split[0]) * (random.uniform(0, 2))
    amount_unit_split[1] = random.choice(weight_units) if amount_unit_split[1] in weight_units else \
        amount_unit_split[1]
    amount_unit_split[1] = random.choice(weight_units) if amount_unit_split[1] in volume_units else \
        amount_unit_split[1]
    return "{:.2f}".format(amount_unit_split[0]) + " " + amount_unit_split[1]


def randomize_unit(old_unit):
    if old_unit in weight_units:
        unit = random.choice(weight_units)
    elif old_unit in volume_units:
        unit = random.choice(volume_units)
    else:
        return ''
    return unit


def randomize_ingredients(entry: dict):
    randomized_ingredients = []
    for ingredient in list(entry):
        reactant, quantity = ingredient.values()
        old_quantity = re.findall(r'[\w\S]+|\d+', quantity)
        # print(old_quantity, "  ",end='')
        if len(old_quantity) != 2:
            randomized_ingredients.append({"reactant": reactant, "quantity": 'NA'})
            # print(quantity, "continuing")
            continue
        try:
            float(old_quantity[0])
        except:
            randomized_ingredients.append({"reactant": reactant, "quantity": 'NA'})
            # print("continuing")
            continue
        new_unit = randomize_unit(old_quantity[1])
        new_quantity = round(np.abs(np.random.normal(float(old_quantity[0]), random.uniform(1, 2), 1))[0], 2)
        # print(new_quantity, new_unit)
        randomized_ingredients.append({"reactant": reactant, "quantity": str(new_quantity) + ' ' + new_unit})
    return randomized_ingredients

def wtf():
    g = 5+5
    return  g

def make_ingredients_list(ingredients):
    parsed = []
    for ingredient in ingredients:
        parsed.append([ingredient["reactant"], ingredient["quantity"]])
    return parsed


def make_ingredients_string(ingredients):
    parsed = ''
    for ingredient in ingredients:
        parsed += ingredient["quantity"] + ' of ' + ingredient["reactant"] + ' '
    return parsed

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

def generate_duration(row, desired_output):
    if type(row) != dict:
        row = {"context":row}
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


def execute_code(code_str):
    try:
        # Create a namespace to hold the variables from executed code
        namespace = {}

        # Execute the code in the given namespace
        exec(code_str, namespace)

        # Retrieve the return value from the namespace
        return_value = namespace.get('result', None)

        return return_value
    except Exception as e:
        # print("Error:", e)
        raise Exception("Not an answer : "+str(e))
