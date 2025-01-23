# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

'''
# why import requests - This imports the requests module, which is a popular python module used to send HTTP requests to websites.
# why from bs4 import BeautifulSoup - This imports BeautifulSoup from the bs4 module. BeautifulSoup is a library that is used for web scrapping purposes to pull the data out of HTML and XML files. It creats a parse tree that can be used to extract data in hierarhical and more readable manner.
# why import os - This imports the os module, which provides a way of interacting with the operating system. This could be used for tasks like creating directories, reading environment variables, etc.
# why headers = {...} - This defines a dictionary called headers with a 'User-Agent' key. The value of this key is a sring taht represents a user agent string. The user agent string is used to tell the server about the browser and operating system of the user. Some websites serve different content based on the user
agent or even block certain user agents (ofter to prevent scrapping). By defining a common browser's user agent sring , this code is trying to mimic a real browser request to potentially avoid blocks or get the same content a real user would see.
'''

City = 'chandigarh'

# user agent
# headers set like below:
headers = {
    'authority': 'www.99acres.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': f'https://www.99acres.com/flats-in-{City}-ffid-page',
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

# Defining the path 
project_dir = '/Users/saurabhsisodiya/Downloads/RealEstateMLProject'
# current_path = os.getcwd()
# print(current_path)

# Define the subdirectories
subdirectories = ['Data', f'Data/{City}', f'Data/{City}/Flats', f'Data/{City}/Societies', f'Data/{City}/Residential', f'Data/{City}/Independent House']

# Create the directory structure
for subdir in subdirectories:
    dir_path = os.path.join(project_dir, subdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")

'''
# Directory structure is created
# Putting start page number and end page number
# Page number to start extraction data
start = int(input("Enter page number where you got error in last run. \nEnter page number to start from:")) 

# End Pagenumber - you can change it for start 
end=start + 10
pageNumber=start
req=0
flats=pd.DataFrame()

try:
    while pageNumber < end:
        i=1
        url=f'https://www.99acres.com/flats-in-{City}-ffid-page-{pageNumber}'
        page=requests.get(url,headers=headers)
        pageSoup=BeautifulSoup(page.content, 'html.parser')
        req+=1
        
        for soup in pageSoup.select_one('div[data-label="SEARCH"]').select('section[data-hydration-on-demand="true"]'):
            # Extract property name and property sub-name
            try:
                property_name = soup.select_one('a.srpTuple__propertyName').text.strip()
                # Extract link
                link = soup.select_one('a.srpTuple__propertyName')['href']
                society = soup.select_one('#srp_tuple_society_heading').text.strip()
            except:
                continue
            # Detail Page
            page = requests.get(link, headers=headers)
            dpageSoup = BeautifulSoup(page.content, 'html.parser')
            req += 1

            try:
                # price range
                price = dpageSoup.select_one('#pdPrice2').text.strip()
            except:
                price=''
            
            # area
            try:
                # area
                area = dpageSoup.select_one('#srp_tuple_price_per_unit_area').text.strip()
            except:
                area=''
            # area with type
            try:
                areaWithType = dpageSoup.select_one("#factArea").text.strip()
            except:
                areaWithType = ''

            try:
                # configuration
                bedRoom = dpageSoup.select_one('#bedRoomNum').text.strip()
            except:
                bedRoom=''
            
            try:
                # bathroom
                bathroom = dpageSoup.select_one('#bathroomNum').text.strip()
            except:
                bathroom=''
            
            try:
                # balcony 
                balcony = dpageSoup.select_one('#balconyNum').text.strip()
            except:
                balcony=''
            
            try:
                # additional room
                additionalRoom = dpageSoup.select_one('#additionalRooms').text.strip()
            except:
                additionalRoom=''
            try:
                # address
                address = dpageSoup.select_one('#address').text.strip()
            except:
                address=''
            try:
                # floor number
                floorNum = dpageSoup.select_one('#floorNumLabel').text.strip()
            except:
                floorNum=''
            try:
                # facing
                facing = dpageSoup.select_one('#facingLabel').text.strip()
            except:
                facing=''
            
            try:
                # price range
                agePossession = dpageSoup.select_one('#agePossessionLbl').text.strip()
            except:
                agePossession=''
            
            try:
                # near by locations 
                nearbyLocations = [i.text.strip() for i in dpageSoup.select_one('div.NearByLocation__tagWrap').select('span.NearByLocation__infoText')]
            except:
                nearbyLocations=''
            
            # description
            try:
                description = dpageSoup.select_one('#description').text.strip()
            except:
                description = ''
            
            # Furnish Details
            try: 
                furnishDetails = [i.text.strip() for i in dpageSoup.select_one('#FurnishDetails').select('li')]
            except:
                furnishDetails = ''
            
            # Features
            if furnishDetails:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[1].select['li']]
                except:
                    features = ''
            else:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[0].select['li']]
                except:
                    features = ''

            # Rating by features
            try:
                rating = [i.text for i in dpageSoup.select_one('div.review__rightSide>div>ul>li>div').select('div.ratingByFeature__circleWrap')]
            except:
                rating = ''
            
            try:
                # property id
                property_id = dpageSoup.select_one('#Prop_Id').text.strip()
            except:
                property_id = ''
            
            # Create a dictionary with the given variables
            property_data = {
                'property_name': property_name,
                'link': link,
                'society': society,
                'price': price,
                'area': area,
                'areaWithType': areaWithType,
                'bedRoom': bedRoom,
                'bathroom': bathroom,
                'balcony': balcony,
                'additionalRoom': additionalRoom,
                'address': address,
                'floorNum': floorNum,
                'facing': facing,
                'agePossesion': agePossession,
                'nearbyLocations': nearbyLocations,
                'description': description,
                'furnishDetails': furnishDetails,
                'features': features,
                'rating': rating,
                'property_id': property_id
            }

            temp_df = pd.DataFrame.from_records([property_data])
            flats = pd.concat([flats, temp_df], ignore_index=True)
            i+=1

            if req % 4 == 0:
                time.sleep(10)
            if req % 15 == 0:
                time.sleep(50)
        print(f'{pageNumber} -> {i}')
        pageNumber+=1
except AttributeError as e:
    print(e)
    print('-'*10)
    '''
    # print('''
        # Your IP might have blocked. Delete Runtime and reconnect again with updating start page number. \n
        # You would see in output above like 1 -> 15\ and so 1 is page nuber and 15 is data items extracted.''')
'''
    csv_file_path = f"/Users/saurabhsisodiya/Downloads/RealEstateMLProject/Data/chandigarh/Flats/flats_{City}_data-page-{start}-{pageNumber-1}.csv"
    
    # This file will be new every time if start page will change, but still taking here mode as append
    if os.path.isfile(csv_file_path):
        # Append DataFrame to the existing file without header
        flats.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        # Write DataFrame to the file with header - first time write
        flats.to_csv(csv_file_path, mode='a', header=True, index=False)
         
'''  

# Page number to start extraction data
start = int(input("Enter page number where you got error in last run.\nEnter page number to start from:")) # Starting Page

# End Page number- you can change is for start i am taking 10pages at a time,
# as IPs are gettig block after some time
end = start+10

pageNumber = start
req=0

flats = pd.DataFrame()

try :
    while pageNumber < end:
        i=1
        url = f'https://www.99acres.com/flats-in-{City}-ffid-page-{pageNumber}'
        page = requests.get(url, headers=headers)
        pageSoup = BeautifulSoup(page.content, 'html.parser')
        req+=1
        for soup in pageSoup.select_one('div[data-label="SEARCH"]').select('section[data-hydration-on-demand="true"]'):

        # Extract property name and property sub-name
            try:
                property_name = soup.select_one('a.srpTuple__propertyName').text.strip()
                # Extract link
                link = soup.select_one('a.srpTuple__propertyName')['href']
                society = soup.select_one('#srp_tuple_society_heading').text.strip()
            except:
                continue
            # Detail Page
            page = requests.get(link, headers=headers)
            dpageSoup = BeautifulSoup(page.content, 'html.parser')
            req += 1
            try:
                #price Range
                price = dpageSoup.select_one('#pdPrice2').text.strip()
            except:
                price = ''

            # Area
            try:
                area = soup.select_one('#srp_tuple_price_per_unit_area').text.strip()
            except:
                area =''
            # Area with Type
            try:
                areaWithType = dpageSoup.select_one('#factArea').text.strip()
            except:
                areaWithType = ''


            # Configuration
            try:
                bedRoom = dpageSoup.select_one('#bedRoomNum').text.strip()
            except:
                bedRoom = ''
            try:
                bathroom = dpageSoup.select_one('#bathroomNum').text.strip()
            except:
                bathroom = ''
            try:
                balcony = dpageSoup.select_one('#balconyNum').text.strip()
            except:
                balcony = ''

            try:
                additionalRoom = dpageSoup.select_one('#additionalRooms').text.strip()
            except:
                additionalRoom = ''


            # Address

            try:
                address = dpageSoup.select_one('#address').text.strip()
            except:
                address = ''
            # Floor Number
            try:
                floorNum = dpageSoup.select_one('#floorNumLabel').text.strip()
            except:
                floorNum = ''

            try:
                facing = dpageSoup.select_one('#facingLabel').text.strip()
            except:
                facing = ''

            try:
                agePossession = dpageSoup.select_one('#agePossessionLbl').text.strip()
            except:
                agePossession = ''

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

            # Furnish Details
            try:
                furnishDetails = [i.text.strip() for i in dpageSoup.select_one('#FurnishDetails').select('li')]
            except:
                furnishDetails = ''

            # Features
            if furnishDetails:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[1].select('li')]
                except:
                    features = ''
            else:
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
            'area': area,
            'areaWithType': areaWithType,
            'bedRoom': bedRoom,
            'bathroom': bathroom,
            'balcony': balcony,
            'additionalRoom': additionalRoom,
            'address': address,
            'floorNum': floorNum,
            'facing': facing,
            'agePossession': agePossession,
            'nearbyLocations': nearbyLocations,
            'description': description,
            'furnishDetails': furnishDetails,
            'features': features,
            'rating': rating,
            'property_id': property_id
        }


            temp_df = pd.DataFrame.from_records([property_data])
            # print(temp_df)
            flats = pd.concat([flats, temp_df], ignore_index=True)
            i += 1
            # if os.path.isfile(csv_file):
            # # Append DataFrame to the existing file without header
            #     temp_df.to_csv(csv_file, mode='a', header=False, index=False)
            # else:
            #     # Write DataFrame to the file with header
            #     temp_df.to_csv(csv_file, mode='a', header=True, index=False)

            if req % 4==0:
                time.sleep(10)
            if req % 15 == 0:
                time.sleep(50)
        print(f'{pageNumber} -> {i}')
        pageNumber += 1

