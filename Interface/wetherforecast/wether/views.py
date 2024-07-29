from django.shortcuts import render, redirect
from .models import Data
from .models import CropType
from django.shortcuts import HttpResponse
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
import requests as rs
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import json
from sklearn.linear_model import LinearRegression
# Create your views here
global place
global watering_time
watering_time = 0

global paddy

global corn

global chilli

global cotton


def home(request):
    a = []
    crop_types = CropType.CROP_CHOICES
    for i in range(1, 11):
        a.append(i)
    if request.method == "POST":

        # Assuming you have a form field named "hours"
        hours = request.POST.get("hours")
        place = request.POST.get("loca")
        crop_type = request.POST.get("crop_type")

        # Redirect to the process view with the POST data as query parameters
        return redirect("process", hours=hours, place=place, crop_type=crop_type)

    datas = Data.objects.all()
    context = {
        'datas': datas,
        'hours': a,
        'crop_types': crop_types
    }
    return render(request, 'home.html', context)


def process(request, hours, place, crop_type):

    if request.method == "POST":

        return redirect("waterd", place=place)

     # post_data = request.POST
    Watertime = hours
    print(Watertime)

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
    crop_obj = CropType.objects.get(crop_type=crop_type)
    crop_type_timefield = int(crop_obj.time_frame)
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
    # place = post_data.get("loca")
    if (place == "Narasaraopet"):
        website = f'https://weather.com/en-IN/weather/hourbyhour/l/62cfbba42fb966e5816f6357072052202fea1ca83d805f3fe0a46d4ab4c0535d'
    elif (place == "Guntur"):
        website = f'https://weather.com/en-IN/weather/hourbyhour/l/b2e1f87fe0f7a92ba70229d148ad9288ee1e5b3621294eb40d7a0041353769d0'
    elif (place == "vijayawada"):
        website = f'https://weather.com/en-IN/weather/hourbyhour/l/8c41d5deb79057bfd46d061ab978048014850037d15cf2015c8a9dad2e74fd96'
    elif (place == "Pinavu"):
        website = f'https://weather.com/en-IN/weather/hourbyhour/l/7517135d125623483dadcbcc2cc525e94f95d211336a3faf504bbfabdef5c548'
    elif (place == "Bhimavaram"):
        website = f'https://weather.com/en-IN/weather/hourbyhour/l/fb3823bcfc000d4d07a7b3b0021029a30123308f3391bbbf305ac7a7ecfb04b8'
    elif (place == "Florida"):
        website = f'https://weather.com/en-IN/weather/hourbyhour/l/9d1dfeac04208c562168a78ecc29aa383e7d77a14bf7f5bfb75046b7ab1a4def'
    elif (place == "Eluru"):
        website = f"https://weather.com/en-IN/weather/hourbyhour/l/98b021c1cbcf2c68dea49d1aeef4d1f00deffbf06028f225c8652b0fab3aea58"
    req = rs.get(website)
    content = req.text
    soup = BeautifulSoup(content, 'lxml')
    h3_elements = soup.find_all(
        'h2', class_='DetailsSummary--daypartName--kbngc', attrs={'data-testid': 'daypartName'})
    for h3 in h3_elements:
        time_data.append(h3.text.strip())
    title = soup.find(
        'span', class_='LocationPageTitle--PresentationName--1AMA6')
    print(title.text)
    location = title.text
    date = soup.find_all('h2', class_='HourlyForecast--longDate--J_Pdh')
    dates = [element.get_text() for element in date]
    print(dates)
    temp = soup.find_all(
        'div', class_='DetailsSummary--temperature--1kVVp')
    rainfall = soup.find_all('div', class_='DetailsSummary--precip--1a98O')
    reports = soup.find_all(
        'div', class_='DetailsSummary--condition--2JmHb')
    for ra in rainfall:
        data1 = ra.find('span')
        rain_data.append(data1.text)
    for report in reports:
        data = report.find('span')
        reports_data.append(data.text)
    for x in temp:
        rain = x.find('span')
        actualtemp.append(rain.text)
    all_data = soup.find_all(
        'ul', class_='DetailsTable--DetailsTable--3Bt2T')
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
        rainfall_model.fit(
            np.array(time_hours).reshape(-1, 1), np.array(rainfall_mm))
        next_24_hours = np.array(range(1, 25)).reshape(-1, 1)
        predicted_rainfall = rainfall_model.predict(next_24_hours)
        total_predicted_rainfall = sum(predicted_rainfall)
        rainy_time_hours = [
            30 if 'mm' in value else 0 for value in rainfall_values]
        rainy_time_model = LinearRegression()
        rainy_time_model.fit(
            np.array(time_hours).reshape(-1, 1), np.array(rainy_time_hours))
        predicted_rainy_time = rainy_time_model.predict(next_24_hours)
        total_predicted_rainy_time = int(
            sum(predicted_rainy_time) / 60)  # Convert minutes to hours
        print(
            f"\nTotal Avg Predicted Rainfall for the Next 24 Hours: {total_predicted_rainfall:.2f} mm")
        print(
            f"Total Avg  Predicted Rainy Time for the Next 24 Hours: {total_predicted_rainy_time} hours")

    def minprediction(time, rain):
        time_hours = [datetime.strptime(t, '%H:%M').hour for t in time]
        rainfall_mm = []
        rainy_time_minutes = []

        for value in rain:
            if 'mm' in value:
                rainfall_mm.append(float(value.split()[0]))
            elif 'cm' in value:
                rainfall_mm.append(float(value.split()[0]) * 10)
            else:
                rainfall_mm.append(0.0)

        for mm in rainfall_mm:
        # Assume linear relationship between rainfall amount and rainy time
            rainy_time_minutes.append(mm * 30)  # Adjust this coefficient as needed

        rainfall_model = LinearRegression()
        rainfall_model.fit(np.array(time_hours).reshape(-1, 1),np.array(rainfall_mm))
        next_24_hours = np.array(range(1, 25)).reshape(-1, 1)
        predicted_rainfall = rainfall_model.predict(next_24_hours)
        total_predicted_rainfall = sum(predicted_rainfall)

        rainy_time_model = LinearRegression()
        rainy_time_model.fit(np.array(time_hours).reshape(-1, 1),np.array(rainy_time_minutes))
        predicted_rainy_time = rainy_time_model.predict(next_24_hours)
        total_predicted_rainy_time = sum(predicted_rainy_time) / 60  # Convert minutes to hours
        print(
        f"Total Predicted Rainfall for the Next 24 Hours: {total_predicted_rainfall:.2f} mm")
        print(
        f"Total Predicted Rainy Time for the Next 24 Hours: {total_predicted_rainy_time:.2f} hours")
        return [total_predicted_rainfall, total_predicted_rainy_time]
     
    website = "https://thingspeak.com/channels/2564034/feeds.json?results=2"
    response = rs.get(website)

    if response.status_code == 200:
        data = json.loads(response.text)

        # Access field1 and field2 values from the JSON data
        field1_values = [feed['field1'] for feed in data['feeds']]

        print(field1_values[1])
        # print(field2_values)
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
    l = []
    Sensor_Value = int(field1_values[1])
    # INPUT FROM SOIL MOISTURE SENSOR
    Soil_Water = Sensor_Value*50*0.45*0.01
    l.append(Soil_Water)
    l.extend(minprediction(time_data, rainfall_data))
    rainfall_mm = l[1]
    rain_hours = l[2]
    # print(rainfall_mm)
    # print(rain_hours)
    total_got = l[0]+l[1]

    if crop_type == 'paddy':
        total_required = 7
    elif crop_type == 'chilli':
        total_required = 9
    elif crop_type == 'corn':
        total_required = 12.6
    elif crop_type == 'cotton':
        total_required = 16
    else:
        total_required = 7

    total_balance = total_required-total_got
    if total_balance <= 0:
        watering_time = 0
        print("No Need for watering")
    else:
        # global watering_time
        k1 = Watertime/total_required
        k2 = k1*total_balance
        watering_time = str(int(k2*60))
        watering_time = int(watering_time)

        # print("Total Watering Time : " + watering_time + " minutes")
    task = get_object_or_404(Data, locations=place)
    context = {
        'sensor': Sensor_Value,
        'location': location,
        'water_time': watering_time,
        'rainfall_mm': rainfall_mm,
        'rain_hours': rain_hours,
        'place': place,
        'data': task,
        'crop_kind': crop_type,
        'time_frame': crop_type_timefield
    }

    return render(request, 'process.html', context)


def water(request, place):
    if request.method == "POST":
        # Update the 'done' field
        task = get_object_or_404(Data, locations=place)
        task.done = True
        task.save()

        website = f"https://api.thingspeak.com/update?api_key=7AI0YJRHGEZ6GB4L&field1={watering_time}"
        rs.get(website)

        context = {

            'task': task
        }

        return render(request, 'waterd.html', context)
    else:
        return HttpResponse("invalid request")
