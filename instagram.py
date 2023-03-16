from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as Soup
import time
import pygsheets

auth_file = "/Users/yee0526/Downloads/independent-tea-380808-b77f919a733d.json"

# 開啟google sheet
gc = pygsheets.authorize(service_file=auth_file)

print("-------")
survey_url = 'https://docs.google.com/spreadsheets/d/15VD1d7BAv108XFwO1_o80ZNE6JT1tCNLTILBn_ye7xE/edit#gid=0'

sh = gc.open_by_url(survey_url)
ws = sh.worksheet_by_title('工作表1')

ws.update_value("E1", "IG爬蟲")
print("-------")

  

# 登入ig - 這邊要輸入自己的IG帳號、密碼
url = "https://www.instagram.com/accounts/login"
email = ""
password = ""

# browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
url = 'https://www.instagram.com/'  


# 防止跳出通知
chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_setting_values.notifications": 2
}
chrome_options.add_experimental_option("prefs", prefs)

# ------ 前往該網址 ------
browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
browser.get(url) 


# 最大化視窗
browser.maximize_window()

WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))



username_input = browser.find_element(By.NAME, 'username')
password_input = browser.find_element(By.NAME, 'password')
print("inputing username and password...")


username_input.send_keys(email)
password_input.send_keys(password)


# ------ 登入 ------
login_click = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))

# ------ 網頁元素定位 ------
# login_click = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]')

# ------ 點擊登入鍵 ------
login_click.click()

# ------ 等畫面登入 ------
time.sleep(10)



nba_url = "https://www.instagram.com/nba/"
browser.get(nba_url) 

time.sleep(10)



# 取得短連結
n_scroll = 1
post_url = []
for i in range(n_scroll):
    scroll = 'window.scrollTo(0, document.body.scrollHeight);'
    browser.execute_script(scroll)
    html = browser.page_source
    soup = Soup(html, 'lxml')

    # 尋找所有的貼文連結
    for elem in soup.select('article div div div div a'):
        # 如果新獲得的貼文連結不在列表裡，則加入
        if elem['href'] not in post_url:
            post_url.append(elem['href'])
    time.sleep(2) # 等待網頁加載

# 總共加載的貼文連結數
print("總共取得 " + str(len(post_url)) + " 篇貼文連結")
print(post_url)



# 找到對應的貼文，滑鼠移上去
post_url = post_url[5]
post_elem = browser.find_element(By.XPATH, '//a[@href="'+str(post_url)+'"]') 
action = ActionChains(browser)
action.move_to_element(post_elem).perform()



# 找到網頁元素
n_like_elem = browser.find_elements(By.CLASS_NAME, '_abpm')
print(n_like_elem)

print("----------------")

n_like = n_like_elem[0].text
print("喜歡數 : " + str(n_like))
ws.update_value("E3", n_like)


n_comment = n_like_elem[1].text
print("留言數 : " + str(n_comment))
ws.update_value("E4", n_comment)

print("----------------")

time.sleep(5)

# 進到內文 - 取得內文、日期、回覆內容
single_post_url = "https://www.instagram.com"+post_url

ws.update_value("E2", single_post_url)
print(single_post_url)
browser.get(single_post_url) 

time.sleep(5)

# 內文(這陣列裡面有標題、所有留言)
post_content = browser.find_elements(By.CLASS_NAME, '_a9zs')

# 標題
post_title = post_content[0].text
print(post_title)

ws.update_value("E5", post_title)
print("----------------")

# 第一則留言
# first_comment = post_content[1].text
# print(first_comment)

# 第一筆~第十筆
for i in range(1, 11):
    print(str(i)+":"+post_content[i].text)
    ws.update_value("E"+str(i+5), str(i)+":"+post_content[i].text)
    

print("----------------")

# 時間
time_ele = browser.find_elements(By.CLASS_NAME, '_aaqe')
datetime_str = time_ele[0].get_attribute('datetime')
datetime_format = datetime_str[:10]
print(datetime_format)

ws.update_value("E16", datetime_format)




# 使用方法
# (1) 108行，可以修改指定的單篇貼文
# (2) 搜尋update_value，按下 command + D ，批量修改
# 之後寫成方法就可以簡單使用