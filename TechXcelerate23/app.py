import os
from flask import Flask, session, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global city, square_footage, electricity_use, vehicle_type, annual_mileage, is_electric, mpg, public_type, week_mileage, flying_hours, frequency_of_meat, meat_type, clothes, waste_comparison, compost_organic, recycle_percentage
    if request.method == 'POST':
        city = request.form['cityList']
        square_footage = int(request.form['square_footage'])
        electricity_use = int(request.form['electricity_use'])
        vehicle_type = int(request.form['vehicle_type'])
        annual_mileage = int(request.form['annual_mileage'])
        is_electric = request.form['is_electric']
        mpg = int(request.form['mpg'])
        public_type = int(request.form['public_type'])
        week_mileage = int(request.form['week_mileage'])
        flying_hours = int(request.form['flying_hours'])
        frequency_of_meat = int(request.form['frequency_of_meat'])
        meat_type = request.form['meat_type']
        clothes = int(request.form['clothes'])
        waste_comparison = int(request.form['waste_comparison'])
        compost_organic = request.form['compost_organic']
        recycle_percentage = int(request.form['recycle_percentage'])
        calculate_carbon_footprint()
        return redirect(url_for('results'))
    else:
        return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html', results=resultsText)

cities = [
    "Fairbanks, AK", "Juneau, AK", "Anchorage, AK", "Barrow, AK", "Grand Forks, ND",
    "Minneapolis, MN", "Milwaukee, WI", "Chicago, IL", "Indianapolis, IN", "New York City, NY",
    "Boston, MA", "Philadelphia, PA", "Pittsburgh, PA", "Cleveland, OH", "St. Louis, MO",
    "Kansas City, MO", "Denver, CO", "Dallas, TX", "Houston, TX", "Atlanta, GA", "Miami, FL",
    "Los Angeles, CA", "San Francisco, CA", "Seattle, WA", "Portland, OR"
]

def get_heating_degree_days(city):
    hdd_data = {
        "Fairbanks, AK": 13000,
        "Juneau, AK": 10000,
        "Anchorage, AK": 7500,
        "Barrow, AK": 17000,
        "Grand Forks, ND": 9000,
        "Minneapolis, MN": 6500,
        "Milwaukee, WI": 5500,
        "Chicago, IL": 6000,
        "Indianapolis, IN": 5000,
        "New York City, NY": 5000,
        "Boston, MA": 4500,
        "Philadelphia, PA": 4000,
        "Pittsburgh, PA": 4500,
        "Cleveland, OH": 5000,
        "St. Louis, MO": 5000,
        "Kansas City, MO": 4500,
        "Denver, CO": 5500,
        "Dallas, TX": 3500,
        "Houston, TX": 3000,
        "Atlanta, GA": 3500,
        "Miami, FL": 1000,
        "Los Angeles, CA": 2000,
        "San Francisco, CA": 1500,
        "Seattle, WA": 3000,
        "Portland, OR": 2500
    }

    return hdd_data.get(city, 0)


def get_meat_intensity(meat):
    meat_intensity_data = {
        "Beef": 16.5,
        "Chicken": 6.9,
        "Pork": 12.2,
        "Lamb": 22.7
    }

    return meat_intensity_data.get(meat, 0)


def get_waste_comparison_value(waste_comparison):
    comparison_data = {
        1: 2.6,  # Much more
        2: 1.95,  # A little more
        3: 1.3,  # Same
        4: 0.975,  # Less
        5: 0.65  # Much less
    }

    return comparison_data.get(waste_comparison, 0)


def calculate_carbon_footprint():
    global resultsText
    q4 = 0
    q5 =0
    q6 =0
    q7 =0
    q8 = 0
    q9 = 0
    q10 = 0


    print("This calculator is only available for residents in the United States as various factors differ drastically in different countries.")
    print("Note: this calculator does not provide an accurate value, it only provides a rough estimate of your carbon footprint.")

    hdd = get_heating_degree_days(city)
    q2 = 0.0000002 * int(square_footage) * hdd
    
    carbon_intensity = 0.85
    q3 = (electricity_use * carbon_intensity * 12) / 1000

    if vehicle_type == 1:
        fcr = 1 / mpg
        q4 = (annual_mileage * fcr * 250) / 10000

    elif vehicle_type == 2:

        fcr = 1 / mpg

        if is_electric.lower() == 'yes':
            q4 = (annual_mileage * fcr * 0.43) / 10000
        else:
            q4 = (annual_mileage * fcr * 200) / 10000

    else:

        miles_in_week = None
        if public_type == 1:
            q4 = (miles_in_week * 52) * (1 / 150) / 100
        elif public_type == 2:
            q4 = (miles_in_week * 52) * (1 / 273) / 100

        else: q4 = (miles_in_week * 52) * (1/300) / 100

        q5 = (flying_hours * 0.5 * 2.7) / 2000

        if frequency_of_meat > 0:

            meat_intensity = get_meat_intensity(meat_type)
            q6 = (frequency_of_meat * 52 * meat_intensity) / 1000

        else:
            q6 = 0

        q7 = (clothes * 10) / 1000

        q8 = get_waste_comparison_value(waste_comparison)

        q9 = -1.6 if compost_organic.lower() == 'yes' else 0

        q10 = 3.2 - (3.2 * recycle_percentage / 100)

    carbon_footprint = q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10

    formatted_carbon_footprint = "{:.1f}".format(carbon_footprint)

    resultsText = f"\nYour estimated carbon footprint is {formatted_carbon_footprint} tons CO2e per year."
    return redirect(url_for('results'))

if __name__ == '__main__':
	app.run()