except AttributeError as e:
    print(e)
    print("----------------")
    print("""Your IP might have blocked. Delete Runitme and reconnect again with updating start page number.\n
            You would see in output above like 1 -> 15\ and so 1 is page number and 15 is data items extracted.""")
    csv_file_path = f"/Users/saurabhsisodiya/Downloads/RealEstateMLProject/chandigarh/Flats/flats_{City}_data-page-{start}-{pageNumber-1}.csv"

    # This file will be new every time if start page will chnage, but still taking here mode as append
    if os.path.isfile(csv_file_path):
    # Append DataFrame to the existing file without header
        flats.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        # Write DataFrame to the file with header - first time write
        flats.to_csv(csv_file_path, mode='a', header=True, index=False)

             
# Function to combine multiple csv file is one file.

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

# Replace with the actual folder path
folder_path = ''

# Replace with the desired combined file path
combined_file_path = '/Users/saurabhsisodiya/Downloads/RealEstateMLProject/flats.csv'

combine_csv_files(folder_path, combined_file_path)
'''
Skip to main content
flats-appartment.ipynb
flats-appartment.ipynb_
Changes will not be saved

'''
# Imports

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
'''
Overview

This code sets up the necessary tools and headers to scrape web data. It imports libraries for sending HTTP requests, parsing HTML, and handling data. Additionally, it defines a user agent header to mimic a web browser, which can be useful to avoid getting blocked by some websites.

import requests

This line imports the requests module, which is a popular Python module used to send HTTP requests to websites.

from bs4 import BeautifulSoup This line imports BeautifulSoup from the bs4 module. BeautifulSoup is a library that is used for web scraping purposes to pull the data out of HTML and XML files. It creates a parse tree that can be used to extract data in a hierarchical and more readable manner.

import os

This line imports the os module, which provides a way of interacting with the operating system. This could be used for tasks like creating directories, reading environment variables, etc.

headers = {...}

This line defines a dictionary called headers with a 'User-Agent' key. The value of this key is a string that represents a user agent string.

The user agent string is used to tell the server about the browser and operating system of the user. Some websites serve different content based on the user agent or even block certain user agents (often to prevent scraping). By defining a common browser's user agent string, this code is trying to mimic a real browser request to potentially avoid blocks or get the same content a real user would see.

Extracting Flats/Apartments
- Your_Project_Directory
  - Data
    - City
      - Flats
      - Societies
      - Residential
      - Independent House

[ ]

Start coding or generate with AI.
'''
[ ]
# Need to change as per your requirement - city name
# Match with 99acers site like for chandighars flats data site is : https://www.99acres.com/flats-in-chandigarh-ffid
# Taking value of city as 'chandigarh'
City = 'chandigarh'

