import constants
import uuid
from numpy import nan as NA
import datetime 

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
        return NA
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
    else:
        return NA


def processArticle(article):
    # create unique id for article
    article_id = uuid.uuid4()

    if "DOI" in article:
        DOI = article["DOI"]
    else:
        DOI = NA

    if "title" in article:
        title = article["title"]
    else:
        title = NA

    if "published" in article:
        publishedDate = processPublishedDate(article["published"])
    else:
        publishedDate = NA

    return [article_id,DOI,title,publishedDate]



def processAuthor(article,article_id):
    authors = []
    affiliations = []
    
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
                first_name = NA
            if not last_name:
                last_name = NA
            authors.append([author_id,article_id,first_name,last_name])

            if "affiliation" in author:
                for affiliation in author["affiliation"]:
                    affiliationCountries = matchCountriesInAffiliation(affiliation["name"])
                    if affiliationCountries is not None:
                        for country in affiliationCountries:
                            affiliation_id = uuid.uuid4()
                            country_name = country
                            affiliations.append([affiliation_id,author_id,country_name])

    return authors,affiliations








