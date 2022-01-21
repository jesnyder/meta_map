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

    f.write('<h2>' + '\n')
    f.write('A map of the clinical trials' + '\n')
    f.write('</h2>' + '\n')

    f.write('<p>' + '\n')
    f.write('A map of the clinical trials' + '\n')
    f.write('</p>' + '\n')

    f.write('\n')
    f.write('<div id="wrapper">')
    f.write('<img src="' + map_save + '" id="0" alt="' + map_save +'" width="100%" />' )
    f.write('</div>')
    f.write('\n')

    f.write('</body>' + '\n')
    f.write('</html>' + '\n')

    f.close()


if __name__ == "__main__":
    main()
