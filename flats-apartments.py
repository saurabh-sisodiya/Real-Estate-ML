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
    print('''
Your IP might have blocked. Delete Runtime and reconnect again with updating start page number. \n
          You would see in output above like 1 -> 15\ and so 1 is page nuber and 15 is data items extracted.''')
    csv_file_path = f"/Users/saurabhsisodiya/Downloads/RealEstateMLProject/Data/chandigarh/Flats/flats_{City}_data-page-{start}-{pageNumber-1}.csv"
    
    # This file will be new every time if start page will change, but still taking here mode as append
    if os.path.isfile(csv_file_path):
        # Append DataFrame to the existing file without header
        flats.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        # Write DataFrame to the file with header - first time write
        flats.to_csv(csv_file_path, mode='a', header=True, index=False)
         
            
            
            
            
            
            
            
             
            