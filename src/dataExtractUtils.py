import constants

def matchCountriesInAffiliation(affiliation):
    matches = []
    for x in constants.COUNTRIES:
        if x in affiliation and x not in matches:
            matches.append(x)

    if len(matches) > 0:
        return matches
    
