import json
import random
import astropy
from datetime import datetime

def execute_code(code_str):
    try:
        # Create a namespace to hold the variables from executed code
        namespace = {}

        # Execute the code in the given namespace
        exec(code_str, namespace)

        # Retrieve the return value from the namespace
        return_value = namespace.get('result', None)

        return str(return_value)
    except Exception as e:
        print("Error:", e)
        raise Exception("Not an answer")


# Define the questions and their respective code answers
questions_and_answers = [
    {
        "question_template": "If a star has an apparent magnitude of {magnitude} in the V-band from Earth, and is located at a distance of {distance} parsecs, what would be its absolute magnitude?",
        "code_template": "import numpy as np\nfrom astropy import units as u\n\nmagnitude = {magnitude}\ndistance = {distance}\nabsolute_magnitude = magnitude - 5 * (np.log10(distance) - 1)\nresult = absolute_magnitude"
    },
    {
        "question_template": "Given the parallax angle of {parallax} arcseconds for a star, how far is it from Earth in light years?",
        "code_template": "from astropy import units as u\n\nparallax = {parallax}\ndistance_in_parsecs = 1.0 / parallax\ndistance_in_light_years = distance_in_parsecs * u.pc.to(u.lyr)\nresult = distance_in_light_years"
    },
    {
        "question_template": "When it's {time} UTC, what would be the solar zenith angle at latitude {latitude}° and longitude {longitude}°?",
        "code_template": "from astropy.coordinates import get_sun, EarthLocation, AltAz\nfrom astropy.time import Time\nfrom astropy import units as u\n\nlocation = EarthLocation(lat={latitude}*u.deg, lon={longitude}*u.deg)\ntime = Time('{time}')\naltaz = get_sun(time).transform_to(AltAz(obstime=time, location=location))\nzenith_angle = 90 * u.deg - altaz.alt\nresult = zenith_angle"
    },
    {
        "question_template": "Considering a binary star system with stars A and B at coordinates RA = {raA}°, Dec = {decA}° and RA = {raB}°, Dec = {decB}°, respectively, if star A goes supernova, at what angular separation would an observer on Earth start noticing the effects on star B?",
        "code_template": "from astropy.coordinates import SkyCoord\nfrom astropy import units as u\n\nstarA = SkyCoord(ra={raA}*u.degree, dec={decA}*u.degree, frame='icrs')\nstarB = SkyCoord(ra={raB}*u.degree, dec={decB}*u.degree, frame='icrs')\nangular_separation = starA.separation(starB)\nresult = angular_separation"
    },
    {
        "question_template": "Given a celestial body with coordinates RA = {ra}° and Dec = {dec}°, what will be its altitude above the horizon at {time} local time for an observer located at latitude = {latitude}° and longitude = {longitude}°?",
        "code_template": "from astropy.coordinates import SkyCoord, EarthLocation, AltAz\nfrom astropy.time import Time\nfrom astropy import units as u\n\nbody = SkyCoord(ra={ra}*u.degree, dec={dec}*u.degree, frame='icrs')\nlocation = EarthLocation(lat={latitude}*u.deg, lon={longitude}*u.deg)\ntime = Time('{time}')\naltaz = body.transform_to(AltAz(obstime=time, location=location))\naltitude = altaz.alt\nresult = altitude"
    },
    {
        "question_template": "How long will it take for light to travel from Proxima Centauri, the nearest star to Earth, to our planet?",
        "code_template": "from astropy import units as u\n\nproxima_distance = 4.24  # in light years\ntime_taken = proxima_distance * u.year\nresult = time_taken"
    }
]

dataset = []

# Generate random data for each question
for idx, qa in enumerate(questions_and_answers):
    for _ in range(250):  # Generate 150 questions from each template
        magnitude = random.uniform(0, 15)
        ra = random.uniform(0, 360)
        dec = random.uniform(-90, 90)
        parallax = random.uniform(0.01, 100)
        time = datetime.now().strftime('%Y-%m-%d') + random.choice(["T00:00:00", "T12:00:00", "T18:00:00", "T23:59:59"])
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        raA = random.uniform(0, 360)
        decA = random.uniform(-90, 90)
        raB = random.uniform(0, 360)
        decB = random.uniform(-90, 90)
        distance = random.uniform(0.1, 10000)  # in parsecs

        question = qa["question_template"].format(magnitude=magnitude, ra=ra, dec=dec, parallax=parallax, time=time, latitude=latitude, longitude=longitude, raA=raA, decA=decA, raB=raB, decB=decB, distance=distance)
        code = qa["code_template"].format(magnitude=magnitude, ra=ra, dec=dec, parallax=parallax, time=time, latitude=latitude, longitude=longitude, raA=raA, decA=decA, raB=raB, decB=decB, distance=distance)
        answer = execute_code(code)
        dataset.append({
            "question": question,
            "code": code,
            "answer":answer
        })

# Save to a JSON file
with open('package_questions/astropy.json', 'w') as f:
    json.dump(dataset, f, indent=4)

print(len(dataset))
print("package_questions/astropy.json")