[ ]
# User Agent
# Headers set like below:
# User Agent
headers = {
    'authority': 'www.99acres.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': f'https://www.99acres.com/flats-in-{City}-ffid-page',
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

[ ]
# If folder structures are in already created no need to run it.

import os

# Define the path to your project directory
project_dir = '/content/drive/MyDrive/DSMP/Case Studies/Real estate/'

# Define the subdirectories
subdirectories = ['Data', f'Data/{City}', f'Data/{City}/Flats', f'Data/{City}/Societies', f'Data/{City}/Residential', f'Data/{City}/Independent House']

# Create the directory structure
for subdir in subdirectories:
    dir_path = os.path.join(project_dir, subdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")

# Now, your directory structure is created.


[ ]
# Put start page number and end page number.

# Page number to start extraction data
start = int(input("Enter page number where you got error in last run.\nEnter page number to start from:")) # Starting Page

# End Page number- you can change is for start i am taking 10pages at a time,
# as IPs are gettig block after some time
end = start+10

pageNumber = start
req=0

flats = pd.DataFrame()

try :
    while pageNumber < end:
        i=1
        url = f'https://www.99acres.com/flats-in-{City}-ffid-page-{pageNumber}'
        page = requests.get(url, headers=headers)
        pageSoup = BeautifulSoup(page.content, 'html.parser')
        req+=1
        for soup in pageSoup.select_one('div[data-label="SEARCH"]').select('section[data-hydration-on-demand="true"]'):

        # Extract property name and property sub-name
            try:
                property_name = soup.select_one('a.srpTuple__propertyName').text.strip()
                # Extract link
                link = soup.select_one('a.srpTuple__propertyName')['href']
                society = soup.select_one('#srp_tuple_society_heading').text.strip()
            except:
                continue
            # Detail Page
            page = requests.get(link, headers=headers)
            dpageSoup = BeautifulSoup(page.content, 'html.parser')
            req += 1
            try:
                #price Range
                price = dpageSoup.select_one('#pdPrice2').text.strip()
            except:
                price = ''

            # Area
            try:
                area = soup.select_one('#srp_tuple_price_per_unit_area').text.strip()
            except:
                area =''
            # Area with Type
            try:
                areaWithType = dpageSoup.select_one('#factArea').text.strip()
            except:
                areaWithType = ''


            # Configuration
            try:
                bedRoom = dpageSoup.select_one('#bedRoomNum').text.strip()
            except:
                bedRoom = ''
            try:
                bathroom = dpageSoup.select_one('#bathroomNum').text.strip()
            except:
                bathroom = ''
            try:
                balcony = dpageSoup.select_one('#balconyNum').text.strip()
            except:
                balcony = ''

            try:
                additionalRoom = dpageSoup.select_one('#additionalRooms').text.strip()
            except:
                additionalRoom = ''


            # Address

            try:
                address = dpageSoup.select_one('#address').text.strip()
            except:
                address = ''
            # Floor Number
            try:
                floorNum = dpageSoup.select_one('#floorNumLabel').text.strip()
            except:
                floorNum = ''

            try:
                facing = dpageSoup.select_one('#facingLabel').text.strip()
            except:
                facing = ''

            try:
                agePossession = dpageSoup.select_one('#agePossessionLbl').text.strip()
            except:
                agePossession = ''

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

            # Furnish Details
            try:
                furnishDetails = [i.text.strip() for i in dpageSoup.select_one('#FurnishDetails').select('li')]
            except:
                furnishDetails = ''

            # Features
            if furnishDetails:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[1].select('li')]
                except:
                    features = ''
            else:
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
            'area': area,
            'areaWithType': areaWithType,
            'bedRoom': bedRoom,
            'bathroom': bathroom,
            'balcony': balcony,
            'additionalRoom': additionalRoom,
            'address': address,
            'floorNum': floorNum,
            'facing': facing,
            'agePossession': agePossession,
            'nearbyLocations': nearbyLocations,
            'description': description,
            'furnishDetails': furnishDetails,
            'features': features,
            'rating': rating,
            'property_id': property_id
        }


            temp_df = pd.DataFrame.from_records([property_data])
            # print(temp_df)
            flats = pd.concat([flats, temp_df], ignore_index=True)
            i += 1
            # if os.path.isfile(csv_file):
            # # Append DataFrame to the existing file without header
            #     temp_df.to_csv(csv_file, mode='a', header=False, index=False)
            # else:
            #     # Write DataFrame to the file with header
            #     temp_df.to_csv(csv_file, mode='a', header=True, index=False)

            if req % 4==0:
                time.sleep(10)
            if req % 15 == 0:
                time.sleep(50)
        print(f'{pageNumber} -> {i}')
        pageNumber += 1

