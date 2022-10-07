import random, math, json, os
import pycountry
import aiohttp, asyncio, time, urllib.request
from datetime import date

#generate random number



def main():

    # generate random number 
    def getRandomNum(min, max):
        return  math.floor(random.uniform(min, max))

    #get list of fugitives from interpol API
    async def getListNotices():

        async with aiohttp.ClientSession() as session:
            randomNum = getRandomNum(1, 200)
            url_notices ="https://ws-public.interpol.int/notices/v1/red?resultPerPage=100&page={0}".format(randomNum)
            response_notices =  await session.get(url_notices)
            data_notices =  await response_notices.json()
            return data_notices

    asyncio.run(getListNotices())  

    async def getNoticesDetails():
        async with aiohttp.ClientSession() as session:
            data_notices = await getListNotices()
            fugitiveKey = list(data_notices['_embedded']["notices"])
            return fugitiveKey
    asyncio.run(getNoticesDetails())

    async def getFugitiveIndex():
        async with aiohttp.ClientSession() as session:
            
            fugitiveKey = await getNoticesDetails()
            fugitivesLength = len(fugitiveKey)
            randomIndex = getRandomNum(0, fugitivesLength)
            return randomIndex

    asyncio.run(getFugitiveIndex())

    async def getFugitiveID():
        async with aiohttp.ClientSession() as session:

            randomIndex = await getFugitiveIndex()
            fugitiveKey = await getNoticesDetails()

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

    asyncio.run(getFugitiveID())

    async def getFugitiveImages():
        async with aiohttp.ClientSession() as session:

            randomIndex = await getFugitiveIndex()
            fugitiveKey = await getNoticesDetails()
            url_images = fugitiveKey[randomIndex]['_links']['images']['href']
            response_images = await session.get(url_images)
            data_images =  await response_images.json()
            imageLink = data_images['_embedded']['images'][0]['_links']['self']['href']
            return imageLink
            
    asyncio.run(getFugitiveImages())

    async def getFugitiveInfo():
        async with aiohttp.ClientSession() as session:

            fugitive_ID = await getFugitiveID()
            url_fugitive_info = "https://ws-public.interpol.int/notices/v1/red/{0}".format(fugitive_ID)
            response_fugitive_info = await session.get(url_fugitive_info)
            data_fugitive_info = await response_fugitive_info.json()
            return data_fugitive_info

    asyncio.run(getFugitiveInfo())

    # change FR to FRANCE
    async def alphaCodeToCountryOfBirth():
        async with aiohttp.ClientSession() as session:

            data_fugitive_info = await getFugitiveInfo()
            country_of_birth = data_fugitive_info['country_of_birth_id']
            countries = list(pycountry.countries)
            for index, country in enumerate(countries):
                if country_of_birth in country.alpha_2:
                    country_of_birth = country.name
                    return country_of_birth

    asyncio.run(alphaCodeToCountryOfBirth())

    async def alphaCodeToCountryWarrant():
        async with aiohttp.ClientSession() as session:

            data_fugitive_info = await getFugitiveInfo()
            country_warant = data_fugitive_info['arrest_warrants'][0]['issuing_country_id']
            countries = list(pycountry.countries)
            for index, country in enumerate(countries):
                if country_warant in country.alpha_2:
                    country_warant = country.name
                    return country_warant

    asyncio.run(alphaCodeToCountryWarrant())

    async def imageDownloader():
        async with aiohttp.ClientSession() as session:

            url_image = await getFugitiveImages()
            file_path = 'images/'
            file_name = 'img01'
            full_path = file_path + file_name + '.jpg'
            urllib.request.urlretrieve(url_image, full_path)

    asyncio.run(imageDownloader()) 

    async def findAge():
        async with aiohttp.ClientSession() as session:

            fugitiveInfo = await getFugitiveInfo()
            randomIndex = await getFugitiveIndex()
            
            date_of_birth = int(fugitiveInfo['date_of_birth'].split('/')[0])
            year = date.today().year
            age = year - date_of_birth
            return age

    asyncio.run(findAge()) 

    async def InfoToJson():
        async with aiohttp.ClientSession() as session:

            data_fugitive_info = await getFugitiveInfo()
            fugitive = {
            "name": data_fugitive_info['name'],
            "forename" : data_fugitive_info['forename'],
            'age' : await findAge(),
            "nat" : await alphaCodeToCountryOfBirth(),
            "marks" : data_fugitive_info['distinguishing_marks'] ,
            "charges" : {
                'for': data_fugitive_info['arrest_warrants'][0]['charge'],
                "by" : await alphaCodeToCountryWarrant()
            },
            'image': await getFugitiveImages()
            } 
            with open('fugitive.json', 'w') as f:
                json.dump(fugitive, f)

    asyncio.run(InfoToJson()) 


main()


            