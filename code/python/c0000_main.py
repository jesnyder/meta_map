import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from bs4 import BeautifulSoup

import requests
import re
import os, json


from c0001_retrieve_meta import retrieve_path
from c0001_retrieve_meta import retrieve_datetime
#from c1000_create_webpage import create_webpage

from c0100_scrape_gscholar import scrape_gscholar
from c0200_scrape_clinical import scrape_clinical

from c1000_build_webpage import build_webpage


def main():
    """
    Objective: Which approach shows more promise for MSC: allogenic or autologous

    1. Scrape clinical trials from NIH Clinical Trials
    2. Build dataframe - each row a trial and columns key descriptors
    3. Build plots
    4. Create webpage

    """

    tasks = [10]

    if 1 in tasks: scrape_gscholar()
    if 2 in tasks: scrape_clinical()

    if 10 in tasks: build_webpage()




    """
    # find searchs
    df = pd.read_csv(os.path.join(retrieve_path('search_terms')))
    search_names = list(df['search_names'])

    for name in search_names:

        print('search_name = ')
        print(name)

        row_number = min(list(df[df['search_names'] == name].index))
        search_terms = str(df.at[row_number, 'search_terms']).split()

        print('search_terms = ')
        print(search_terms)

        for term in search_terms:

            scrape_gscholar_json(name, term)


def scrape_gscholar_json(name, term):
    """

    """

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

    proxies = {
        'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
        }

    num_list = np.arange(0, 52, 1, dtype=int)

    for num in num_list:
        print('num = ' + str(num))

        # build the url
        url = 'https://scholar.google.com/scholar?'
        url = url + 'start=' + str(int(num*10))
        url = url + '&q=' + term
        url = url + '&hl=en&as_sdt=0,5'
        print('url = ')
        print(url)

        # Get webpage, but wait to prevent blocking
        print('Wait: ' + retrieve_datetime())
        time.sleep(30)
        html = requests.get(url, headers=headers, proxies=proxies).text
        time.sleep(30)
        print('Wait: ' + retrieve_datetime())

        soup = BeautifulSoup(html, 'lxml')

        # scan for error
        error = str('Our systems have detected unusual traffic from your computer network.  This page checks to see if it')
        if error in str(soup):
            print('Automated search detected.')
            break

        # Scrape just PDF links
        for pdf_link in soup.select('.gs_or_ggsm a'):
            pdf_file_link = pdf_link['href']
            print(pdf_file_link)

        # JSON data will be collected here
        data = []

        # Container where all needed data is located
        for result in soup.select('.gs_ri'):

            title = result.select_one('.gs_rt').text

            try:
                title_link = result.select_one('.gs_rt a')['href']
            except:
                title_link = None

            publication_info = result.select_one('.gs_a').text
            snippet = result.select_one('.gs_rs').text
            cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
            related_articles = result.select_one('a:nth-child(4)')['href']
            try:
                all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
            except:
                all_article_versions = None

            # get number of citations for each paper
            try:
                txt_cite = result.find("div", class_="gs_fl").find_all("a")[2].string
            except:
                txt_cite = '0 0 0'

            try:
                citations = txt_cite.split(' ')
            except:
                citations = '0 0 0'

            citations = (citations[-1])

            try:
                citations = int(citations)
            except:
                citations = 0

            # get the year of publication of each paper
            txt_year = result.find("div", class_="gs_a").text
            year = re.findall('[0-9]{4}', txt_year)
            if year:
                year = list(map(int,year))[0]
            else:
                year = 0


            data.append({
                'title': title,
                'title_link': title_link,
                'publication_info': publication_info,
                'snippet': snippet,
                'citations': citations,
                'cited_by': f'https://scholar.google.com{cited_by}',
                'related_articles': f'https://scholar.google.com{related_articles}',
                'all_article_versions': f'https://scholar.google.com{all_article_versions}',
                'year': year,
                })

            json_string = json.dumps(data, indent = 2, ensure_ascii = False)
            print(json_string)

            time_string = retrieve_datetime()

            path = retrieve_path('json_gscholar')
            path = os.path.join(path, name)
            if not os.path.exists(path):os.makedirs(path)
            file = os.path.join(path, term + ' ' + name + ' ' + time_string + '.json')

            print('json file saved: ')
            print(file)

            with open(file, 'w') as outfile:
                # json.dump(json_string, outfile)
                outfile.write(json_string)

        # if successful, save the url to a file
        #url_path = retrieve_path('url_gscholar')
        url_file = os.path.join(retrieve_path('url_gscholar'), name)
        if not os.path.exists(url_file):os.makedirs(url_file)
        url_f = os.path.join(retrieve_path(url_file, name + '.csv')
        url_f = open(url_file, 'a')
        url_f.write(url + '\n')
        url_f.close()

        """


if __name__ == "__main__":
    main()
