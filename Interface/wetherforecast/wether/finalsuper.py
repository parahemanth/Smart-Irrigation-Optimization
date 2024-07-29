from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
Watertime = float(input("Enter The Watering Time in Hours:"))


def convert_to_12_hour_format(time_str):
    try:
        # Split the time string into hours and minutes
        hours, minutes = map(int, time_str.split(':'))
        # Check if it's midnight (24:00)
        if hours == 24:
            return "12:00 AM"
        # Determine AM or PM
        period = "AM" if hours < 12 else "PM"

        # Convert hours to 12-hour format
        hours = hours % 12

        # Handle midnight (12:00 AM)
        if hours == 0:
            hours = 12
        if time == '12:30 AM':
            print(dates[0])
        elif time == '01:30 AM':
            print(dates[1])
        elif time == '12:30 AM':
            print(dates[2])
        # Format the time in 12-hour format
        time_12_hour = f"{hours:02d}:{minutes:02d} {period}"

        return time_12_hour
    except ValueError:
        return "Invalid time format"


time_data = []
rainfall_data = []
superdata = []
actualtemp = []
windflow_data = []
time_intervals = []
rainfall_values = []
maxrainfall = []
maxtime = []
humidity_data = []
uv_indexdata = []
cloud_data = []
rain_data = []
reports_data = []
website = f'https://weather.com/en-IN/weather/hourbyhour/l/c5a9b7379c7fecf334f2a6d13c384ef5dd4dc1e678193e98da6ad6686bef255c'
request = requests.get(website)
content = request.text
soup = BeautifulSoup(content, 'lxml')
h3_elements = soup.find_all(
    'h3', class_='DetailsSummary--daypartName--kbngc', attrs={'data-testid': 'daypartName'})
for h3 in h3_elements:
    time_data.append(h3.text.strip())
title = soup.find('span', class_='LocationPageTitle--PresentationName--1AMA6')
print(title.text)
date = soup.find_all('h2', class_='HourlyForecast--longDate--J_Pdh')
dates = [element.get_text() for element in date]
print(dates)
temp = soup.find_all('div', class_='DetailsSummary--temperature--1kVVp')
rainfall = soup.find_all('div', class_='DetailsSummary--precip--1a98O')
reports = soup.find_all('div', class_='DetailsSummary--condition--2JmHb')
for ra in rainfall:
    data1 = ra.find('span')
    rain_data.append(data1.text)
for report in reports:
    data = report.find('span')
    reports_data.append(data.text)
for x in temp:
    rain = x.find('span')
    actualtemp.append(rain.text)
all_data = soup.find_all('ul', class_='DetailsTable--DetailsTable--3Bt2T')
for singledata in all_data:
    singledata.find('div', class_='DetailsTable--field--CPpc_')
    spandata = singledata.find_all('span')
    for tag in spandata:
        if 'data-testid' in tag.attrs:
            if tag['data-testid'] == 'PercentageValue':
                percentage = tag.get_text()
                humidity_data.append(percentage)
            elif tag['data-testid'] == 'AccumulationValue':
                rain_amount = tag.get_text()
                rainfall_data.append(rain_amount)
            elif tag['data-testid'] == 'Wind':
                windflow = tag.get_text()
                windflow_data.append(windflow)
humidity_actual_data = humidity_data[1::2]
cloud_cover = humidity_data[::2]
print("Time     Temperature    Cloud cover %   Humidity %     rain%        Rain Amount mm     wind flow direction        situation           \n")
for i, (time, temp, humidity, rain, repo, radata,  wind, cloud) in enumerate(zip(time_data[0:24], actualtemp[0:24], humidity_actual_data[0:24],  rainfall_data[0:24],   rain_data[0:24], reports_data[0:24], windflow_data[0:24], cloud_cover[0:24])):
    if rain != '0 cm' or (rain == '0 cm' and (rainfall_data[i-1] != '0 cm' or rainfall_data[(i+1) % len(rainfall_data)] != '0 cm')):
        rainfall_values.append(rain)
        time_intervals.append(time)
    ctime = convert_to_12_hour_format(time)
    print(f"{ctime}:      {temp}         {humidity}           {cloud}             {repo}         {rain}                {wind}          {radata}       ")


