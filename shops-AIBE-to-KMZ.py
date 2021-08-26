from POIs.functions import pack_attributes

def scrape_Aibe():
    source_url = "https://aibe.lt/parduotuves/"
    from seleniumwire import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(executable_path = ChromeDriverManager().install())
    driver.get(source_url)
    jsonMarkers = driver.execute_script('return jsonMarkers') #get var "jsonMarkers"
    shopList = jsonMarkers[10:] #shops starts with n-th object in the list and continues to end of list

    all_Aibe_shops = [] #list for saving shops

    for i in shopList: 
        all_Aibe_shops.append(
            pack_attributes(
                i[3],
                i[2],
                i[17],
                "not found",
                "on work days: "+i[4]+"-"+i[5]+"; "+ "on Saturday: "+i[6]+"-"+i[7]+"; "+"on Sunday: "+i[8]+"-"+i[9],
                i[0],
                i[1],
                "Aibe.png")
            )
    driver.quit() #close browser
    return all_Aibe_shops
    

result_path = (input("Paste path to folder. Result KML will be saved there: ") or "D:\\TEMP")
print("Selected result folder: " + result_path)
result_path = (result_path + '\\').replace('\\\\','\\')

api_key = (input("Paste Google Maps Geocoding API key: ") or "AIzaSyABVFtB1GXC-ay7UQRFKTWr5o6bhhHxsEE")
print("key " + api_key + " will be used for geocoding")


all_Aibe_shops = scrape_Aibe()

from POIs.functions import geolocate
geolocate(api_key, all_Aibe_shops)

result_filename_prefix = "AIBE_"

import datetime
end_timestamp = str(datetime.datetime.now().strftime("%Y%m%d_%H-%M"))

from POIs.functions import save_as_KMZ
save_as_KMZ(all_Aibe_shops, result_path, result_filename_prefix, end_timestamp)

from POIs.functions import save_as_ZIP
save_as_ZIP(result_path, result_filename_prefix, end_timestamp)

from CLTreport.summary import report_summary
report_summary()

# Below are notes for making EXE package with pyinstaller from PY code.

# cd C:\Users\Ve\Documents\GitHub\shops-AIBE-to-KMZ
# cd C:\Users\Vejas\Documents\GitHub\shops-AIBE-to-KMZ
# pyinstaller ./shops-AIBE-to-KMZ.py --onefile
