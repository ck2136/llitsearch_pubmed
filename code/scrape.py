#!/usr/bin/python3.6
"""
Python Script
Scrape PUBMED
Requires:'Biopython'
Author: CK
License:GNU
"""

from Bio import Entrez
import time
import json


def search(batch_size, query):
    try:
        from urllib.error import HTTPError
    except ImportError:
        from urllib2 import HTTPError

    Entrez.email = 'chong.kim@ucdenver.edu'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            usehistory='y',
                            term=query)
    search_results = Entrez.read(handle)
    count = int(search_results["Count"])
    print("Found %i results" % count)
    # initialize a dictionary
    asthma_abs = {
        'ID': [],
        'Abstract': []
    }
    for start in range(0, count, batch_size):
        end = min(count, start+batch_size)
        print("Going to download record %i to %i" % (start+1, end))
        attempt = 1
        while attempt <= 3:
            try:
                print("Current records = %i to %i" % (start+1, end),
                      "Current attempt = ", attempt)
                fetch_handle = Entrez.efetch(db='pubmed', rettype='medline',
                                             retmode='xml', retstart=start,
                                             retmax=batch_size,
                                             webenv=search_results["WebEnv"],
                                             query_key=search_results["QueryKey"])
                print("Success!")
                attempt = 4
            except HTTPError as err:
                if 500 <= err.code <= 599:
                    print("Received error from server %s" % err)
                    print("Attempt %i of 3" % attempt)
                    attempt += 1
                    time.sleep(15)
                else:
                    raise
        data = Entrez.read(fetch_handle)
        fetch_handle.close()
        for i, paper in enumerate(data['PubmedArticle']):
            asthma_abs['ID'].append(paper['MedlineCitation']['PMID'])
            asthma_abs['Abstract'].append(paper['MedlineCitation']['Article']['Abstract']['AbstractText'])
    print("Saving data...")
    with open("../data/downloaded_abs.json", "w") as fp:
        json.dump(asthma_abs, fp)


if __name__ == '__main__':
    #user_query = input("Query for PUBMED search: ")
    user_query = 'asthma AND prediction AND beta'
    #user_batch = int(input("Batch size? (default = 11): "))
    user_batch = 10 # keep it at 10 for now :)
    search(user_batch, user_query)
