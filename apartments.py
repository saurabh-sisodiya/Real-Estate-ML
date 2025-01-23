# Importing Libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time


# Headers set like below:
# User Agent
headers = {
    'authority': 'www.99acres.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.99acres.com/property-in-gurgaon-ffid',
    'sec-ch-ua': '"Chromium";v="107", "Not;A=Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/527.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}
# Extract function

def extract_data(pageSoup):
    global i
    d = pd.DataFrame()
    for soup in pageSoup.select_one('div[data-label="SEARCH"]').select('section[data-hydration-on-demand="true"]'):

        # Extract property name and property sub-name
        try:
            property_name = soup.find('a', class_='projectTuple__projectName').text.strip()
            property_sub_name = soup.find('h2', class_='projectTuple__subHeadingWrap').text.strip()
            # print(property_name+'\n'+property_sub_name)
            # Extract link
            link = soup.select_one('a', class_='projectTuple__projectName')['href']

            page = requests.get(link, headers=headers)
            dpageSoup = BeautifulSoup(page.content, 'html.parser')
            top_f=[]
            top_facilities = dpageSoup.find('div',id='top-facilities').find_all('div', class_="UniquesFacilities__xidFacilitiesCard")
            for facilities in top_facilities :
                top_f.append(facilities.text.strip())

            # print(top_f)
            # Extract Nearbay Locations with Distances
            LocationAdvantages = {}
            for l in dpageSoup.select_one('div[data-label="LOCATION_HIGHLIGHTS"]').select('div.locAdvantagesCard__locAdCard'):
                t = l.find('div').find_all('div')
                loaction = t[0].text.strip()
                distance = t[1].text.strip()
                LocationAdvantages[loaction] = distance

            # Extract nearby locations
            nearby_elements = soup.find_all('div', class_="SliderTagsAndChips__container")[0].find_all('li', class_ = 'SliderTagsAndChips__item')
            nearby = [element.text.strip() for element in nearby_elements]


            #price Range
            price_range = soup.find('div', class_="pageComponent configurationCards__srpCardStyle").text

            # Extract price details
            prices_details = {}
            price_elements =  soup.find('div', class_ = 'carousel__CarouselBox').find_all('div', class_="configurationCards__cardContainer")
            for element in price_elements:
                bedroom_type = element.select_one('span.configurationCards__configBandLabel').text.strip()
                building_type = element.select_one('span.configurationCards__configBandHeading').text.strip()
                area_type = element.select_one('span.configurationCards__cardAreaTypeStyle').text.strip()
                area = element.select_one('span.configurationCards__cardAreaSubHeadingOne').text.strip()
                price_range = element.select_one('span.configurationCards__cardPriceHeading').text.strip()

                prices_details[bedroom_type] = {
                    'building_type': building_type,
                    'area_type' : area_type,
                    'area': area,
                    'price-range': price_range
                }
            # # Print the extracted data
            # print("Property Name: ", property_name)
            # print("Property Sub-name: ", property_sub_name)
            # print("Nearby Locations: ", nearby)
            # print("Location Advantages: ", LocationAdvantages)
            # print("Link: ", link)
            # print("Price Details: ", prices_details)
            # print('Top Facilities: ', top_f)


            # Create a dictionary with the given variables
            data_dict = {
                "PropertyName": property_name,
                "PropertySubName": property_sub_name,
                "NearbyLocations": nearby,
                "LocationAdvantages": LocationAdvantages,
                "Link": link,
                "PriceDetails": prices_details,
                "TopFacilities": top_f
            }

            temp_df = pd.DataFrame.from_records([data_dict])
            # print(temp_df)
            d = pd.concat([d, temp_df], ignore_index=True)


        except:
            # print('No Data')
            pass
        i += 1
    return d


pageNumber=1
i=1
# Create an empty DataFrame
df = pd.DataFrame()

# Specify the file path for the CSV file
file_path = "appartment_data.csv"
# df.to_csv(file_path, mode='a', index=False)

while pageNumber < 50:
    URL = f'https://www.99acres.com/property-in-gurgaon-ffid-page-{pageNumber}'
    page = requests.get(URL, headers=headers)
    pageSoup = BeautifulSoup(page.content, 'html.parser')
    try:
        data = extract_data(pageSoup)

        # Append the dictionary as a row in the DataFrame
        if df.empty:
            df = pd.concat([data, df], ignore_index=True)
            data.to_csv(file_path, index=False)
        else:
            df = pd.concat([data, df], ignore_index=True)
            data.to_csv(file_path, mode='a', index=False, header=False)

        print(f"Data Extracted from {pageNumber}  : {data.shape}. Total Data : {df.shape} ")
        pageNumber += 1
    except:
        print("Request Might be decline- waiting for 50 sec to request again.")
        time.sleep(50)
# print(soup.prettify())

df.shape

data = pd.read_csv('/content/appartment_data.csv')

data.shape
data.drop_duplicates()
