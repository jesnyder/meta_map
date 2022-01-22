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


def build_webpage():
    """
    Objective: Communicate prioritized knowledge in analyzed data

    Tasks:
        1. Create index.html



    """

    print('started build_webpage')

    tasks = [1, 2]

    if 2 in tasks: chart_js()
    if 1 in tasks: start_html()

    print('completed build_webpage')


def chart_js():
    """

    """

    df_save = os.path.join(retrieve_path('df_clinical'), 'df_combined_v03' + '.csv')
    df = pd.read_csv(df_save)

    df = df.sort_values('Enrollment', ascending=False)

    lat = list(df['lat'])
    lon = list(df['lon'])
    enrollment = list(df['Enrollment'])
    title = list(df['Title'])

    f = open(os.path.join(retrieve_path('js_index')), 'w')

    f.write('JSC.Chart(\'chartDiv\', {')
    f.write('\n')

    #f.write('type: \'horizontal column\',')
    chart_type = 'horizontal column'
    chart_type = 'scatter'
    #chart_type = 'bubble'
    f.write('type: \'' + chart_type + '\' , ')
    f.write('\n')

    f.write('series: [')
    f.write('\n')

    f.write('{')
    f.write('\n')

    f.write('points: [')
    f.write('\n')

    for i in range(len(lat[0:10])):

        f.write('\n')
        f.write('{')
        f.write('x: ' + '\'' + str(float(lat[i])) + '\'' + ', ')
        f.write('y: ' + '\'' + str(float(lon[i])) + '\'' + ', ')
        f.write('r: ' + '\'' + str(float(enrollment[i])) + '\'' )
        f.write('}' + ' , ')
        f.write('\n')

    """
    f.write('{x: \'Apples\', y: 50},')
    f.write('\n')

    f.write('{x: \'Oranges\', y: 42}')
    f.write('\n')
    """

    f.write(']')
    f.write('\n')

    f.write('}')
    f.write('\n')

    f.write(']')
    f.write('\n')

    f.write('});')
    f.write('\n')

    f.close()




def start_html():
    """

    """

    map_save = os.path.join(retrieve_path('map_clinical'), 'map' + '.png')
    print('map_save = ')
    print(map_save)

    # open index.html file
    f = open(os.path.join(retrieve_path('html_index')), 'w')

    f.write('<html>' + '\n')

    # head
    f.write('<head>' + '\n')
    f.write('<title>' + '\n')
    f.write('Global clinical trial map' + '\n')
    f.write('</title>' + '\n')
    f.write('</head>' + '\n')

    # body
    f.write('<body>' + '\n')


    f.write('<center>' + '\n')
    f.write('<h2>' + '\n')
    f.write('A map of the clinical trials' + '\n')
    f.write('</h2>' + '\n')

    f.write('<center>' + '\n')
    f.write('<h3>' + '\n')
    f.write('Objective: Survey clinical trials using an MSC intervention' + '\n')
    f.write('</h3>' + '\n')

    f.write('<p>' + '\n')
    f.write('A map of the clinical trials' + '\n')
    f.write('</p>' + '\n')
    f.write('</center>' + '\n')


    f.write('\n')
    f.write('<center>' + '\n')
    f.write('<h3>' + '\n')
    f.write('Method: Data Scraping' + '\n')
    f.write('</h3>' + '\n')

    f.write('<p>' + '\n')
    f.write('The National Instittue of Health (NIH) and the National Library of Medicine (NLM) maintain a website that archives clinical trials. ClinicalTrials.gov (NIH) is a database of ' + '\n')
    f.write('</p>' + '\n')
    f.write('</center>' + '\n')
    f.write('\n')


    f.write('\n')
    f.write('<div id="wrapper">')
    f.write('<img src="' + map_save + '" id="0" alt="' + map_save +'" width="100%" />' )
    f.write('</div>')
    f.write('\n')

    f.write('</body>' + '\n')

    f.write('<body>' + '\n')
    f.write('<center>' + '\n')
    f.write('<div id="chartDiv" style="width:80%; height:300px; margin:0 auto;">')
    f.write('</div>' + '\n')
    f.write('</center>' + '\n')
    f.write('</body>' + '\n')

    # make a table to list trial count by country
    for  file in os.listdir(retrieve_path('count_clinical')):
        df = pd.read_csv(os.path.join(retrieve_path('count_clinical'), file))
        del df['Unnamed: 0']
        df = df[df['count'] > 10]
        print(df)

        if 'Country' not in file and 'Affiliation' not in file and 'City' not in file and 'Condition' not in file and 'Outcome Measures' not in file and 'Facility' not in file and 'Interventions' not in file and 'Locations' not in file and 'Zipcode' not in file:
            continue

        f.write('<center>' + '\n')
        f.write('<h3>' + '\n')
        name, ext = file.split('.')
        f.write(name + '\n')
        f.write('</h3>' + '\n')

        f.write('<p>' + '\n')
        f.write('The search found ')
        f.write(str(len(list(df['count']))))
        f.write(' entries with more than 10 trials. The number of trials in the table is ')
        f.write(str(sum(list(df['count']))))
        f.write('.')
        f.write('</p>' + '\n')



        f.write('</center>' + '\n')

        f.write('<table ')
        f.write('style="border:1px solid black;margin-left:auto;margin-right:auto;"')
        f.write(' >' + '\n')

        # write the table header
        f.write('<tr>' + '\n')
        for name in df.columns:
            f.write('<td>' + '\n')
            f.write(name)
            f.write('</td>' + '\n')

            f.write('<td>' + '\n')
            f.write('       ')
            f.write('</td>' + '\n')

        f.write('</tr>' + '\n')

        for j in range(len(list(df.iloc[:,0]))):

            f.write('<tr>' + '\n')

            for name in df.columns:

                f.write('<td>' + '\n')
                f.write(str(df.loc[j][name]))
                f.write('</td>' + '\n')

                f.write('<td>' + '\n')
                f.write('       ')
                f.write('</td>' + '\n')

            f.write('</tr>' + '\n')

        f.write('</table>' + '\n')

    # include for javascript chart
    # ref: https://www.freecodecamp.org/news/how-to-make-your-first-javascript-chart/
    f.write('<script src="https://code.jscharting.com/2.9.0/jscharting.js"></script>')
    f.write('\n')
    js_index = retrieve_path('js_index')
    f.write('<script src="' + js_index + '"></script>')
    f.write('\n')

    f.write('</html>' + '\n')

    f.close()


if __name__ == "__main__":
    main()
