import urllib.request as req

only_title=[]
href_topic = []
publish_time = []
only_like_dislike = []

#拿出時間PublishTime的function
def getDate(URLs):

    for URL in URLs:
        request2 = req.Request(URL, headers={
            "cookie":"over18=1", #模仿cookie
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        })

        with req.urlopen(request2) as response:
            data2=response.read().decode("utf-8")

        import bs4 #這段碼在replit裡面不一樣
        #root代表整份網頁，data裡面是剛剛抓到的原始碼
        root2 = bs4.BeautifulSoup(data2, "html.parser") #這段碼在replit裡面不一樣
        #print(root2.title.string)

        article_metaline = root2.find_all("div", class_="article-metaline")
        #print(article_metaline)
        #publish_time = []在function外面
        if article_metaline:
            for div in article_metaline:
                article_meta_tag = div.find("span", class_="article-meta-tag")
                article_meta_value = div.find("span", class_="article-meta-value")
                if article_meta_tag.string == "時間":
                    if article_meta_value:
                        publish_time.append(article_meta_value.string)
                    else:
                        publish_time.append("")
        else:
            publish_time.append("")

    #print(publish_time)
    return publish_time





#抓文章標題、讚/噓總數 + getDate() function要用的網址list
def getData(url):
    request = req.Request(url, headers={
        "cookie":"over18=1", #模仿cookie
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    #print(data) #------檢視整份網頁原始碼

    import bs4 #這段碼在replit.com裡面不一樣
    #root代表整份網頁，data裡面是剛剛抓到的原始碼
    root = bs4.BeautifulSoup(data, "html.parser") #這段碼在replit.com裡面不一樣
    print(root.title.string) #--->網頁最上方的標題

    titles=root.find_all("div",class_="title") #--->有全部標題的list
    #only_title=[] 放到function外面去
    #有一些有a，有一些沒有a(已經被刪除的文章)
    for title in titles:        
        #如果標題有a標籤，就印出來
        if title.a != None:
            only_title.append(title.a.string)
            print(title.a.string) #--->每個文章的標題
    #print(only_title) #--->印出沒有<div><a href>的標題list

    #only_like_dislike = []在function外面
    #尋找推和噓的總和
    total_like_dislike = root.find_all("div", class_="r-ent")
    if total_like_dislike:
        for div in total_like_dislike:
            nrec = div.find("div", class_="nrec")
            exist_title = div.find("div", class_="title")
            if exist_title.a != None:
                if nrec.span != None:
                    only_like_dislike.append(nrec.span.string)
                else:
                    only_like_dislike.append("0")
        #print(only_like_dislike)


    #做一個href_topic = []，這個list包含所有文章的href
    #href_topic = []在function外面
    click_in_topic = root.find_all("div", class_="title")
    for div in click_in_topic:
        a_tag = div.find("a")
        if a_tag != None:
            href_topic.append("https://www.ptt.cc"+a_tag["href"])
            #print(a_tag["href"]) #--->檢查每個文章標題的href
    #print(href_topic)  #---->這個list裡面有所有文章標題的href
    #return href_topic
    
    #找到內文是"‹ 上頁"的a標籤(在a裡面，根據string裡的文字尋找)
    nextLink = root.find("a", string="‹ 上頁")
    return nextLink["href"]
    

#抓取一個頁面的標題
pageURL="https://www.ptt.cc/bbs/Lottery/index.html"

count=0
while count<3:
    pageURL = "https://www.ptt.cc" + getData(pageURL)    
    count+=1
getDate(href_topic)


#檢查各種資料的list
#print(only_title)
#print(href_topic)
#print(publish_time)
#print(only_like_dislike)


#最後寫入csv
import csv

combined = list(zip(only_title, only_like_dislike, publish_time))
num = len(combined)
#print(num)

with open("article.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    #將連在一起的list，分開寫入csv，變成一行一行
    for i in range(0, num):
        writer.writerow(combined[i])