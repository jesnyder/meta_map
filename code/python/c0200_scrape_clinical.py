from bs4 import BeautifulSoup
import json
import lxml
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import re
import requests
import shutil
import pandas as pd
import pandas_read_xml as pdx
import time

from c0001_retrieve_meta import retrieve_path
from c0001_retrieve_meta import retrieve_ref
from c0001_retrieve_meta import retrieve_datetime
from clinicalstudies_gov_scanner import ClinicalTrial
from find_color import find_color


def scrape_clinical():
    """
    Objective: Scrape clinical trial information from NIH ClinicalTrials.gov
    Search terms saved in a user provided document

    Tasks:

        *** manual process ***
        a. Navigate to clinicaltrials.gov
        b. Manually search and download results
        c. Save the .csv to user_provided clinical_trials

        *** automated ***
        1. Make one comprehensive dataframe
        2. Scrape json using url from DataFrame
        2. Find unique values

        *** not implemented ***
        3.
        4.

    """

    tasks = [6]

    if 1 in tasks: aggregate_trials()
    if 2 in tasks: scrape_json()
    if 3 in tasks: df_from_json()
    if 4 in tasks: scrape_gps()
    if 5 in tasks: count_trials()
    if 6 in tasks: csv_to_xlsx()

    if 7 in tasks: map_clinical()

def map_clinical():
    ""

    ""

    df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined_v03' + '.csv')
    df = pd.read_csv(df_save)

    df = df.sort_values('Enrollment', ascending=False)

    lat = list(df['lat'])
    lon = list(df['lon'])
    enrollment = list(df['Enrollment'])
    title = list(df['Title'])

    plt.close('all')
    figure, axes = plt.subplots()

    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)

    fontSize = retrieve_ref('fontSize')
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : fontSize}
    plt.rc('font', **font)
    plt.rc('font', size=fontSize)
    plt.rc('axes', titlesize=fontSize)

    # place blank map in background
    blank_map_file_list = os.listdir(retrieve_path('blank_map'))
    blank_map_file = blank_map_file_list[0]
    blank_map_file= os.path.join(retrieve_path('blank_map'), blank_map_file )
    img = plt.imread(blank_map_file)
    extent = [-170, 190, -58, 108]
    axes.imshow(img, extent=extent)

    for i in range(len(lat)):

        if df.at[i, 'Country'] == None:
            continue


        try:
            marker, edge, alpha = find_color(len(title[i]))
            print('colors retrieved.')

            print('enrollment[i] = ' + str(enrollment[i]))
            size =  int(enrollment[i] + 2)
            if size > 100: size = 100
            print('size = ' + str(size))

            plt.scatter(lon[i], lat[i], s=size, color=marker, edgecolors=edge, alpha=alpha, linewidths=0.1)

            """
            #plt.scatter(lon[i], lat[i], s = size, color=color[0], edgecolors=color[1], alpha=color[2], linewidths=0.1)
            """

        except:
            continue


    map_save = os.path.join(retrieve_path('map_clinical'), 'map' + '.png')
    plt.savefig(map_save, dpi = int(retrieve_ref('dpi')))
    print('plot saved: ')
    print(map_save)



def csv_to_xlsx():
    """
    Copy and save dataframe as a excel file
    """
    for f in os.listdir(retrieve_path('df_clinical')):
        name, ext = os.path.splitext(f)
        if 'csv' in ext:
            src = os.path.join(retrieve_path('df_clinical'), name + '.csv')
            dst =  os.path.join(retrieve_path('df_clinical'), name + '.xlsx')
            print('src = ')
            print(src)
            print('dst = ')
            print(dst)
            shutil.copyfile(src, dst)


def scrape_gps():
    """

    """

    df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined_v02' + '.csv')
    df = pd.read_csv(df_save)

    df['lat'] = [None] * len(list(df['Unnamed: 0']))
    df['lon'] = [None] * len(list(df['Unnamed: 0']))
    df['map_url'] = [None] * len(list(df['Unnamed: 0']))
    del df['Unnamed: 0']

    facilities = list(df['Facility'])
    zipcodes = list(df['Zipcode'])
    cities = list(df['City'])
    countries = list(df['Country'])

    print('facilities = ')
    print(facilities)

    for i in range(len(facilities)):

        df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined_v03' + '.csv')
        df.to_csv(df_save)
        csv_to_xlsx()

        if countries[i] == None:
            continue

        print('Completeness: ' + str(100*i/len(facilities)))

        url = 'https://nominatim.openstreetmap.org/search/'
        zipcode = str(zipcodes[i])
        city = str(cities[i])
        city = city.replace(' ', '+')
        url = url + zipcode + '+' + city
        url = url + '?format=json'

        try:
            response = requests.get(url).json()

            lat = response[0]["lat"]
            lon = response[0]["lon"]

            print(response[0]["lat"])
            print(response[0]["lon"])

            df.at[i, "lat"] = lat
            df.at[i, "lon"] = lon
            df.at[i, "map_url"] = url

            print('url = ')
            print(url)

            continue

        except:
            lat, lon = None, None

            df.at[i, "lat"] = lat
            df.at[i, "lon"] = lon
            df.at[i, "map_url"] = url

        url = 'https://nominatim.openstreetmap.org/search/'
        zipcode = str(zipcodes[i])
        city = str(cities[i])
        city = city.replace(' ', '+')
        country = str(countries[i])
        country = country.replace(' ', '+')
        url = url + city + '+' + country
        url = url + '?format=json'

        try:
            response = requests.get(url).json()

            lat = response[0]["lat"]
            lon = response[0]["lon"]

            print(response[0]["lat"])
            print(response[0]["lon"])

            df.at[i, "lat"] = lat
            df.at[i, "lon"] = lon
            df.at[i, "map_url"] = url

            print('url = ')
            print(url)

            continue

        except:
            lat, lon = None, None

            df.at[i, "lat"] = lat
            df.at[i, "lon"] = lon
            df.at[i, "map_url"] = url


