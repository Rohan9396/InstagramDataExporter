from selenium import webdriver
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.image as mpimg
import time
import requests
import json
import json

print("hello")

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.maximize_window()
driver.implicitly_wait(30)

def screenCap():
    millis = int(round(time.time() * 1000))
    imgName=millis
    driver.save_screenshot('Screens/'+"test"+str(imgName)+".png")
    img=mpimg.imread('Screens/'+"test"+str(imgName)+".png")
    imgplot = plt.imshow(img)
    plt.show()

def do_Login(username,password):
    driver.get('https://www.instagram.com/accounts/login/')
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_xpath("//*[text()='Log In']").click()
    #screenCap()

def do_ScrapInstagramData(usernameInsta):
    
    instagram_url = 'https://www.instagram.com'
    #profile_url = 'cristiano/'
    #instagram_username = 'itsallaboutjourney'
    instagram_username = usernameInsta
    final_url = instagram_url +'/'+ instagram_username
    json_instagram_url = final_url + '/?__a=1'
    
    
    try:
        r = requests.get(json_instagram_url)
        #json_url = urlopen(json_instagram_url)
        #r = json.loads(json_url.read())
        print(r)
    except Exception as e:
        print(r.status_code)

    if r.status_code == 200:
        #print(r)
        data = r.json()
        graphql = data['graphql']
        user = graphql['user']
        username = user['username']
        business_category_name = user['business_category_name']
        category_enum = user['category_enum']
        business_email = user['business_email']
        edge_followed_by = user['edge_followed_by']
        followed_by_count = edge_followed_by['count']  #Followers count
        edge_follow = user['edge_follow']
        follow_count = edge_follow['count']                #Following count
        edge_owner_to_timeline_media = user['edge_owner_to_timeline_media']
        postsNumber = edge_owner_to_timeline_media['count']  #No. of posts
    # print(username)
    # print(business_category_name)
        #print(business_email)
    # print(category_enum)

        #print(followed_by_count)
        #print(follow_count)
        #print(postsNumber)
        product = {
                'Username': username,
                'Business Category': business_category_name,
                'Business Email': business_email,
                'Category Enum' : category_enum,
                'Followers' : followed_by_count,
                'Following' : follow_count,
                'Posts' : postsNumber,
                'Profile URL' : final_url
            }
        product_list.append(product)

    else:
        print(r.status_code)
    
    
    #print(data)

    

#do_Login("Sample Username","Sample Password")
do_Login("jontyracer","Jonty&2020")
time.sleep(3)

driver.find_element_by_xpath("//*[text()='Not Now']").click()
product_list_new=[]
def searchAndPrint(searchText):
    driver.find_element_by_xpath("//*[@placeholder='Search']").clear()
    driver.find_element_by_xpath("//*[@placeholder='Search']").send_keys(searchText)
    #screenCap()
    time.sleep(3)
    ele=driver.find_element_by_xpath("//*[@class='fuqBx']")
    results=ele.find_elements_by_tag_name("a")
    l=[]
    for i in results:
        #Excluding Hashtags
        if "#" not in i.text:
            l.append(i.text.partition('\n')[0])
#            print(i.text.partition('\n')[0],end=" , ")
            #print(i.text.partition('\n')[0])
            if(' ' in (i.text.partition('\n')[0])):
                print("Space in Word")
            else:
                product_list_new.append(i.text.partition('\n')[0])
            

searchAndPrint("coinbox")
print(product_list_new)

#for pro in product_list_new:
#    print(pro)

# new code
product_list = []

for usernameInsta in product_list_new:
    do_ScrapInstagramData(usernameInsta)
    time.sleep(5)

df = pd.DataFrame(product_list)

df.to_csv('New_demo3.csv')
print('save to file')