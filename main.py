import random, math, json, os
import requests
import pycountry
import urllib.request
from datetime import date



def getRandomNum(min, max):
    return  math.floor(random.uniform(min, max))

#SELECT PAGES OF NOTICES
def getListNotices():

        randomNum = getRandomNum(1, 500)
        url_notices ="https://ws-public.interpol.int/notices/v1/red?resultPerPage=100&page={0}".format(randomNum)
        response_notices =   requests.get(url_notices)
        data_notices =   response_notices.json()
        return data_notices

# GET FUGITIVE KEY
def getNoticesDetails():

        data_notices =  getListNotices()
        fugitiveKey = list(data_notices['_embedded']["notices"])
        return fugitiveKey

#GET RANDOM FUGITIVES INDEX
def getFugitiveIndex():

    fugitiveKey =  getNoticesDetails()
    fugitivesLength = len(fugitiveKey)
    randomIndex = getRandomNum(0, fugitivesLength)
    def closure_func():
        return randomIndex
    return closure_func()

randomIndex = getFugitiveIndex()

#GET FUGITIVES ID, ie 23456-23456
def getFugitiveID():

        fugitiveKey =  getNoticesDetails()
        # change  ie: 3545/3454 to 3545-3454 
        iD = fugitiveKey[randomIndex]['entity_id']
        iDStr = iD.split('/')

        alt_iD = list(iDStr)
        new_iD = []
        real_iD = list(new_iD)

        real_iD.insert(1, alt_iD[0])
        real_iD.insert(2, '-')
        real_iD.insert(3, alt_iD[1])

        fugitive_ID = ''.join(real_iD)
        return fugitive_ID

# GET INFORMATIONS FROM SPECIFIC FUGITIVE
def getFugitiveInfo():

        fugitive_ID =  getFugitiveID()
        url_fugitive_info = "https://ws-public.interpol.int/notices/v1/red/{0}".format(fugitive_ID)
        response_fugitive_info =  requests.get(url_fugitive_info)
        data_fugitive_info =  response_fugitive_info.json()
        return data_fugitive_info

#TRANSLATE ie FR TO FRANCE
def alphaCodeToCountryOfBirth():

        data_fugitive_info =  getFugitiveInfo()
        country_of_birth = data_fugitive_info['country_of_birth_id']
        countries = list(pycountry.countries)
        for index, country in enumerate(countries):
            if country_of_birth in country.alpha_2:
                country_of_birth = country.name
                return country_of_birth

#TRANSLATE ie FR TO FRANCE
def alphaCodeToCountryWarrant():

        data_fugitive_info =  getFugitiveInfo()
        country_warant = data_fugitive_info['arrest_warrants'][0]['issuing_country_id']
        countries = list(pycountry.countries)
        for index, country in enumerate(countries):
            if country_warant in country.alpha_2:
                country_warant = country.name
                return country_warant

#TGET FUGITIVES IMAGES LINK
def getFugitiveImages():

        fugitiveKey =  getNoticesDetails()
        url_images = fugitiveKey[randomIndex]['_links']['images']['href']
        response_images =  requests.get(url_images)
        data_images =   response_images.json()
        imageLink = data_images['_embedded']['images'][0]['_links']['self']['href']
        return imageLink

# DOWNLOAD IMAGE
def imageDownloader():

        url_image =  getFugitiveImages()
        file_path = 'images/'
        file_name = 'img01'
        full_path = file_path + file_name + '.jpg'
        urllib.request.urlretrieve(url_image, full_path)

imageDownloader()

# DATE OF BIRTH TO INTEGER YEARS OLD 
def findAge():
    
        fugitiveInfo =  getFugitiveInfo()
        date_of_birth = int(fugitiveInfo['date_of_birth'].split('/')[0])
        year = date.today().year
        age = year - date_of_birth
        return age

# DICT TO JSON FORMAT
def InfoToJson():

        data_fugitive_info =  getFugitiveInfo()
        fugitive = {
        "name": data_fugitive_info['name'],
        "forename" : data_fugitive_info['forename'],
        'age' :  findAge(),
        "nat" :  alphaCodeToCountryOfBirth(),
        "marks" : data_fugitive_info['distinguishing_marks'] ,
        "charges" : {
            'for': data_fugitive_info['arrest_warrants'][0]['charge'],
            "by" :  alphaCodeToCountryWarrant()
        },
        'image':  getFugitiveImages()
        } 
        with open('fugitive.json', 'w') as f:
            json.dump(fugitive, f)

InfoToJson()