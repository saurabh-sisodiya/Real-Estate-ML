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
    'referer': 'https://www.99acres.com/residential-land-in-gurgaon-ffid-page',
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

land = pd.DataFrame()

import time

# Put start page number and end page number
start = 1 # Starting Page
end = 50 # End Page

csv_file = f"/Users/saurabhsisodiya/Downloads/RealEstateMLProject/resedential-Land/resedential_land_gurgaon_data-p{start}-{end}.csv"
pageNumber = start
req=0
while pageNumber < end:
    i=1
    url = f'https://www.99acres.com/residential-land-in-gurgaon-ffid-page-{pageNumber}'
    page = requests.get(url, headers=headers)
    pageSoup = BeautifulSoup(page.content, 'html.parser')
    req+=1
    for soup in pageSoup.select_one('div[data-label="SEARCH"]').select('section[data-hydration-on-demand="true"]'):

    # Extract property name and property sub-name
        try:
            property_name = soup.select_one('a.srpTuple__propertyName').text.strip()
            # Extract link
            link = soup.select_one('a.srpTuple__propertyName')['href']

        except:
            continue

        try:
            society = soup.select_one('#srp_tuple_society_heading').text.strip()
        except:
            society = ''
        # Detail Page
        page = requests.get(link, headers=headers)
        dpageSoup = BeautifulSoup(page.content, 'html.parser')
        req+=1
        try:
            #price Range
            price = dpageSoup.select_one('#pdPrice2').text.strip()
        except:
            price = ''

        # Area
        try:
            area = soup.select_one('#srp_tuple_secondary_area').text.strip()
        except:
            area =''
        # # Area with Type
        # try:
        #     areaWithType = dpageSoup.select_one('#factArea').text.strip()
        # except:
        #     areaWithType = ''

        # Address
        try:
            address = dpageSoup.select_one('#address').text.strip()
        except:
            address = ''
        # Floor Number
        try:
            floorNumAllowed = dpageSoup.select_one('#floorNumLabel').text.strip()
        except:
            floorNumAllowed = ''

        try:
            noOfOpenSides = dpageSoup.select_one('#noOfOpenSides').text.strip()
        except:
            noOfOpenSides = ''

        try:
            possession = dpageSoup.select_one('#agePossessionLbl').text.strip()
        except:
            possession = ''

        # Nearby Locations

        try:
            nearbyLocations = [i.text.strip() for i in dpageSoup.select_one('div.NearByLocation__tagWrap').select('span.NearByLocation__infoText')]
        except:
            nearbyLocations = ''

        # Descriptions
        try:
            description = dpageSoup.select_one('#description').text.strip()
        except:
            description = ''



        # Features

        try:
            features = [i.text.strip() for i in dpageSoup.select('#features')[0].select('li')]
        except:
            features = ''




        # Rating by Features
        try:
            rating = [i.text for i in dpageSoup.select_one('div.review__rightSide>div>ul>li>div').select('div.ratingByFeature__circleWrap')]
        except:
            rating = ''
        # print(top_f)

        try:
        # Property ID
            property_id = dpageSoup.select_one('#Prop_Id').text.strip()
        except:
            property_id = ''

        # Create a dictionary with the given variables
        property_data = {
        'property_name': property_name,
        'link': link,
        'society': society,
        'price': price,
        'areaWithType': area,

        'address': address,
        'floorNumAllowed': floorNumAllowed,
        'noOfOpenSides': noOfOpenSides,
        'possession': possession,
        'nearbyLocations': nearbyLocations,
        'description': description,

        'features': features,
        'rating':rating,
        'property_id': property_id
    }


        temp_df = pd.DataFrame.from_records([property_data])
        # print(temp_df)
        land = pd.concat([land, temp_df], ignore_index=True)
        i += 1

        if os.path.isfile(csv_file):
        # Append DataFrame to the existing file without header
            temp_df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            # Write DataFrame to the file with header
            temp_df.to_csv(csv_file, mode='a', header=True, index=False)




    print(f'{pageNumber} -> {i}')
    pageNumber += 1

    if req%4==0:
        time.sleep(10)
    if req %20==0:
        time.sleep(20)

land.to_csv('/Users/saurabhsisodiya/Downloads/RealEstateMLProject/resedential-Land/resedential_land_gurgaon_data-p1-100_2122rows.csv', index=False)

def combine_csv_files(folder_path, combined_file_path):
    combined_data = pd.DataFrame()  # Create an empty DataFrame to hold the combined data

    # Iterate through all CSV files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            print('file_path')
            # Read the data from the current CSV file
            df = pd.read_csv(file_path)

            # Append the data to the combined DataFrame
            combined_data = combined_data.append(df, ignore_index=True)

            # Delete the original CSV file
            os.remove(file_path)

    # Save the combined data to a new CSV file
    combined_data.to_csv(combined_file_path, index=False)

# Example usage:
folder_path = '/Users/saurabhsisodiya/Downloads/RealEstateMLProject/resedential-Land'  # Replace with the actual folder path
combined_file_path = '/Users/saurabhsisodiya/Downloads/RealEstateMLProject/resedential-Land/residential-land.csv'  # Replace with the desired combined file path

combine_csv_files(folder_path, combined_file_path)

pd.read_csv(combined_file_path)
