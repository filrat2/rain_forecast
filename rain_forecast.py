# -*- coding: utf-8 -*-

# import needed modules
from requests import get
from csv import writer, reader
from datetime import date
import sys

# %% define function for export/save data to *.csv file


def write_csv(data, filepath):
    with open(filepath, 'w', newline='') as csv_file:
        write = writer(csv_file)
        for element in data:
            write.writerow(element.split(","))


# %% check arguments passed by user by sys.argv

if len(sys.argv) == 3:
    api_key = sys.argv[1]
    user_input_date = sys.argv[2]
elif len(sys.argv) == 2:
    api_key = sys.argv[1]
    user_input_date = str(date.today())
elif len(sys.argv) < 2:
    print("\nPodano za mało argumentów za pomocą 'sys.argv'.\n"
          "Program do działania wymaga dwóch lub trzech argumentów:\n"
          "rain_forecast.py << klucz API >> << data w formacie YYYY-MM-DD >>\n"
          "lub\n"
          "rain_forecast.py << klucz API >>.\n\n"
          "Działanie programu zakończone.")
    sys.exit()
else:
    print("\nPodano za dużo argumentów za pomocą 'sys.argv'.\n"
          "Program do działania wymaga dwóch lub trzech argumentów:\n"
          "rain_forecast.py << klucz API >> << data w formacie YYYY-MM-DD >>\n"
          "lub\n"
          "rain_forecast.py << klucz API >>.\n\n"
          "Działanie programu zakończone.")
    sys.exit()

if len(user_input_date) != 10:
    print("\nNieprawidłowy format daty.\n"
          "Prawidłowy format to YYYY-MM-DD, np. 2022-10-10.\n\n"
          "Działanie programu zakończone.")
    sys.exit()

# %% variables to downlad data from API

url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"

# coordinates for Poznań
latitude = 52.40692
longitude = 16.92993

querystring = {"lat": latitude, "lon": longitude}

headers = {
    "X-RapidAPI-Key": f"{api_key}",
    "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
}

# %% variables to open/read data from *.csv file

FILEPATH = "checked_days.csv"

csv_file = reader(open(FILEPATH))
lines_from_csv = list(csv_file)

dictionary_CSV = {}

# %% load data from *.csv file to dict

for element in lines_from_csv:
    dictionary_CSV[f"{element[0]}"] = {
        'precip': float(element[1]),
        'snow': float(element[2])
        }

# %% main 'if/elif/else' statetments

if user_input_date in dictionary_CSV.keys():
    if (dictionary_CSV[f'{user_input_date}']['precip'] > 0 and
            dictionary_CSV[f'{user_input_date}']['snow'] > 0):
        print(f"\nW dniu {user_input_date} w Poznaniu "
              "będzie padać śnieg z deszczem :(")

    elif dictionary_CSV[f'{user_input_date}']['precip'] > 0:
        print(f"\nW dniu {user_input_date} w Poznaniu "
              "będzie padać deszcz! Zabierz ze sobą parasol :)")

    elif dictionary_CSV[f'{user_input_date}']['snow'] > 0:
        print(f"\nW dniu {user_input_date} w Poznaniu "
              "będzie padać śnieg! Ubierz coś ciepłego :)")

    else:
        print(f"\nW dniu {user_input_date} w Poznaniu nie będzie padać! "
              "Miłego dnia :)")

else:
    print("\nPobieram dane z API.")
    dictionary_API = {}
    r = get(url, headers=headers, params=querystring)
    response = r.json()
    weather_forecast_data = response['data']

    for day in weather_forecast_data:
        dictionary_API[f"{day['datetime']}"] = {
            'precip': day['precip'],
            'snow': day['snow']
            }

    if user_input_date in dictionary_API.keys():
        if (dictionary_API[f'{user_input_date}']['precip'] > 0 and
                dictionary_API[f'{user_input_date}']['snow'] > 0):
            print(f"\nW dniu {user_input_date} w Poznaniu "
                  "będzie padać śnieg z deszczem :(")

        elif dictionary_API[f'{user_input_date}']['precip'] > 0:
            print(f"\nW dniu {user_input_date} w Poznaniu "
                  "będzie padać deszcz! Zabierz ze sobą parasol :)")

        elif dictionary_API[f'{user_input_date}']['snow'] > 0:
            print(f"\nW dniu {user_input_date} w Poznaniu "
                  "będzie padać śnieg! Ubierz coś ciepłego :)")

        else:
            print(f"\nW dniu {user_input_date} w Poznaniu nie będzie padać! "
                  "Miłego dnia :)")

    else:
        print(f"\nNie wiem czy w dniu {user_input_date} będzie padać "
              "w Poznaniu!")

# write/save data to *.csv file
    list_for_write_csv = []
    for key, day in zip(dictionary_API.keys(), dictionary_API):
        string = (f"{key},{dictionary_API[day]['precip']},"
                  f"{dictionary_API[day]['snow']}")
        list_for_write_csv.append(string)

    write_csv(list_for_write_csv, FILEPATH)

# %%
