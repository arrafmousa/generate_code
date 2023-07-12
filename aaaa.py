import pubchempy as pcp
from function_calls import *

import pubchempy as pcp
import function_calls


def generated_code():
    desired_product = to_gr(' 13.63 g ')
    product_described = to_gr(' 8.68 g ')
    described_component = to_gr(' 9.25 g ')
    needed_reactor = desired_product / product_described * described_component
    reactor_molar_weight = pcp.get_compounds(" Dimethylsulfoxide ", 'name')[0].exact_mass
    return (needed_reactor / float(reactor_molar_weight))


ret_vale = generated_code()