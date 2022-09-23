import os
import glob
import psycopg2
import pandas as pd
import uuid
import numpy as np
from sqlQueries import *
import gzip
import json
import dataExtractUtils as de
import psycopg2.extras
import psycopg2.extensions

def process_article_file(cur, filepath):
    """Reads data from a CROSSREF article file and inserts into udacityprojectdb database 
    
    Parameters
    ----------
    cur : a psycopg2 cursor object
        The cursor object that can be used to execute statements against the database
        
    filepath : str
        The filepath to the folder where the article metadata files are stored
    
    """
    
    articleData = {
    'article_id' : [],
    'DOI' : [],
    'title' : [],
    'published_date' : [],
    'year_id' : []
    }

    authorData = {
    'author_id' : [],
    'article_id' : [],
    'first_name' : [],
    'last_name' : []
    }

    affiliationData = {
    'affiliation_id' : [],
    'author_id' : [],
    'country_name' : []
    }

    affiliationCountry = {
    'country_ID' : [],
    'affiliation_id' : []
    }

    affiliationErrors = {
    'affiliation_id' : [],
    'author_id' : [],
    'affiliation_name' : []
    }

    # open article file
    ##df = pd.read_json(filepath, lines=True)
    with gzip.open(filepath, 'r') as fin:        
        json_bytes = fin.read()    
                      
    json_str = json_bytes.decode('utf-8')            
    data = json.loads(json_str)

    for item in data["items"]:
        if "type" in item:
            if item["type"] == 'journal-article':
                article = de.processArticle(item)

                year_key = de.year_key_lookup(article[3])

                articleData['article_id'].append(article[0])
                articleData['DOI'].append(article[1])
                articleData['title'].append(article[2])
                articleData['published_date'].append(article[3])
                articleData['year_id'].append(year_key)

                authors = de.processAuthor(item,article[0],article[1]) # pass article id in so it can be used as foreign key for author # pass DOI for locating errors in files
                affiliationErrorData = authors[2]
                authorAffiliations = authors[1]
                authors = authors[0]

                
                for author in authors:
                    authorData['author_id'].append(author[0])
                    authorData['article_id'].append(author[1])
                    authorData['first_name'].append(author[2])
                    authorData['last_name'].append(author[3])

                if authorAffiliations is not None:
                    for affiliation in authorAffiliations:
                        affiliationData['affiliation_id'].append(affiliation[0])
                        affiliationData['author_id'].append(affiliation[1])
                        affiliationData['country_name'].append(affiliation[2])

                if affiliationErrorData is not None:
                    for affiliationError in affiliationErrorData:
                        affiliationErrors['affiliation_id'].append(affiliationError[0])
                        affiliationErrors['author_id'].append(affiliationError[1])
                        affiliationErrors['affiliation_name'].append(affiliationError[2])

            

    articles = pd.DataFrame(articleData)
    authors = pd.DataFrame(authorData)
    affiliations = pd.DataFrame(affiliationData)
    affiliationErrors = pd.DataFrame(affiliationErrors) 


    # insert article records
    
    cur.executemany(article_table_insert, articles.to_numpy().tolist())

    # insert author records

    cur.executemany(author_table_insert, authors.to_numpy().tolist())

    # insert affiliation records

    cur.executemany(affiliation_table_insert, affiliations.to_numpy().tolist())

    # insert affiliation error records

    cur.executemany(affiliation_errors_table_insert, affiliationErrors.to_numpy().tolist())
    
    # insert artist record
    #artist_data = df[['artist_id', 'artist_name','artist_location','artist_latitude','artist_longitude']].values[0].tolist()
    #cur.execute(artist_table_insert, artist_data)



def process_data(cur, conn, filepath, func):
    """Reads all files under directory and inserts into udacityprojectdb database 
    
    Parameters
    ----------
    cur : a psycopg2 cursor object
        The cursor object that can be used to execute statements against the udacityprojectdb database
    
    con: a psycopg2 connection object
        The connection object that provides the connection to the udacityprojectdb database
    
    filepath : str
        The filepath to the folder where the JSON article data files are stored
        
    func: a function object
        if process_article_file then all article files will be processed     
    
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json.gz'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
        print('Processed file: {}'.format(datafile))


def load_years(cur,conn):
    dim_year_data = {
    'year_id' : list(range(1,402)),
    'year' : list(range(1800,2201))
    }

    dim_year = pd.DataFrame(dim_year_data)
    cur.executemany(year_table_insert, dim_year.to_numpy().tolist())
    conn.commit()

def main():
    """ETL entry point 
    - creates connection to udacityprojectdb database
    - creates a cursor object 
    - calls process_data function with process_crossref_file as an argument to first process all article data files
    """
    psycopg2.extras.register_uuid()
    conn = psycopg2.connect("host=127.0.0.1 dbname=udacityprojectdb user=student password=6GNjBQvF")
    cur = conn.cursor()

    load_years(cur,conn)

    #process_data(cur, conn, filepath='../data/Crossref', func=process_article_file)
    process_data(cur, conn, filepath='/home/jswainston/Downloads/April2022CrossrefPublicDataFile', func=process_article_file)

    conn.close()


if __name__ == "__main__":
    main()