except AttributeError as e:
    print(e)
    print("----------------")
    print("""Your IP might have blocked. Delete Runitme and reconnect again with updating start page number.\n
            You would see in output above like 1 -> 15\ and so 1 is page number and 15 is data items extracted.""")
    csv_file_path = f"/content/drive/MyDrive/DSMP/Case Studies/Real estate/Data/chandigarh/Flats/flats_{City}_data-page-{start}-{pageNumber-1}.csv"

    # This file will be new every time if start page will chnage, but still taking here mode as append
    if os.path.isfile(csv_file_path):
    # Append DataFrame to the existing file without header
        flats.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        # Write DataFrame to the file with header - first time write
        flats.to_csv(csv_file_path, mode='a', header=True, index=False)
'''
Enter page number where you got error in last run.
Enter page number to start from:5
'NoneType' object has no attribute 'select'
----------------
Your IP might have blocked. Delete Runitme and reconnect again with updating start page number.

            You would see in output above like 1 -> 15\ and so 1 is page number and 15 is data items extracted.
If getting errors
Solution for colab
Go to menu bar:
Runtime -> Disconnect and Delete runtime -> Reconnect again.

- **Initialization of Variables**:

    - start and end specify the range of web pages to scrape.
    - csv_file defines the path to the CSV file where data will be saved.
    - pageNumber starts from the initial value of start and will be incremented to navigate through the pages.
    - req counts the number of HTTP requests made.

- **Loop for Page Navigation**:

Overview

The code scrapes property data from the website "99acres.com" for apartments in Gurgaon. It navigates through a range of pages, extracts details of each property, and saves the data to a CSV file. The script is designed to handle potential errors gracefully, using try and except blocks to manage missing data, and introduces pauses to avoid making rapid requests and potentially getting blocked by the website.

Initialization of Variables:

start and end specify the range of web pages to scrape.
csv_file defines the path to the CSV file where data will be saved.
pageNumber starts from the initial value of start and will be incremented to navigate through the pages.
req counts the number of HTTP requests made.
Loop for Page Navigation:

The while loop is used to navigate through each page in the range from start to end.
Inside this loop, the URL of the page to be scraped is constructed using the pageNumber.
An HTTP GET request is made to retrieve the content of the page, and the content is then parsed using BeautifulSoup.
Loop for Property Extraction:

The nested for loop navigates through individual property sections on the current page.
The script attempts to extract the property name, its link, and its society name.
If any of these attributes are missing, it skips to the next property.
Detail Extraction:

For each property, an HTTP request is made to its detail page.
The code then attempts to extract various property details like price, area, bedroom count, bathroom count, balcony count, address, and many other attributes. If any attribute is missing, the code handles it gracefully, assigning an empty string or an empty list as appropriate.
Creating and Saving Data:

All extracted details are stored in a dictionary named property_data.
This dictionary is then converted to a temporary DataFrame temp_df.
The data is appended to a main DataFrame flats and also saved to the CSV file. If the file already exists, the new data is appended without writing the headers again.
Request Management:

To avoid making too many rapid requests (which can lead to IP bans), the script introduces pauses.
Every 4 requests, it pauses for 10 seconds. Every 15 requests, it pauses for 50 seconds.
Page Counter and Loop Increment:

After scraping all properties on a page, the code prints the page number and the number of properties processed.
pageNumber is incremented to move to the next page.

[ ]
# Function to combine multiple csv file is one file.

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

# Replace with the actual folder path
folder_path = '/content/drive/MyDrive/DSMP/Case Studies/Real estate/flats_appartment'

# Replace with the desired combined file path
combined_file_path = '/content/drive/MyDrive/DSMP/Case Studies/Real estate/flats_appartment/flats.csv'

combine_csv_files(folder_path, combined_file_path)
'''
'''
file_path
<ipython-input-7-26a7d1242761>:13: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  combined_data = combined_data.append(df, ignore_index=True)
<ipython-input-7-26a7d1242761>:13: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  combined_data = combined_data.append(df, ignore_index=True)
file_path
Overview: The function combine_csv_files combines all the CSV files located in a specified folder into a single CSV file. After appending the data from each individual file to the combined file, the original file is deleted.

Function Definition:

combine_csv_files(folder_path, combined_file_path):

folder_path: Path to the folder containing the CSV files you want to combine.
combined_file_path: Path where the combined CSV file should be saved.
Initialize an Empty DataFrame:

combined_data = pd.DataFrame(): An empty DataFrame combined_data is created to hold all the data from the individual CSV files.
Iterate Through CSV Files:

The for loop iterates over each file in the directory specified by folder_path.
Within the loop, the code checks if the current file ends with .csv to ensure that only CSV files are processed.
Read and Append Data:

file_path = os.path.join(folder_path, file_name): Constructs the full path to the current CSV file.
df = pd.read_csv(file_path): Reads the data from the current CSV file into a DataFrame df.
combined_data = combined_data.append(df, ignore_index=True): Appends the data from df to the combined_data DataFrame. The ignore_index=True parameter ensures that the index is reset and continuous in the combined data.
Delete the Original CSV File:

os.remove(file_path): Deletes the original CSV file after its data has been appended to the combined data. This step helps in conserving storage space.
Save the Combined Data:

combined_data.to_csv(combined_file_path, index=False): Writes the combined_data DataFrame to a new CSV file at the specified combined_file_path. The parameter index=False ensures that the DataFrame's index is not written to the CSV.
Example Usage:

The provided paths (folder_path and combined_file_path) specify the location of the individual CSV files and the path for the combined CSV file, respectively.
Calling the combine_csv_files function with these paths will combine all CSV files in the specified folder and save the combined data to the desired location.

[ ]
pd.read_csv(combined_file_path)

Colab paid products - Cancel contracts here
'''
'''
Overview: The function combine_csv_files combines all the CSV files located in a specified folder into a single CSV file. After appending the data from each individual file to the combined file, the original file is deleted.

Function Definition:

combine_csv_files(folder_path, combined_file_path):

folder_path: Path to the folder containing the CSV files you want to combine.
combined_file_path: Path where the combined CSV file should be saved.
Initialize an Empty DataFrame:

combined_data = pd.DataFrame(): An empty DataFrame combined_data is created to hold all the data from the individual CSV files.
Iterate Through CSV Files:

The for loop iterates over each file in the directory specified by folder_path.
Within the loop, the code checks if the current file ends with .csv to ensure that only CSV files are processed.
Read and Append Data:

file_path = os.path.join(folder_path, file_name): Constructs the full path to the current CSV file.
df = pd.read_csv(file_path): Reads the data from the current CSV file into a DataFrame df.
combined_data = combined_data.append(df, ignore_index=True): Appends the data from df to the combined_data DataFrame. The ignore_index=True parameter ensures that the index is reset and continuous in the combined data.
Delete the Original CSV File:

os.remove(file_path): Deletes the original CSV file after its data has been appended to the combined data. This step helps in conserving storage space.
Save the Combined Data:

combined_data.to_csv(combined_file_path, index=False): Writes the combined_data DataFrame to a new CSV file at the specified combined_file_path. The parameter index=False ensures that the DataFrame's index is not written to the CSV.
Example Usage:

The provided paths (folder_path and combined_file_path) specify the location of the individual CSV files and the path for the combined CSV file, respectively.
Calling the combine_csv_files function with these paths will combine all CSV files in the specified folder and save the combined data to the desired location.
'''
pd.read_csv(combined_file_path)