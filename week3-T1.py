#fetch data from URL
import urllib.request
#如果檔案是JSON
import json

url_1 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
url_2 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

try:
    with urllib.request.urlopen(url_1) as response:
        data_1 = response.read()
        #parse JSON from the response
        json_data_1 = json.loads(data_1.decode('utf-8'))
except urllib.error.URLError as e:
    print(f"Failed to fetch data: {e}")    
    json_data_1 = {}

try:
    with urllib.request.urlopen(url_2) as response:
        data_2 = response.read()
        #parse JSON from the response
        json_data_2 = json.loads(data_2.decode('utf-8'))
except urllib.error.URLError as e:
    print(f"Failed to fetch data: {e}")    
    json_data_2 = {}



#裡面的資訊有
#"info":如何到這個景點
#"stitle":關聯字
#"xpostdate":日期
#"longitude":緯度
#"REF_WP":地點編號
#"avBegin":開始日期
#"langinfo"
#"SERIAL_NO":可對應到第二個檔案
#"RowNumber"
#"CAT1":分類>景點
#"CAT2":分類>養生溫泉
#"MEMO_TIME":預約時間
#"POI"
#"filelist":裡面有很多jpg
#"idpt":網站名稱
#"latitude":緯度
#"xbody":正文
#"id":第幾筆資料的編號
#"avEnd":結束日期


import csv

#假設json_data_1 is a list of dictionaries
data_to_write = []
for entry in json_data_1["data"]["results"]:
    seri_no = entry["SERIAL_NO"]
    for entry2 in json_data_2["data"]:
        if entry2["SERIAL_NO"] == seri_no:
            address = entry2["address"]
            #.find(string)是找這個string中最低的index
            start = len("臺北市  ")
            end = address.find("區", start) + 1 #+1是因為要包含"區"
            district = address[start:end]
            #print(district)
            data_to_write.append({
                'stitle': entry['stitle'],
                'district': district,
                'longitude': entry['longitude'],
                'latitude': entry['latitude'],
                'filelist': "https//" + entry['filelist'].split('https://')[1:][0]
            })

mrt_data = []
for entry in json_data_2["data"]:
    seri_no2 = entry["SERIAL_NO"]
    mrt = entry["MRT"]
    key_value = {"MRT":mrt, "SERIAL_NO":seri_no2, "STITLE":[]}
    mrt_data.append(key_value)
    #print(mrt)
#print(mrt_data)

for entry in json_data_1["data"]["results"]:
    spot = entry["stitle"]
    seri_no3 = entry["SERIAL_NO"]
    for mrt in mrt_data:
        if mrt["SERIAL_NO"] == seri_no3:
            mrt["STITLE"].append(spot)
#print(mrt_data)

grouping_spot = []
for data in mrt_data:
    found = False
    for group in grouping_spot:
        if group["MRT"] == data["MRT"]:
            group["STITLE"].extend(data["STITLE"])
            found = True
            break
    if not found:
        #MRT station 還沒在grouping list裡面
        grouping_spot.append({
            "MRT": data["MRT"],
            "STITLE": data["STITLE"]
        }) 
#print(grouping_spot)      


            
#[{'MRT':'北投', 'GROUPING_SPOT':['景點1', '景點2']},{....}]    

#print(data_to_write)
    



#寫入spot.csv
with open('spot.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #可以加更多field names，會顯示在csv檔裡面的第一行
    fieldnames = ['stitle', 'district', 'longitude','latitude', 'filelist']
    #.DictWriter()可以將list of dictionaries轉成csv檔，每個dictionary會是一行row，key順序則是跟著feildnames裡面的順序
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #下面這個.writeheader()功能會保證csv裡面的第一行header是跟著fieldnames
    #writer.writeheader()    

    #preparing the data dictionary from the spot information
    for data in data_to_write:
        writer.writerow(data)

print("Data has been written to spot.csv")


#寫入mrt.csv
with open('mrt.csv', 'w', newline='', encoding='utf-8') as csvfile: 
    writer = csv.writer(csvfile)

    #preparing the data dictionary from the spot information
    for data in grouping_spot:
        writer.writerow([data["MRT"]] + data["STITLE"])

print("Data has been written to mrt.csv")