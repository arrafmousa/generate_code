import random
import pandas as pd

# List of placeholder values for RA and Dec
# ra_values = [10.5, 15.2, 32.1, 42.8, 56.3]
# dec_values = [45.3, -30.1, 0.5, -12.9, 28.7]

# List of placeholder values for distance
distance_values = [10, 50, 100, 200, 500]

# Generate 10 different questions and corresponding code snippets
question_types = [
    "Coordinate Conversion",
    "Distance Calculation",
    "Celestial Object Name",
    "Redshift Calculation",
    "Magnitude Calculation",
    "Galactic Coordinates",
    "Angular Separation",
    "Orbital Period Calculation",
]

# Shuffle the question types
dataset = {"prompt": [], "code": [], "answer": []}
DATA_LENGTH = 5000
for entry in range(DATA_LENGTH):
    question_type = random.choice(question_types)
    if question_type == "Coordinate Conversion":
        # Coordinate Conversion Question
        # Randomly select RA and Dec values
        ra = round(random.uniform(0, 100), 2)
        dec = round(random.uniform(-90, 90), 2)

        # Craft the question
        question = f"Convert the equatorial coordinates (RA = {ra}, Dec = {dec}) of a celestial object to Galactic coordinates using Astropy. What are the Galactic coordinates (l and b)?"

        # Craft the code snippet
        code_snippet = f"""
from astropy.coordinates import SkyCoord

ra = {ra}  
dec = {dec} 
equatorial_coord = SkyCoord(ra=ra, dec=dec, unit="deg", frame="icrs")
galactic_coord = equatorial_coord.transform_to('galactic')
galactic_l = galactic_coord.l.deg  
galactic_b = galactic_coord.b.deg  
answer = (galactic_l, galactic_b)
"""

    elif question_type == "Distance Calculation":
        # Distance Calculation Question
        # Randomly select a distance value
        distance = random.choice(distance_values)

        # Craft the question
        question = f"Given a star with an absolute magnitude of 4.2, calculate the apparent magnitude at a distance of {distance} parsecs using Astropy."

        # Craft the code snippet
        code_snippet = f"""
from astropy import units as u
import numpy as np
from astropy.constants import L_sun

absolute_mag = 4.2
distance = {distance} * u.pc
apparent_mag = absolute_mag + 5 * (np.log10(distance / u.pc) - 1)
answer = apparent_mag
"""

    elif question_type == "Celestial Object Name":
        # Celestial Object Name Question
        # Randomly select RA and Dec values
        ra = round(random.uniform(0, 100), 2)
        dec = round(random.uniform(-90, 90), 2)

        # Craft the question
        question = f"What is the name of the celestial object located at RA = {ra} and Dec = {dec} using Astropy?"

        # Craft the code snippet
        code_snippet = f"""
from astropy.coordinates import SkyCoord

ra = {ra}  
dec = {dec} 
equatorial_coord = SkyCoord(ra=ra, dec=dec, unit="deg", frame="icrs")
object_name = equatorial_coord.to_string('hmsdms')
answer = object_name
"""

    elif question_type == "Redshift Calculation":
        # Redshift Calculation Question
        # Randomly select a redshift value
        redshift = random.uniform(0, 0.1)

        # Craft the question
        question = f"A galaxy is observed to have a redshift of {redshift}. Calculate its recessional velocity using Astropy."

        # Craft the code snippet
        code_snippet = f"""
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u

redshift = {redshift}
recessional_velocity = cosmo.H0 * redshift * cosmo.comoving_distance(redshift)
answer = recessional_velocity.to(u.km/u.s)
"""

    elif question_type == "Magnitude Calculation":
        # Magnitude Calculation Question
        # Randomly select a distance value
        distance = random.choice(distance_values)

        # Craft the question
        question = f"A star located at a distance of {distance} parsecs has an apparent magnitude of 6.2. Calculate its absolute magnitude using Astropy."

        # Craft the code snippet
        code_snippet = f"""
from astropy import units as u
import numpy as np
from astropy.constants import L_sun

apparent_mag = 6.2
distance = 50 * u.pc
absolute_mag = apparent_mag - 5 * (np.log10(distance / u.pc) - 1)
answer = absolute_mag
"""

    elif question_type == "Galactic Coordinates":
        # Galactic Coordinates Question
        # Randomly select RA and Dec values
        ra = round(random.uniform(0, 100), 2)
        dec = round(random.uniform(-90, 90), 2)

        # Craft the question
        question = f"What are the Galactic coordinates (l and b) of a celestial object located at RA = {ra} and Dec = {dec} using Astropy?"

        # Craft the code snippet
        code_snippet = f"""
from astropy.coordinates import SkyCoord

ra = {ra}  
dec = {dec}  
equatorial_coord = SkyCoord(ra=ra, dec=dec, unit="deg", frame="icrs")
galactic_coord = equatorial_coord.transform_to('galactic')
galactic_l = galactic_coord.l.deg  
galactic_b = galactic_coord.b.deg  
answer = (galactic_l, galactic_b)
"""

    elif question_type == "Angular Separation":
        # Angular Separation Question
        # Randomly select RA and Dec values for two celestial objects
        ra1 = round(random.uniform(0, 100), 2)
        dec1 = round(random.uniform(-90, 90), 2)
        ra2 = round(random.uniform(0, 100), 2)
        dec2 = round(random.uniform(-90, 90), 2)

        # Craft the question
        question = f"What is the angular separation between two celestial objects located at (RA = {ra1}, Dec = {dec1}) and (RA = {ra2}, Dec = {dec2}) using Astropy?"

        # Craft the code snippet
        code_snippet = f"""
from astropy.coordinates import SkyCoord

ra1 = {ra1}  
dec1 = {dec1}  
ra2 = {ra2} 
dec2 = {dec2}  
coord1 = SkyCoord(ra=ra1, dec=dec1, unit="deg", frame="icrs")
coord2 = SkyCoord(ra=ra2, dec=dec2, unit="deg", frame="icrs")
angular_sep = coord1.separation(coord2)
answer = angular_sep
"""

    elif question_type == "Orbital Period Calculation":
        # Orbital Period Calculation Question
        # Randomly select a distance value
        distance = random.choice(distance_values)

        # Craft the question
        question = f"Calculate the orbital period of a planet orbiting a star located at a distance of {distance} parsecs using Astropy."

        # Craft the code snippet
        code_snippet = f"""
from astropy import units as u
import numpy as np
from astropy.constants import G, M_sun

distance = {distance} * u.pc
star_mass = 1 * M_sun
orbital_period = (2 * np.pi * (distance**3 / (G * star_mass))**0.5).to(u.yr)
answer = orbital_period
"""

    # Print the question and corresponding code snippet
    # print(question)
    loc = {}
    exec(code_snippet, globals(), loc)
    code_snippet = code_snippet.replace("\n", "[EOL]")
    dataset["answer"].append(loc["answer"])
    dataset["prompt"].append(question)
    dataset["code"].append(code_snippet)

train_dataset = {"prompt": dataset["prompt"][:int(DATA_LENGTH * 0.7)],
                 "code": dataset["code"][:int(DATA_LENGTH * 0.7)],
                 "answer": dataset["answer"][:int(DATA_LENGTH * 0.7)]}
test_dataset = {"prompt": dataset["prompt"][int(DATA_LENGTH * 0.7):int(DATA_LENGTH * 0.85)],
                 "code": dataset["code"][int(DATA_LENGTH * 0.7):int(DATA_LENGTH * 0.85)],
                 "answer": dataset["answer"][int(DATA_LENGTH * 0.7):int(DATA_LENGTH * 0.85)]}
val_dataset = {"prompt": dataset["prompt"][int(DATA_LENGTH * 0.85):],
                 "code": dataset["code"][int(DATA_LENGTH * 0.85):],
                 "answer": dataset["answer"][int(DATA_LENGTH * 0.85):]}
pd.DataFrame.from_dict(train_dataset).to_csv("data/astropy_train.csv")
pd.DataFrame.from_dict(val_dataset).to_csv("data/astropy_val.csv")
pd.DataFrame.from_dict(test_dataset).to_csv("data/astropy_test.csv")
