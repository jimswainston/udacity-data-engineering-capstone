from curses import keyname
import constants
import uuid
from numpy import nan as NA
import datetime 
import pandas.io.sql as sqlio
import psycopg2

def country_code_lookup(country):
    """
    Lookup an ISO 3166 alpha-3 country code using the name of a country
    
    Parameters
    ----------
    country : the name of a country
    
    Returns
    ----------
    country_code (str) : ISO 3166 alpha-3 country code for the country
    """    
    country_code = constants.COUNTRIES[country]
    return country_code

def country_key_lookup (country_code,country_table):
    """
    Lookup primary key of country from the dim_country table

    Parameters
    ----------
    country_code : ISO 3166 alpha-3 country code for the country        
        
    country_table : a pandas dataframe containing contents of dim_country

    Returns
    ----------
    country_id (int) : the primary key of the country from the dim_country table   
    
    """    
    if country_code is not None:
        country_id = country_table.loc[country_table['country_code'] == country_code, 'country_id'].iloc[0]
        return int(country_id)

def match_countries_in_affiliation(affiliation):
    """
    Finds all the countries mentioned in an authors affiliation string
    
    Parameters
    ----------
    affiliation : a string containing the affiliation of an author of a journal article paper 
        
    Returns
    ----------
    matches (list) : a list of country names found in the affliation string
    """    
    matches = []
    for x in constants.COUNTRIES:
        if x in affiliation and x not in matches:
            matches.append(x)

    if len(matches) > 0:
        return matches
    


def process_published_date(json_published_object):
    """
    Get the published date of a journal article
    
    Parameters
    ----------
    json_published_object: a Pyton Dict representing a json Published
    object from the Crossref JSON. The Dict contains the published date
    of an article. 
        
    Returns
    ----------
    published_date (datetime) : the date that the article was published. Returns 
    None if published date is not available in the article metadata.
    """    
    date_parts = json_published_object["date-parts"][0]
    if len(date_parts) == 0:
        return None
    elif len(date_parts) == 3:
        year = date_parts[0]
        month = date_parts[1]
        day = date_parts[2]
        published_date = datetime.datetime(year,month,day)
        return published_date
    elif len(date_parts) == 2:
        year = date_parts[0]
        month = date_parts[1]
        day = 1 # if not available assume first day of month
        published_date = datetime.datetime(year,month,day)
        return published_date
    elif len(date_parts) == 1:
        year = date_parts[0]
        month = 1 # if not available assume first month of year
        day = 1 # if not available assume first day of month
        published_date = datetime.datetime(year,month,day)
        return published_date
    else:
        return None


def process_article(article):
    """
    Retrieve article metadata (article_id,DOI,title and published_date)
    
    Parameters
    ----------
    article : a dict converted from a JSON object 
    representing a journal article

    Returns
    ----------
    A list that contains an article_id, DOI, title and published_date
    article_id (uuid) : a uuid generated for the article
    DOI (str): the digital object identifier for the article
    title (str): the title for the article
    published_date (datetime): the date the article was published.        
    
    """    
    # create unique id for article
    article_id = uuid.uuid4()

    if "DOI" in article:
        DOI = article["DOI"]
    else:
        DOI = None

    if "title" in article:
        title = article["title"][0]
    else:
        title = None

    if "published" in article:
        published_date = process_published_date(article["published"])
    else:
        published_date = None

    return [article_id,DOI,title,published_date]



def process_author(article,article_id,DOI,country_table):
    """
    Retrieve author metadata and generate uuid for author. 
    For each author we are creating an affiliation and using
    the author_id as a foreign key to the afilliation.
    

    Parameters
    ----------
    article : a dict converted from a JSON object 
    representing a journal article
    article_id: uuid for the article
    DOI: Digital Object Identifier for the article
    country_table: a pandas dataframe containing contents of dim_country

    Returns
    ----------    
    authors (list) : a list of the authors in the article. Metadata for
    each author including author_id(uuid),article_id(uuid), first_name(str)
    and last_name (str)
    affiliations (list) : a list of the instutions the author is affiliated with.
    Includes affiliation_id(uuid), author_id(uuid) and affiliation_name(str) 
    affiliation_errors (list) : a list of the affliations where a country wasn't
    found. Includes affiliation_id(uuid), author_id(uuid) and affiliation_name(str)
        
    
    """    
    authors = []
    affiliations = []
    affiliation_errors = [] #store affiliations where a country was not found
    
    if "author" in article:
        
        for author in article["author"]:
            
            author_id = uuid.uuid4()
                       
            if "given" in author:
                first_name = author["given"]
            else:
                first_name = ""

            if "family" in author:
                last_name = author["family"]
            else:
                last_name = ""
            
            #handle empty strings
            if not first_name:
                first_name = None
            if not last_name:
                last_name = None
            authors.append([author_id,article_id,first_name,last_name])

            # catching exceptions where there is no affiliation name. Modern method is to link to an ID in an oranisation registory. 
            #TODO handle ID based affiliations
            try:
                if "affiliation" in author:
                    for affiliation in author["affiliation"]:
                        affiliation_countries = match_countries_in_affiliation(affiliation["name"])
                        if affiliation_countries is not None: # only create an affliation when we know the country
                            for country in affiliation_countries:
                                affiliation_id = uuid.uuid4()
                                country_name = country
                                country_code = country_code_lookup(country)
                                country_id = country_key_lookup(country_code,country_table)                                
                                affiliations.append([affiliation_id,author_id,country_id])
                        elif affiliation_countries is None:
                            affiliation_id = uuid.uuid4()
                            affiliation_name = affiliation["name"]
                            affiliation_errors.append([affiliation_id,author_id,affiliation_name])
            except KeyError:
                print("Key error: " + "name key not found " + "-" " Article DOI :" + str(DOI))


    return authors,affiliations,affiliation_errors





def year_key_lookup (pubdate):
    """
    Retrieve id of the year for a published date. 
    This id maps to the primary key of the dim_year
    table.  
    
    Parameters
    ----------
    pubdate (int) : the year the article was published. 
        
    Returns
    ---------- 
    year_key (int) : the id of the year for a published date.    
    """    
    if pubdate is not None:
        if type(pubdate) is datetime:
            year_index = constants.DIM_YEAR_LOOKUP['year'].index(pubdate.year) 
            year_key = constants.DIM_YEAR_LOOKUP['year_id'][year_index]
            return year_key
        elif type(pubdate) is int:
            year_index = constants.DIM_YEAR_LOOKUP['year'].index(pubdate) 
            year_key = constants.DIM_YEAR_LOOKUP['year_id'][year_index]
            return year_key