def df_from_json():
    """

    """

    parameters = []
    parameters.append('Facility')
    parameters.append('Zipcode')
    parameters.append('City')
    parameters.append('Country')
    parameters.append('Condition')
    parameters.append('Name')
    parameters.append('Affiliation')
    parameters.append('Role')

    df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined' + '.csv')
    df = pd.read_csv(df_save)

    for name in parameters:
        df[name] =  [None] * len(list(df['Unnamed: 0']))

    del df['Unnamed: 0']

    print('df = ')
    print(df)

    for nctid in list(df['NCT Number']):

        print('nctid = ' + str(nctid))
        s = ClinicalTrial(nctid)
        print(f"Study found in {s.location}: {s.title}")

        row_number = min(list(df[df['NCT Number'] == nctid].index))

        for i in range(len(parameters)):

            if parameters[i] == 'Condition':
                df.at[row_number, parameters[i]] = s.condition

            elif parameters[i] == 'Name':
                df.at[row_number, parameters[i]] = s.contacts[0]

            elif parameters[i] == 'Affiliation':
                df.at[row_number, parameters[i]] = s.contacts[1]

            elif parameters[i] == 'Role':
                df.at[row_number, parameters[i]] = s.contacts[2]

            else:
                df.at[row_number, parameters[i]] = s.location[i]

        # lat, lon = retireve_gps(s, parameters)

    df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined_v02' + '.csv')
    df.to_csv(df_save)

    # copy file as excel
    dst = os.path.join(retrieve_path('df_clinical'), 'df_combined_v02' + '.xlsx')
    shutil.copyfile(df_save, dst)



def count_trials():
    """

    """

    df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined_v02' + '.csv')
    df = pd.read_csv(df_save)
    del df['Unnamed: 0']

    df = df.drop_duplicates(subset = 'NCT Number')
    df = df.reset_index()

    col_names = df.columns

    for name in col_names:

        print('name = ' + str(name))

        unique_list = []
        count_list = []

        for item in list(df[name]):

            if item not in unique_list:

                unique_list.append(item)

                df_item = (df[df[name] == item])

                count = len(list(df_item[name]))
                count_list.append(count)

        if 'Sponsor' in name:
            name = 'Sponsor'

        df_item = pd.DataFrame()
        df_item['count'] = count_list
        df_item[name] = unique_list

        df_item = df_item.sort_values('count', ascending=False)

        file_name = os.path.join(retrieve_path('count_clinical'), name + '.csv')
        df_item = df_item.reset_index()
        del df_item['index']
        df_item.to_csv(file_name)


def aggregate_trials():
    """
    From the downloaded trials
    Aggregate results
    """
    df_combined = pd.DataFrame()

    path = os.path.join(retrieve_path('clinical_download'))
    file_list = os.listdir(path)

    for file in file_list:

        df = pd.read_csv(os.path.join(path, file))

        search_term = file.split('.')
        term = search_term[0]
        df['search_term'] = [term] * len(list(df['Rank']))

        col_names = df.columns
        df_combined = pd.DataFrame.append(df, df_combined)

    year_list = []
    month_list = []
    for years in list(df_combined['Start Date']):

        try:
            year = re.findall('[0-9]{4}', years)
            years = years.split(' ')
            month = years[0]

        except:
            year = years
            print('year = ' + str(years))

        year_list.append(year)
        month_list.append(month)

    df_combined['Year'] = year_list
    df_combined['Month'] = month_list
    df_combined = df_combined.sort_values('NCT Number', ascending=False)
    del df_combined['Rank']

    # save the file
    df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined' + '.csv')
    df_combined.to_csv(df_save)

    # copy file as excel
    dst = os.path.join(retrieve_path('df_clinical'), 'df_combined' + '.xlsx')
    shutil.copyfile(df_save, dst)



def scrape_json():
    """
    Scrape and save json
    """

    df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined' + '.csv')
    df = pd.read_csv(df_save)

    for nctid in list(df['NCT Number']):

        path = retrieve_path('json_clinical')
        file = os.path.join(path, nctid  + '.json')

        if os.path.exists(file) == True:
            continue

        ClinicalTrialRetrieve(nctid)


class ClinicalTrialRetrieve():
    """
    Data structure for handling information about a given Clinical Study.
    Requires an NCTID to create (so it can be looked up via API).
    Attributes include:

      title (BriefTitle)
      location (country, zip)

    """

    def __init__(self, nctid):
        BASE_URL = "https://clinicaltrials.gov/api/query/full_studies?expr={}&fmt=json"
        self.nctid = nctid
        self.api_url = BASE_URL.format(self.nctid)
        print(f"Study url: {self.api_url}")

        time.sleep(2)
        r = requests.get(self.api_url)
        time.sleep(2)

        raw_json = r.json()

        if len(raw_json["FullStudiesResponse"]["FullStudies"]) != 1:
            logging.error(f"Could not find study for nctid {self.nctid}")

        self.raw_json = raw_json["FullStudiesResponse"]["FullStudies"][0]["Study"]

        data = raw_json["FullStudiesResponse"]["FullStudies"][0]["Study"]

        json_string = json.dumps(data, indent = 2, ensure_ascii = False)
        # print(json_string)

        time_string = retrieve_datetime()
        path = retrieve_path('json_clinical')
        file = os.path.join(path, nctid  + '.json')

        with open(file, 'w') as outfile:
            # json.dump(json_string, outfile)
            outfile.write(json_string)



if __name__ == "__main__":
    main()
