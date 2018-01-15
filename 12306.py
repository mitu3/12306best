from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import time
from nonstop import run


USERNAME = '24983649@qq.com'
PASSWORD = 'chu'
value_fromstation = '%u5317%u4EAC%2CBJP'  # 始发站（深圳北）  在浏览器先搜索  然后查看cookies  字段  _jc_save_fromStation
value_tostation = '%u5929%u6D25%2CTJP'    # 终点站（云浮东）    在浏览器先搜索  然后查看cookies  字段  _jc_save_toStation
value_date = '2018-01-11'                 # 出发时间
train_type = 'K'                          #车次类型
timer = 0       #    定时抢票 1     不定时  0
hourer = 11     #    时间
miner = 59      #    分钟

def login_proc(username, password):
    # 打开登录页面
    sel = webdriver.Chrome()
    sel.maximize_window()
    # sel=webdriver.Firefox('C:\\Users\chufusheng\Desktop')
    sel.implicitly_wait(30)
    login_url = 'https://kyfw.12306.cn/otn/login/init'
    sel.get(login_url)
    # sign in the username
    try:
        user_input = sel.find_element_by_id("username")
        user_input.clear()
        user_input.send_keys(username)
        print ('user-id write success!')
    except:
        print ('user-id write error!')
    # sign in the pasword
    try:
        pwd_input = sel.find_element_by_id("password")
        pwd_input.clear()
        pwd_input.send_keys(password)
        print ('pw write success!')
    except:
        print ('pw write error!')

    # Check for Login success

    while True:
        curpage_url = sel.current_url
        if curpage_url != login_url:
            if curpage_url[:-1] != login_url:  # choose wrong verify_pic
                print ('Login finished!')

                break
        else:
            time.sleep(5)
            print (u'------------>等待用户图片验证')
    return sel
#
def search_proc(sel):

    # 打开订票网页
    book_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    sel.get(book_url)
    # 始发站
    sel.add_cookie({"name": "_jc_save_fromStation", "value": value_fromstation})
    # 终点站
    sel.add_cookie({"name": "_jc_save_toStation", "value": value_tostation})
    # 出发日期
    sel.add_cookie({"name": "_jc_save_fromDate", "value": value_date})

    sel.refresh()

    time.sleep(1)

    train_type_dict = {'T': '//input[@name="cc_type" and @value="T"]',
                       'K': '//input[@name="cc_type" and @value="K"]',# 特快
                       'G': '//input[@name="cc_type" and @value="G"]',  # 高铁
                       'D': '//input[@name="cc_type" and @value="D"]',  # 动车
                       'Z': '//input[@name="cc_type" and @value="Z"]'}  # 直达
    # 车次类型选择
    global train_type
    if train_type == 'T' or train_type == 'G' or train_type == 'D' or train_type == 'Z' or train_type == 'K':
        sel.find_element_by_xpath(train_type_dict[train_type]).click()
    else:
        print (u"车次类型异常或未选择!(train_type=%s)" % train_type)

    # Keys.F5
    sel.find_element_by_id('query_ticket').click()




def book_proc(sel, result):


    search_btn = WebDriverWait(sel, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ticket_{}"]/td[13]/a'.format(result))))
    try:
        search_btn.click()
    except:
        search_btn.send_keys(Keys.ENTER)

    cust_sel_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    while True:
        if (sel.current_url == cust_sel_url):
            print (u'页面跳转成功!')
            break
        else:
            print (u'等待页面跳转...')

    try:
        global USERNAME, PASSWORD
        sel.find_element_by_id("username").send_keys(USERNAME)
        sel.find_element_by_id("password").click()
        sel.find_element_by_id("password").clear()
        sel.find_element_by_id("password").send_keys(PASSWORD)

        time.sleep(3)
    except:
        print('搜索不到输入框')


    time.sleep(1)
    try :
        sel.find_element_by_id("normalPassenger_0").click()
        sel.find_element_by_id("submitOrder_id").click()
        time.sleep(1)

        sel.find_element_by_id("back_edit_id").click()    #   返回
        # sel.find_element_by_id("qr_submit_id").click()    #   提交

    except:
        print('选择失败')







if __name__ == '__main__':
    # # 变量定义
    # leave_date = '2016-12-23'
    # train_type = 'K'
    # refresh_interval = 0.1
    # timer = False
    resultt = ''
    sel = login_proc(USERNAME, PASSWORD)
    # search_proc(sel, train_type, timer)
    search_proc(sel)
    if timer == 1:
        while True:
            current_time = time.localtime()
            print(current_time)
            if ((current_time.tm_hour == hourer) and (current_time.tm_min >= miner) and (
                        current_time.tm_sec >= 00)):
                print (u'开始刷票...')
                break
            else:
                time.sleep(5)
                if current_time.tm_sec % 30 == 0:
                    print (time.strftime('%H:%M:%S', current_time))
    while True:
        result = run()
        print(result)
        if result == 0:
            # sel.find_element_by_id('query_ticket').click()
            waitB = WebDriverWait(sel, 10 ,poll_frequency=1, ignored_exceptions=None).until(EC.presence_of_element_located((By.XPATH, '//*[@id="query_ticket"]')))
            # sel.switch_to_window(sel.window_handles[1])
            sreach_window = sel.current_window_handle
            # waitB.click()
            waitB.send_keys(Keys.ENTER)
            time.sleep(0.5)
            print('......')
        else:
            resultt = result
            try:
                sel.find_element_by_xpath('//*[@id="ticket_{}"]/td[13]/a'.format(result))
                break
            except:
                print('...')



    book_proc(sel, result)