def avgprediction(time_intervals, rainfall_values):
    time_hours = [datetime.strptime(
        time, '%H:%M').hour for time in time_intervals]
    # Convert rainfall values to millimeters
    rainfall_mm = []
    for value in rainfall_values:
        if 'mm' in value:
            rainfall_mm.append(float(value.split()[0]))
        elif 'cm' in value:
            # Convert cm to mm (1 cm = 10 mm)
            rainfall_mm.append(float(value.split()[0]) * 10)
        else:
            rainfall_mm.append(0.0)
    rainfall_model = LinearRegression()
    rainfall_model.fit(np.array(time_hours).reshape(-1, 1),
                       np.array(rainfall_mm))
    next_24_hours = np.array(range(1, 25)).reshape(-1, 1)
    predicted_rainfall = rainfall_model.predict(next_24_hours)
    total_predicted_rainfall = sum(predicted_rainfall)
    rainy_time_hours = [
        30 if 'mm' in value else 0 for value in rainfall_values]
    rainy_time_model = LinearRegression()
    rainy_time_model.fit(np.array(time_hours).reshape(-1,
                         1), np.array(rainy_time_hours))
    predicted_rainy_time = rainy_time_model.predict(next_24_hours)
    total_predicted_rainy_time = int(
        sum(predicted_rainy_time) / 60)  # Convert minutes to hours
    # print(f"\nTotal Avg Predicted Rainfall for the Next 24 Hours: {total_predicted_rainfall:.2f} mm")
    # print(f"Total Avg  Predicted Rainy Time for the Next 24 Hours: {total_predicted_rainy_time} hours")


def minprediction(time, rain):
    time_hours = [datetime.strptime(time, '%H:%M').hour for time in time]
    rainfall_mm = []
    for value in rain:
        if 'mm' in value:
            rainfall_mm.append(float(value.split()[0]))
        elif 'cm' in value:
            # Convert cm to mm (1 cm = 10 mm)
            rainfall_mm.append(float(value.split()[0]) * 10)
        else:
            rainfall_mm.append(0.0)
    rainfall_model = LinearRegression()
    rainfall_model.fit(np.array(time_hours).reshape(-1, 1),
                       np.array(rainfall_mm))
    next_24_hours = np.array(range(1, 25)).reshape(-1, 1)
    predicted_rainfall = rainfall_model.predict(next_24_hours)
    total_predicted_rainfall = sum(predicted_rainfall)
    rainy_time_hours = [30 if 'mm' in value else 0 for value in rainfall_data]
    rainy_time_model = LinearRegression()
    rainy_time_model.fit(np.array(time_hours).reshape(-1,
                         1), np.array(rainy_time_hours))
    predicted_rainy_time = rainy_time_model.predict(next_24_hours)
    total_predicted_rainy_time = int(
        sum(predicted_rainy_time) / 60)  # Convert minutes to hours
    print(
        f" \nTotal Predicted Rainfall for the Next 24 Hours: {total_predicted_rainfall:.2f} mm")
    print(
        f"Total Predicted Rainy Time for the Next 24 Hours: {total_predicted_rainy_time} hours")
    return [total_predicted_rainfall, total_predicted_rainy_time]


l = []
VMC = float(input("Enter The VMC Percentage: "))
Depth = float(input("Enter The Depth of Soil Sensor (mm):"))
Soil_Water = VMC*Depth/100
l.append(Soil_Water)
l.extend(minprediction(time_data, rainfall_data))
total_got = l[0]+l[1]
total_required = 33.00
total_balance = total_required-total_got
if total_balance <= 0:
    print("No Need for watering")
else:
    k1 = Watertime/8
    k2 = k1*total_balance
    print("Total Watering Time : " + str(int(k2*60)) + " minutes")
