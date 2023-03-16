import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


# 登入fb
url = "https://www.facebook.com/"
email = "lin034506618@gmail.com"
password = "a0937130711"


# 防止跳出通知
chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_setting_values.notifications": 2
}
chrome_options.add_experimental_option("prefs", prefs)


# 開啟下載的chromedriver
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)



# 最大化視窗
driver.maximize_window()
# 進入Facebook登入畫面
driver.get(url)


# 填入帳號密碼，並送出

driver.find_element(By.ID, "email").send_keys(email)
driver.find_element(By.ID, "pass").send_keys(password)
driver.find_element(By.NAME, "login").click()


time.sleep(5)

# 進到NBA粉專
driver.get("https://www.facebook.com/nba")
# driver.get("https://www.facebook.com/emuse.com.tw")
soup = BeautifulSoup(driver.page_source, 'html.parser')



# 往下滑3次，讓Facebook載入文章內容
# for x in range(3):
#     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#     print("scroll")
#     time.sleep(5)


# 定位文章標題
titles = soup.find_all("div", class_="x78zum5 xdt5ytf xz62fqu x16ldp7u")
print(titles)
# for title in titles:
#     # 定位每一行標題
#     posts = title.find_all("div", dir="auto")
#     # 如果有文章標題才印出
#     if len(posts):
#         for post in posts:
#             print(post.text)

#     print("-" * 30)



# 等待10秒
time.sleep(5)
# 關閉瀏覽器
driver.quit()

# payload = {
#     'from': '/bbs/Gossiping/index.html',
#     'yes': 'yes'
# }
# rs = requests.session()
# response = rs.post("https://www.ptt.cc/ask/over18", data=payload) 
# response = rs.get("https://www.ptt.cc/bbs/Gossiping/index.html") 
# root = BeautifulSoup(response.text, "html.parser")
# links = root.find_all("div", class_="title") 

# # print(response.text)
# # print(response.status_code)
# for link in links:
#     # print(link.text.strip()) # strip()用來刪除文字前面和後面多餘的空白
#     page_url = "https://www.ptt.cc"+link.a["href"]
#     print(page_url)






# # 讀檔
# response = ""
# with open("crawl_me.html", "r", encoding="utf8") as file:
#     response = file.read()

# # BeautifulSoup解析原始碼
# soup = BeautifulSoup(response, "html.parser")
# print(soup.prettify())

# h1 = soup.find("h1")
# print(h1)

# container = soup.find("div", class_="container")
# print(container)


# h2s = soup.find_all("h2")
# print(h2s)
# print(h2s[1])   # 使用索引值