import os
from flask import Flask, session, render_template, url_for, redirect, request
# To do: Add fields to frontend
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  # global city, square_footage, electricity_use, vehicle_type, annual_mileage, is_electric, mpg, public_type, week_mileage, flying_hours, frequency_of_meat, meat_type, clothes, waste_comparison, compost_organic, recycle_percentage
  if request.method == 'POST':
    city = request.form['city_list']
    oil_usage = int(request.form['oil_usage'])
    gas_usage = int(request.form['gas_usage'])
    # square_footage = int(request.form['square_footage'])
    electricity_use = int(request.form['electricity_use'])
    vehicle_type = int(request.form['vehicle_type'])
    annual_mileage = int(request.form['annual_mileage'])
    mpg = int(request.form['mpg'])
    fuel = int(request.form['fuel'])
    is_electric = request.form['is_electric']
    flying_hours = int(request.form['flying_hours'])
    # public_type = int(request.form['public_type'])
    # week_mileage = int(request.form['week_mileage'])
    frequency_of_meat = int(request.form['frequency_of_meat'])
    meat_type = request.form['meat_type']
    clothes = int(request.form['clothes'])
    waste_comparison = int(request.form['waste_comparison'])
    compost_organic = request.form['compost_organic']
    recycle_percentage = int(request.form['recycle_percentage'])
    calculate_carbon_footprint(city, oil_usage, gas_usage, electricity_use, vehicle_type, annual_mileage, mpg, fuel, is_electric, flying_hours, frequency_of_meat, meat_type, clothes, waste_comparison, compost_organic, recycle_percentage)
    return redirect(url_for('results'))
  else:
    return render_template('index.html')

@app.route('/results')
def results():
  try:
    return render_template('results.html', results=resultsText)
  except NameError:
    return render_template('index.html')
carbon_factor = 0

cities = [
  "Fairbanks, AK", "Juneau, AK", "Anchorage, AK", "Barrow, AK",
  "Grand Forks, ND", "Minneapolis, MN", "Milwaukee, WI", "Chicago, IL",
  "Indianapolis, IN", "New York City, NY", "Boston, MA", "Philadelphia, PA",
  "Pittsburgh, PA", "Cleveland, OH", "St. Louis, MO", "Kansas City, MO",
  "Denver, CO", "Dallas, TX", "Houston, TX", "Atlanta, GA", "Miami, FL",
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

def calculate_carbon_footprint(city, oil_usage, gas_usage, electricity_use, vehicle_type, annual_mileage, mpg, fuel, is_electric, flying_hours, frequency_of_meat, meat_type, clothes, waste_comparison, compost_organic, recycle_percentage):
  # print("This calculator is only available for residents in the United States as various factors differ drastically in different countries.")
  # print("Note: this calculator does not provide an accurate value it only provides a rough estimate of your carbon footprint")
  # print(cities)
  # city = input("Where do you live? (City, State): ")
  oil_usage = float(input("How much heating oil do you use in a month? (gallons) "))
  q1 = (oil_usage * 12 / 10.19) / 1000
  # gas_usage = float(input("How much therms of gas do you use in a month? "))
  # tell the user that they can find it on their monthly gas bill
  q2 = gas_usage * 0.00529 * 12
  # electricity_use = float(input("How much electricity do you use every month? (kWh): "))
  q3 = (electricity_use * 12 * 0.000433)
  # vehicle_type = int(input("Do you travel by motorcycle or car? (Type 1 for motorcycle, 2 for car, and 3 for bus, and 4 for train. "))
  # while vehicle_type not in [1, 2,3,4,]:
  #   print("Invalid vehicle type. Please enter 1 for motorcycle, 2 for car, 3 for bus, 4 for train, .")
  #   vehicle_type = int(input("Do you travel by motorcycle or car? (Type 1 for motorcycle, 2 for car, 3 for bus, 4 for train,): "))
  if vehicle_type == 1:
    # annual_mileage = float(input("What is your annual mileage? "))
    # mpg = float(input("How efficient is your motorcycle? (MPG): "))
    # fuel = int(input("Does your car run on Diesel or Gasoline? Type 1 for Diesel and 2 for Gasoline. "))
    if fuel == 1:
      carbon_factor = 8.78
    elif fuel == 2:
      carbon_factor = 10.19
    fcr = 1 / mpg
    q4 = (annual_mileage * fcr * carbon_factor) / 1000
  elif vehicle_type == 2:
    # annual_mileage = float(input("What is your annual mileage? "))
    # mpg = float(input("How efficient is your motorcycle? (MPG): "))
    # is_electric = input("Does your car an electric car? (Y/N) ")
    if is_electric == 'N' or 'n':
      # fuel = int(input("Does your car run on Diesel or Gasoline? Type 1 for Diesel and 2 for Gasoline. "))
      if fuel == 1:
        carbon_factor = 8.78
      elif fuel == 2:
        carbon_factor = 10.19
      fcr = 1 / mpg
    if is_electric.lower() == 'y':
      q4 = (annual_mileage * fcr * 33.7 * 0.855) / 2000
    else:
      q4 = (annual_mileage * fcr * carbon_factor) / 1000
  elif vehicle_type == 3:
    # annual_mileage = float(input("how many miles in a week do you you travel with bus? "))
    q4 = (annual_mileage * 0.39 * 52) / 2000
  elif vehicle_type == 4:
    # annual_mileage = float(input("How many miles in a week do you travel by train? "))
    q4 = (annual_mileage * 1.609 * 42.12) / 1000
  # flying_hours = float(input("How many hours a year do you fly? "))
  q5 = flying_hours * 0.242
  # frequency_of_meat = float(input("How many times a week do you eat meat? "))
  if frequency_of_meat != 0:
    # meat_type = input("What type of meat do you consume the most? (Beef, Chicken, Pork, Lamb): ")
    meat_intensity = get_meat_intensity(meat_type)
    q6 = (frequency_of_meat * 52 * meat_intensity) / 1000
  else:
    q6 = 0
  # clothes = int(input("How many clothes do you buy per year? "))
  q7 = (clothes * 10) / 1000
  # waste_comparison = int(input("How much waste do you produce compared to your neighbors? (1-Much More, 2-A Little More, 3-Same, 4-Less, 5-Much Less): "))
  # while waste_comparison not in [1, 2, 3, 4, 5]:
  #   print("Invalid waste comparison. Please enter a number from 1 to 5.")
  #   waste_comparison = int(
  #     input(
  #       "How much waste do you produce compared to your neighbors? (1-Much More, 2-A Little More, 3-Same, 4-Less, 5-Much Less): "
  #     ))
  q8 = get_waste_comparison_value(waste_comparison)
  # compost_organic = input("Do you compost organic waste? (Y/N): ")
  # while compost_organic.lower() not in ['y', 'n']:
  #   print("Invalid input. Please enter 'Y' for yes or 'N' for no.")
  #   compost_organic = input("Do you compost organic waste? (Y/N): ")
  q9 = -1.6 if compost_organic.lower() == 'y' else 0
  # recycle_percentage = float(input("Do you recycle all your waste? (Percentage): "))
  # while recycle_percentage < 0 or recycle_percentage > 100:
  #   print("Invalid recycle percentage. Please enter a value between 0 and 100.")
  #   recycle_percentage = float(input("Do you recycle all your waste? (Percentage): "))
  q10 = 3.2 - (3.2 * recycle_percentage / 100)
  carbon_footprint = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10
  carbon_footprint = round(carbon_footprint, 1)
  print(f"\nYour estimated carbon annual footprint is {carbon_footprint} tons CO2e per year.")

if __name__ == '__main__':
  app.run()
