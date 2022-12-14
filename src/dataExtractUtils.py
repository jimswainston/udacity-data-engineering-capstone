from curses import keyname
import constants
import uuid
from numpy import nan as NA
import datetime 
import pandas.io.sql as sqlio
import psycopg2




def country_code_lookup(country):
    country_code = constants.COUNTRIES[country]
    return country_code

def country_key_lookup (country_code,country_table):
    if country_code is not None:
        country_id = country_table.loc[country_table['country_code'] == country_code, 'country_id'].iloc[0]
        return int(country_id)

def matchCountriesInAffiliation(affiliation):
    matches = []
    for x in constants.COUNTRIES:
        if x in affiliation and x not in matches:
            matches.append(x)

    if len(matches) > 0:
        return matches
    


def processPublishedDate(jsonPublishedObject):
    dateParts = jsonPublishedObject["date-parts"][0]
    if len(dateParts) == 0:
        return None
    elif len(dateParts) == 3:
        year = dateParts[0]
        month = dateParts[1]
        day = dateParts[2]
        publishedDate = datetime.datetime(year,month,day)
        return publishedDate
    elif len(dateParts) == 2:
        year = dateParts[0]
        month = dateParts[1]
        day = 1 # if not available assume first day of month
        publishedDate = datetime.datetime(year,month,day)
        return publishedDate
    elif len(dateParts) == 1:
        year = dateParts[0]
        month = 1 # if not available assume first month of year
        day = 1 # if not available assume first day of month
        publishedDate = datetime.datetime(year,month,day)
        return publishedDate
    else:
        return None


def processArticle(article):
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
        publishedDate = processPublishedDate(article["published"])
    else:
        publishedDate = None

    return [article_id,DOI,title,publishedDate]



def processAuthor(article,article_id,DOI,country_table):
    authors = []
    affiliations = []
    affiliationErrors = [] #store affiliations where a country was not found
    
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

            # catching exceptions where there is no affiliation name. Modern method is to link to an ID in an oranisatio registory. 
            #TODO handle ID based affiliations
            try:
                if "affiliation" in author:
                    for affiliation in author["affiliation"]:
                        affiliationCountries = matchCountriesInAffiliation(affiliation["name"])
                        if affiliationCountries is not None:
                            for country in affiliationCountries:
                                affiliation_id = uuid.uuid4()
                                country_name = country
                                country_code = country_code_lookup(country)
                                country_id = country_key_lookup(country_code,country_table)
                                #affiliations.append([affiliation_id,author_id,country_name,country_code])
                                affiliations.append([affiliation_id,author_id,country_id])
                        elif affiliationCountries is None:
                            affiliation_id = uuid.uuid4()
                            affiliation_name = affiliation["name"]
                            affiliationErrors.append([affiliation_id,author_id,affiliation_name])
            except KeyError:
                print("Key error: " + "name key not found " + "-" " Article DOI :" + str(DOI))


    return authors,affiliations,affiliationErrors





def year_key_lookup (pubdate):
    if pubdate is not None:
        if type(pubdate) is datetime:
            year_index = constants.DIM_YEAR_LOOKUP['year'].index(pubdate.year) 
            year_key = constants.DIM_YEAR_LOOKUP['year_id'][year_index]
            return year_key
        elif type(pubdate) is int:
            year_index = constants.DIM_YEAR_LOOKUP['year'].index(pubdate) 
            year_key = constants.DIM_YEAR_LOOKUP['year_id'][year_index]
            return year_key






