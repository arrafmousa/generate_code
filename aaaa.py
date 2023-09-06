import pubchempy as pcp

compound_1 = pcp.get_compounds('Acetic acid', 'name')[0]
compound_2 = pcp.get_compounds('Butyric acid', 'name')[0]

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