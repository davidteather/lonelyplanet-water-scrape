from selenium import webdriver
import time
import requests


scrape = True
citiesB = True
# Gets countries
# https://cms.lonelyplanet.com/graphql?operationName=descendantsQuery&variables=%7B%22limit%22%3A12%2C%22placeType%22%3A%5B%22Country%22%5D%2C%22sort%22%3A%5B%7B%22field%22%3A%22field_plc_poi_count%22%7D%2C%7B%22field%22%3A%22field_plc_top_choice_poi_count%22%7D%5D%2C%22offset%22%3A12%2C%22entityId%22%3A%2236%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%220ea1810f01b3bf8688b460d8c4dd182ce576772cb407619c6e63d0188c255c24%22%7D%7D

if scrape:
    more = True
    cities = []
    offset = 0
    if citiesB:
        while more:
            typeReq = "City"
            url = "https://cms.lonelyplanet.com/graphql?operationName=descendantsQuery&variables=%7B%22limit%22%3A12%2C%22placeType%22%3A%5B%22" + typeReq + "%22%5D%2C%22sort%22%3A%5B%7B%22field%22%3A%22field_plc_poi_count%22%7D%2C%7B%22field%22%3A%22field_plc_top_choice_poi_count%22%7D%5D%2C%22offset%22%3A" + str(offset) + "%2C%22entityId%22%3A%2236%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%220ea1810f01b3bf8688b460d8c4dd182ce576772cb407619c6e63d0188c255c24%22%7D%7D"
            data = requests.get(url).json()

           #  print(data)
            if len(data['data']['nodeQuery']['entities']) == 0:
                more = False
            else:
                for x in data['data']['nodeQuery']['entities']:
                    #if x['fieldPlcSlug'] == None:
                    #    if x['fieldPlcAncestry'][0]['entity']['fieldPlcSlug'] != None:
                    #        cities.append(x['fieldPlcName'] + "\t" + x['fieldPlcAncestry'][0]['entity']['fieldPlcSlug'])
                    #else:
                    if x['fieldPlcSlug'] != None and x['fieldPlcSlug'] != None:
                        print("x")
                        cities.append(x['fieldPlcName'] + "\t" + x['fieldPlcSlug'])
                    offset += 1

    countries = []

    offset = 0

    more = True
    while more:
        typeReq = "Country"
        url = "https://cms.lonelyplanet.com/graphql?operationName=descendantsQuery&variables=%7B%22limit%22%3A12%2C%22placeType%22%3A%5B%22" + typeReq + "%22%5D%2C%22sort%22%3A%5B%7B%22field%22%3A%22field_plc_poi_count%22%7D%2C%7B%22field%22%3A%22field_plc_top_choice_poi_count%22%7D%5D%2C%22offset%22%3A" + str(offset) + "%2C%22entityId%22%3A%2236%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%220ea1810f01b3bf8688b460d8c4dd182ce576772cb407619c6e63d0188c255c24%22%7D%7D"
        data = requests.get(url).json()
        #print(url)

        if len(data['data']['nodeQuery']['entities']) == 0:
            more = False
        else:
            for x in data['data']['nodeQuery']['entities']:
                #if x['fieldPlcSlug'] == None:
                #    countries.append(x['fieldPlcName'] + "\t" + x['fieldPlcAncestry'][0]['entity']['fieldPlcSlug'])
                #else:
                if x['fieldPlcSlug'] != None and x['fieldPlcName'] != None:
                    countries.append(x['fieldPlcName'] + "\t" + x['fieldPlcSlug'])
                offset += 1

    with open("data.csv", 'w+', encoding='utf-8') as f:
        f.write(str(len(cities)) + "\n")
        for city in cities:
            f.write(city + "\n")

        print(countries)
        for country in countries:
            f.write(country + "\n")

with open("data.csv", 'r', encoding='utf-8') as inp:
    lines = inp.readlines()
    cityCount = int(lines[0].replace("\n", ""))

    citiesSlug = []
    citiesName = []
    for city in range(1,cityCount+1):
       citiesSlug.append(lines[city].replace("\n", "").split("\t")[1])
       citiesName.append(lines[city].replace("\n", "").split("\t")[0])

    countriesSlug = []
    countriesName = []
    for country in range(cityCount+1, len(lines)):
        countriesSlug.append(lines[country].replace("\n", "").split("\t")[1])
        countriesName.append(lines[country].replace("\n", "").split("\t")[0])
        #countriesName = countries
        #countriesSlug = countriesSlug

with open("cities.csv", 'w+', encoding='utf-8') as f:
    print("Created cities")

with open("countries.csv", 'w+', encoding='utf-8') as f:
    print("Created countries")

driver = webdriver.Chrome()

with open("cities.csv", 'a', encoding='utf-8') as output:
    output.write("City,Link,Content\n")


if citiesB:

    for x in range(0,len(citiesSlug)):
        print(x)
        try:
            driver.get("https://www.lonelyplanet.com/{}/health".format(citiesSlug[x]))
            time.sleep(3)
            # driver.get("https://www.lonelyplanet.com/france/health")
            body = driver.find_element_by_xpath("//div[@class='layer__content card--page__content context--content js-layer-content']").get_attribute("innerHTML")
            

            try:
                # Handles error if slug not found
                split = body.split('<h3 class="copy--h3">')
            except:
                split = []
            #print(split)

            for y in range(0,len(split)):
                if "Tap Water</h3>" in split[y]:
                    print(split)
                    tapWater = split[y].split('</h3>\n<div class="copy--body">\n')[1].split('<h2 class="copy--h2">')[0] \
                        .replace("\n", "").replace("<p>", "").replace("</p>", "").replace("Tap Water</h2>", "").replace("</h3>", "") \
                        .replace("<em>", "").replace("</em>", "").replace("</div>", "").replace("<div>", "").replace(",", "%2C")
                    with open("cities.csv", 'a', encoding='utf-8') as output:
                        output.write("{},{},{}\n".format(citiesName[x], "https://www.lonelyplanet.com/{}/health".format(citiesSlug[x]), tapWater))
        except:
            print("Errored Out")


with open("countries.csv", 'a', encoding='utf-8') as output:
    output.write("Country,Link,Content\n")


for x in range(0,len(countriesSlug)):
    try:
        driver.get("https://www.lonelyplanet.com/{}/health".format(countriesSlug[x]))
        # driver.get("https://www.lonelyplanet.com/france/health")
        body = driver.find_element_by_xpath("//div[@class='layer__content card--page__content context--content js-layer-content']").get_attribute("innerHTML")
        

        try:
            # Handles error if slug not found
            split = body.split('<h3 class="copy--h3">')
        except:
            split = []
        #print(split)

        for y in range(0,len(split)):
            if "Tap Water</h3>" in split[y]:
                tapWater = split[y].split('</h3>\n<div class="copy--body">\n')[1].split('<h2 class="copy--h2">')[0] \
                    .replace("\n", "").replace("<p>", "").replace("</p>", "").replace("Tap Water</h2>", "").replace("</h3>", "") \
                    .replace("<em>", "").replace("</em>", "").replace("</div>", "").replace("<div>", "").replace(",", "%2C")
                with open("countries.csv", 'a', encoding='utf-8') as output:
                    output.write("{},{},{}\n".format(countriesName[x], "https://www.lonelyplanet.com/{}/health".format(countriesSlug[x]), tapWater))
    except:
        print("errored country")


driver.quit()