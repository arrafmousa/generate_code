import pubchempy as pcp
import re

def compensate_for_loss(loss="0%", current_value=0) -> float:
    amount = re.search(r"(\d+\.*\d+)", loss).group()
    if "%" in loss:
        return current_value * (100 / (float(amount) + 100))
    else:
        return current_value + float(amount)


def to_mg(product_described):
    if 'mg' in product_described or 'mL' in product_described or 'ml' in product_described:
        proudct_in_mg = float(re.search("(\d+\.?\d*)", product_described).group())
    elif 'g' in product_described or 'gr' in product_described or 'L' in product_described:
        proudct_in_mg = float(re.search("(\d+\.?\d*)", product_described).group()) * 1000
    else:
        assert 'kg' in product_described
        proudct_in_mg = float(re.search("(\d+\.?\d*)", product_described).group()) * 1000000
    return proudct_in_mg


def to_gr(product_described):
    if 'mg' in product_described or 'mL' in product_described or 'ml' in product_described:
        proudct_in_gr = float(re.search("(\d+\.?\d*)", product_described).group()) / 1000
    elif 'g' in product_described or 'gr' in product_described or 'L' in product_described:
        proudct_in_gr = float(re.search("(\d+\.?\d*)", product_described).group())
    else:
        if 'kg' not in product_described:
            print(product_described)
        proudct_in_gr = float(re.search("(\d+\.?\d*)", product_described).group()) * 1000
    return proudct_in_gr


def normalize_component_to_100mg_product(components, product_described):
    # todo: delegate to another function - but i want to minimize the functions that are used
    portions = product_described / 100

    normalize_components = []
    for comp in components:
        quantity = to_mg(comp[1])
        component_in_mg = quantity / portions
        normalize_components.append([comp[0], component_in_mg])
    return normalize_components


def compensate_for_loss(loss="0%", current_value=0) -> float:
    amount = re.search(r"(\d+\.*\d+)", loss).group()
    if "%" in loss:
        return current_value * (100 / (float(amount) + 100))
    else:
        return current_value + float(amount)


def to_minute(ss):
    return 1
