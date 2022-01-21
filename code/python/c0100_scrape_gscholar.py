from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import requests
import shutil
import pandas as pd
import time

from c0001_retrieve_meta import retrieve_path
from c0001_retrieve_meta import retrieve_datetime



def scrape_gscholar():
    """
    Objective: Scrape publication information from Google Scholar
    Search terms saved in a user provided document

    Tasks:
        1. Scrape json from Google Scholar
        2. Convert json to dataframe
        3. Summarize the number of results for each search name

        *** not implemented ***
        4. Scrape additional metadata using publication url
        5. Find latitude and longitude using OpenMaps for institution

    """

    tasks = [2, 3]

    # find search names and corresponding search terms
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

            if 1 in tasks: scrape_gscholar_json(name, term)

        if 2 in tasks: json_to_dataframe(name)
        if 3 in tasks: summarize_scrape(name)


def summarize_scrape(name):
    """
    List counts for each search term
    """

    df_path = retrieve_path('df_gscholar')
    df_file = os.path.join(df_path, name + '.csv')
    df = pd.read_csv(df_file)

    file = open(retrieve_path('summary_gscholar'), 'a+')
    file.write(retrieve_datetime() + ' , ')
    file.write(name + ' , ')
    file.write(str(len(list(df['title']))) + ' , ')
    file.write('\n')
    file.close()


def json_to_dataframe(name):
    """
    Open the saved json
    Convert to a dataframe
    Aggregate over all search terms
    """

    # establish a blank dataframe
    df = pd.DataFrame()

    # list all json files retrieved for the search term
    path = os.path.join(retrieve_path('json_gscholar'), name)
    file_list = os.listdir(path)
    print('file_list = ')
    print(file_list)

    for file in file_list:

        if file.endswith('.json'):

            if name in str(file):

                jsonfile = os.path.join(path, file)
                df_file = pd.read_json(jsonfile)

                df = pd.DataFrame.append(df, df_file)

    print(df)

    # sort
    df = df[df['year'] > 2012]
    df = df.drop_duplicates(subset = 'title_link')
    df = df.sort_values('citations', ascending=False)
    df = df.reset_index()

    del df['index']
    print(df)

    print(df['citations'])

    df_path = retrieve_path('df_gscholar')
    df_file = os.path.join(df_path, name + '.csv')
    df.to_csv(df_file)

    # copy file as excel
    dst = os.path.join(df_path, name + '.xlsx')
    shutil.copyfile(df_file, dst)





def scrape_gscholar_json(name, term):
    """
    Recieve the search name and term
    Build a url to a google scholar page
    Scrape the metadata and save each page as a json file
    """

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

    proxies = {
        'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
        }

    num_list = np.arange(0, 10, 1, dtype=int)

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
        time.sleep(50)
        html = requests.get(url, headers=headers, proxies=proxies).text
        time.sleep(15)
        print('Wait: ' + retrieve_datetime())

        soup = BeautifulSoup(html, 'lxml')

        # scan for error
        error = str('Our systems have detected unusual traffic from your computer network.  This page checks to see if it')
        error2 = str('Sorry, we can\'t verify that you\'re not a robot when JavaScript is turned off.')
        if error in str(soup) or error2 in str(soup):
            print('Automated search detected.')
            break

        print('soup = ')
        print(soup)

        # Scrape just PDF links
        for pdf_link in soup.select('.gs_or_ggsm a'):
            pdf_file_link = pdf_link['href']
            print(pdf_file_link)

        # JSON data will be collected here
        data = []

        # check if results were found
        try:
            results = soup.select('.gs_ri')
            print('Results found for url = ')
            print(url)
        except:
            print('No results found. Scrape for term ended.')
            break

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
            file = os.path.join(path, name + ' ' + term + ' ' + time_string + '.json')

            print('json file saved: ')
            print(file)

            with open(file, 'w') as outfile:
                # json.dump(json_string, outfile)
                outfile.write(json_string)



if __name__ == "__main__":
    main()
