import pubchempy as pcp
import random
import json

from tqdm import tqdm


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
        print("Error:", e)
        raise Exception("Not an answer")


def question_one(compound):
    code = f"""
import pubchempy as pcp

compound = pcp.get_compounds('{compound}', 'name')[0]
formula = compound.molecular_formula
count_O = formula.count('O')
count_C = formula.count('C')

predominant_atom = 'O' if count_O > count_C else 'C'
result = predominant_atom
"""

    answer = execute_code(code)

    return {
        "question": f"For the chemical compound '{compound}', which atom has a higher count: oxygen (O) or carbon (C)?",
        "code": code,
        "answer": answer
    }


def question_two(compound1, compound2):
    code = f"""
import pubchempy as pcp

methane = pcp.get_compounds('{compound1}', 'name')[0]
ethane = pcp.get_compounds('{compound2}', 'name')[0]

count_single_bonds_methane = methane.canonical_smiles.count('-')
count_single_bonds_ethane = ethane.canonical_smiles.count('-')

more_single_bonds = '{compound1}' if count_single_bonds_methane > count_single_bonds_ethane else '{compound2}'
result = more_single_bonds
"""

    answer = execute_code(code)

    return {
        "question": f"Based on their canonical SMILES representation, which compound has more single bonds: '{compound1}' or '{compound2}'?",
        "code": code,
        "answer": answer
    }


def question_three(compound1, compound2):
    code = f"""
import pubchempy as pcp

compound_1 = pcp.get_compounds('{compound1}', 'name')[0]
compound_2 = pcp.get_compounds('{compound2}', 'name')[0]

formula_1 = compound_1.molecular_formula
formula_2 = compound_2.molecular_formula

# Extracting the number of hydrogens from the molecular formula
def get_hydrogen_count(formula):
    if 'H' in formula:
        try:
            count_H = int(formula.split('H')[1].split('O')[0])
        except:
            try:
                count_H = int(formula.split('H')[1])
            except:
                count_H = 1
    else:
        count_H = 0
    return count_H

count_H1 = get_hydrogen_count(formula_1)
count_H2 = get_hydrogen_count(formula_2)

times = count_H1 / count_H2 if count_H2 != 0 else 'infinite'
result = times
"""

    answer = execute_code(code)

    return {
        "question": f"How many times more hydrogen atoms does '{compound1}' have compared to '{compound2}'?",
        "code": code,
        "answer": answer
    }


def question_four(compound1, compound2):
    code = f"""
import pubchempy as pcp

compound_1 = pcp.get_compounds('{compound1}', 'name')[0]
compound_2 = pcp.get_compounds('{compound2}', 'name')[0]

heavier_compound = '{compound1}' if compound_1.molecular_weight > compound_2.molecular_weight else '{compound2}'
result = heavier_compound
"""

    answer = execute_code(code)

    return {
        "question": f"Which is heavier: a single molecule of '{compound1}' or a single molecule of '{compound2}'?",
        "code": code,
        "answer": answer
    }


compound_list = [
    'Acetic acid', 'Acetone', 'Acetylene', 'Adenosine triphosphate', 'Aluminium oxide',
    'Ammonia', 'Amylase', 'Aniline', 'Anthracene', 'Arginine', 'Ascorbic acid', 'Asparagine',
    'Aspartic acid', 'Benzaldehyde', 'Benzamide', 'Benzoic acid', 'Benzyl alcohol', 'Biotin',
    'Bromine', 'Butane', 'Butanol', 'Butyric acid', 'Caffeine', 'Calcium carbonate',
    'Calcium chloride', 'Calcium oxide', 'Carbon tetrachloride', 'Cellulose', 'Chloroform',
    'Chlorine', 'Cholesterol', 'Citric acid', 'Cobalamin', 'Copper sulfate', 'Cysteine',
    'Diacetyl', 'Diaminobenzene', 'Diborane', 'Dicobalt octacarbonyl', 'Diethyl ether',
    'Dimethyl sulfoxide', 'Ethylene', 'Ethylene glycol', 'Fatty acid', 'Ferrocene', 'Fluorine',
    'Formic acid', 'Fructose', 'Galactose', 'Glucose', 'Glycerol', 'Glycine', 'Glycolic acid',
    'Guanine', 'Helium', 'Hexane', 'Histidine', 'Hydrochloric acid', 'Hydrogen peroxide',
    'Hydroquinone', 'Indigo dye', 'Iodine', 'Iron(III) chloride', 'Isobutylamine', 'Isopropanol',
    'Ketene', 'Lactic acid', 'Lactose', 'Lead(II) nitrate', 'Lithium chloride', 'Lysine',
    'Magnesium chloride', 'Magnesium oxide', 'Maltose', 'Manganese(II) chloride', 'Methionine',
    'Methyl acetate', 'Methylamine', 'Naphthalene', 'Neon', 'Nickel carbonyl', 'Nicotine',
    'Nitric acid', 'Nitrogen dioxide', 'Nitrous oxide', 'Octane', 'Oleic acid', 'Oxygen difluoride',
    'Palmitic acid', 'Pentane', 'Phenol', 'Phosgene', 'Phosphoric acid', 'Platinum hexafluoride',
    'Potassium bromide', 'Potassium chloride', 'Potassium iodide', 'Potassium nitrate',
    'Propene', 'Pyridine', 'Ribose', 'Rubidium bromide', 'Selenium hexafluoride', 'Silicon tetrachloride',
    'Sodium bicarbonate', 'Sodium chloride', 'Sodium hydroxide', 'Sodium sulfate', 'Starch',
    'Stearic acid', 'Sucrose', 'Sulfur hexafluoride', 'Tannic acid', 'Tartaric acid',
    'Thiamine', 'Toluene', 'Urea', 'Valine', 'Vanillin', 'Vitamin A', 'Vitamin D', 'Vitamin K',
    'Xylene', 'Zinc chloride', 'Zinc oxide'
]

data = []
nan1 = 0
nan2 = 0
nan3 = 0
nan4 = 0
# Randomly select two compounds.
for i in range(3):
    for compound in tqdm(compound_list):
        compound2 = random.choice(compound_list)
        while compound == compound2:
            compound2 = random.choice(compound_list)

        try:
            data.append(question_one(compound))
        except Exception as e:
            nan1 += 1

        compound2 = random.choice(compound_list)
        while compound == compound2:
            compound2 = random.choice(compound_list)
        try:
            data.append(question_two(compound, compound2))
        except Exception as e:
            nan2 += 1

        compound2 = random.choice(compound_list)
        while compound == compound2:
            compound2 = random.choice(compound_list)
        try:
            data.append(question_three(compound, compound2))
        except Exception as e:
            nan3 += 1

        compound2 = random.choice(compound_list)
        while compound == compound2:
            compound2 = random.choice(compound_list)
        try:
            data.append(question_four(compound, compound2))
        except Exception as e:
            nan4 += 1

# Write to a JSON file.
with open('package_questions/pcp.json', 'w') as file:
    json.dump(data, file, indent=4)

print(f"total entries number {len(data)}, erroneous : {nan1 + nan2 + nan3 + nan4}",
      f"erroneous questions = {[nan1 , nan2 , nan3 , nan4]}")
