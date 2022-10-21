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
import constants
import pandas.io.sql as sqlio


def load_fact_gdp(cur,conn,filepath,country_table):
    gdp_data = pd.read_csv(filepath,header=2)
    
    fact_gdp = {
        'id' : [],
        'country_id' : [],
        'year_id' : [],
        'gdp_amount' : []
    }

    codes = list(constants.COUNTRIES.values())
    codes = list(dict.fromkeys(codes))  # remove duplicate codes

    years = list(range(2015,2021))

    for code in codes:
        country_id = de.country_key_lookup(code,country_table)
        for year in years:
            id = uuid.uuid4()
            gdp_amount = None
            year_id = de.year_key_lookup(year) 
            try:            
                gdp_amount = gdp_data.loc[gdp_data['Country Code'] == code, str(year)].iloc[0]                
            except IndexError:
                print(str(code) + " " + str(year) + " " + str("Country code not found"))
            fact_gdp['id'].append(id)
            fact_gdp['country_id'].append(country_id)
            fact_gdp['year_id'].append(year_id)
            fact_gdp['gdp_amount'].append(gdp_amount)
    
    gdp_table = pd.DataFrame(fact_gdp, dtype=object)
    cur.executemany(gdp_table_insert, gdp_table.to_numpy().tolist())
    conn.commit()

def process_article_file(cur, filepath, country_table):
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
    #'country_name' : [],
    #'country_code' : [],
    'country_id' : []
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

                authors = de.processAuthor(item,article[0],article[1],country_table) # pass article id in so it can be used as foreign key for author # pass DOI for locating errors in files
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
                        affiliationData['country_id'].append(affiliation[2])
                        #affiliationData['country_name'].append(affiliation[2])
                        #affiliationData['country_code'].append(affiliation[3])

                if affiliationErrorData is not None:
                    for affiliationError in affiliationErrorData:
                        affiliationErrors['affiliation_id'].append(affiliationError[0])
                        affiliationErrors['author_id'].append(affiliationError[1])
                        affiliationErrors['affiliation_name'].append(affiliationError[2])

            

    articles = pd.DataFrame(articleData)
    authors = pd.DataFrame(authorData)
    affiliations = pd.DataFrame(affiliationData, dtype=object)
    affiliationErrors = pd.DataFrame(affiliationErrors) 


    # insert article records
    
    cur.executemany(article_table_insert, articles.to_numpy().tolist())

    # insert author records

    cur.executemany(author_table_insert, authors.to_numpy().tolist())

    # insert affiliation records
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(affiliations)
    
    cur.executemany(affiliation_table_insert, affiliations.to_numpy().tolist())

    # insert affiliation error records

    cur.executemany(affiliation_errors_table_insert, affiliationErrors.to_numpy().tolist())
    

def process_data(cur, conn, filepath, func, country_table):
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
        func(cur, datafile, country_table)
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

def load_countries(cur,conn):
    country_data = {
        'country_code' : [],
        'country_name' : []
    }

    for code in constants.COUNTRIES.values():
        country_data['country_code'].append(code)

    for name in constants.COUNTRIES.keys():
        country_data['country_name'].append(name)

    countries = pd.DataFrame(country_data)
    countries = countries.dropna()
    countries = countries.drop_duplicates(subset=['country_code'])
    countries = countries.sort_values('country_code')
    countries.loc[countries['country_code'] == 'GBR', 'country_name'] = 'United Kingdom'
    countries.loc[countries['country_code'] == 'AUS', 'country_name'] = 'Australia'
    countries.loc[countries['country_code'] == 'FRA', 'country_name'] = 'France'
    countries = countries.reset_index(drop=True)
    countries['country_id'] = countries.index
    countries = countries[['country_code','country_name']]
    cur.executemany(country_table_insert, countries.to_numpy().tolist())
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
    load_countries(cur,conn)

    # load country data used for reference in ETL
    connCountry = psycopg2.connect("host=127.0.0.1 dbname=udacityprojectdb user=student password=6GNjBQvF")
    sql = "select * from dim_country;"
    country_table = sqlio.read_sql_query(sql, conn)
    connCountry.close()

    load_fact_gdp(cur,conn,filepath='../data/WorldBank/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4481247.csv', country_table=country_table)
    
    process_data(cur, conn, filepath='/home/jswainston/Downloads/April2022CrossrefPublicDataFile', func=process_article_file, country_table=country_table)

    conn.close()


if __name__ == "__main__":
    main()