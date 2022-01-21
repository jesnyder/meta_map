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

    tasks = [1]

    if 1 in tasks: start_html()

    print('completed build_webpage')


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
    f.write('Objective: Survey Clinical Trials using an MSC Intervention' + '\n')
    f.write('</h3>' + '\n')

    f.write('<p>' + '\n')
    f.write('A map of the clinical trials' + '\n')
    f.write('</p>' + '\n')
    f.write('</center>' + '\n')

    f.write('<center>' + '\n')
    f.write('<h3>' + '\n')
    f.write('Method: Data Scraping' + '\n')
    f.write('</h3>' + '\n')

    f.write('<p>' + '\n')
    f.write('A map of the clinical trials' + '\n')
    f.write('</p>' + '\n')
    f.write('</center>' + '\n')

    f.write('\n')
    f.write('<div id="wrapper">')
    f.write('<img src="' + map_save + '" id="0" alt="' + map_save +'" width="100%" />' )
    f.write('</div>')
    f.write('\n')

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
        f.write('</center>' + '\n')

        f.write('<table ')
        f.write('style="border:1px solid black;margin-left:auto;margin-right:auto;"')
        f.write(' ">' + '\n')

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

    f.write('</html>' + '\n')

    f.close()


if __name__ == "__main__":
    main()
