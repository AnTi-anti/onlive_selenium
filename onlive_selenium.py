# coding: utf-8
from json import loads
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
warnings.filterwarnings('ignore')
import wmi
w = wmi.WMI()
import time

class Concert(object):

    def __init__(self, date, session, ticket_type, ticket_num, target_url, driver_path, buy_time, wait_time, phone):
        self.date = date
        self.session = session
        self.ticket_type = ticket_type
        self.ticket_num = ticket_num
        self.target_url = target_url  # 目标购票网址
        self.driver_path = driver_path  # 浏览器驱动地址
        # self.driver = webdriver.Chrome(driver_path)
        self.num = 0  # 尝试次数
        self.status = 0  # 状态标记
        self.time_start = 0  # 开始时间
        self.time_end = 0  # 结束时间
        self.driver = None
        self.buy_time = time.mktime(time.strptime(buy_time, "%Y %m %d %H %M %S"))
        self.wait_time = wait_time
        self.phone = phone

    def login(self):
        self.driver.get(self.target_url)
        WebDriverWait(self.driver, 10, 0.1).until(EC.title_contains('演出详情'))
        print(u'###进入到抢票地址初始页面成功###')
        # self.set_cookie()

    def enter_concert(self):
        print(u'###打开浏览器，准备进入正在现场###')
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver.get("https://m.zhengzai.tv/#/user")  # 正在现场登录账号页面
        # while self.driver.title == '演出首页':
        WebDriverWait(self.driver, 1000).until(EC.title_is('演出首页'))
        print("进入到演出首页")
        time.sleep(1)
        self.driver.get(self.target_url)


    # 判断元素是否存在
    def isElementExist(self, element, driver):
        flag = True
        browser = driver
        try:
            browser.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag

        # 实现抢票日期选择函数
    def choose_date(self):
        print(u"###进入抢票界面###")

        while self.driver.title.find('选择票种') == -1:  # 如果跳转到了确认界面就算这步成功了，否则继续执行此步
            self.num += 1  # 尝试次数加1

            # 确认页面刷新成功
            try:
                print(self.driver.current_url)
                time.sleep(1)
                box = WebDriverWait(self.driver, 1, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ticket-detail-body')))
                box_buy = WebDriverWait(self.driver, 1, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ticket-detail-footer ')))

            except:
                raise Exception(u"***Error: 页面刷新出错***")

            # 日期进行选择
            try:
                selects = box.find_elements_by_class_name('van-tabs__nav')
                if selects:
                    for item in selects:
                        date = item
                    if WebDriverWait(date, 1, 0.1).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'van-tab'))):
                        data_list = date.find_elements_by_class_name('van-tab')  # 选定日期
                        print('可选日期数量为：{}'.format(len(data_list)))
                        for i in self.date:  # 根据优先级选择一个可行日期
                            j = data_list[i - 1]
                            j.click()  # 选定好日期点击按钮确定
                            # break
                else:
                    print("不需要对日期进行选择(只有一种情况)")
            except:
                raise Exception(u"***Error: 选择日期不成功***")

            # 寻找购买标签
            try:
                buybutton = box_buy.find_element_by_class_name('footer-buy-btn')
                buybutton_text = buybutton.text
            except:
                raise Exception(u"***Error: 【购买】 标签元素找不到***")

            if buybutton_text == "购买" or buybutton_text == "售罄":
                buybutton.click()
                self.status = 4


    def choose_session_type(self):
        print(u"###进入选择票种界面###")

        while self.driver.title.find('购买详情') == -1:  # 如果跳转到了购买详情就算这步成功了，否则继续执行此步
            self.num += 1  # 尝试次数加1

            # 确认页面刷新成功
            try:
                print(self.driver.current_url)
                time.sleep(1)
                box = WebDriverWait(self.driver, 1, 0.1).until(EC.presence_of_element_located((By.CLASS_NAME, 'ticket-purchase-content')))
            except:
                raise Exception(u"***Error: 选择票种页面刷新出错***")

            # 选择场次
            try:
                selects_session = box.find_elements_by_class_name('van-tabs__nav')
                for item in selects_session:
                    session = item

                if WebDriverWait(session, 1, 0.1).until(EC.presence_of_element_located((By.CLASS_NAME, 'van-tab'))):
                    session_list = session.find_elements_by_class_name('van-tab')  # 选定场次
                    print('可选场次数量为：{}'.format(len(session_list)))
                    for i in self.session:  # 根据优先级选择一个可行场次
                        j = session_list[i - 1]
                        j.click()  # 选定好场次点击按钮确定
                        #break
            except:
                raise Exception(u"***Error: 选择场次不成功***")

            # 选择票种
            try:
                selects_type = box.find_elements_by_class_name('ticket-types-content')
                for item in selects_type:
                    type_ticket = item

                if WebDriverWait(type_ticket, 1, 0.1).until(EC.presence_of_element_located((By.CLASS_NAME, 'ticket-type'))):
                    type_list = type_ticket.find_elements_by_class_name('ticket-type')  # 选定票种
                    print('可选票种数量为：{}'.format(len(type_list)))
                    for i in self.ticket_type:  # 根据优先级选择一个可行票种
                        j = type_list[i - 1]
                        j.click()  # 选定好票种点击按钮确定
                        break
            except:
                raise Exception(u"***Error: 选择票种不成功***")

            # 选择票数
            try:
                ticket_num_up = box.find_element_by_class_name('goods-amount-more')
            except:
                raise Exception(u"***Error: 选择票数元素 位置找不到***")

            # 结算标签
            box_settle = WebDriverWait(self.driver, 1, 0.1).until(EC.presence_of_element_located((By.CLASS_NAME, 'purchase-next-btn'))) #结算按钮
            try:
                settlebutton = box_settle.find_element_by_class_name('pay-btn')
                seeelebutton_text = settlebutton.text
            except:
                raise Exception(u"***Error: 结算 标签元素找不到***")

            if seeelebutton_text == "未开售":
                while True:
                    try:
                        if (self.buy_time - time.time() < float(self.wait_time)):
                            self.status = 2
                            self.driver.refresh()
                            time.sleep(2)
                            print(u"---尚未开售，刷新等待---")
                            break
                    except:
                        continue

            if "开售倒计时" in seeelebutton_text:
                while True:
                    try:
                        if (self.buy_time - time.time() < float(self.wait_time)):
                            self.status == 2
                            self.driver.refresh()
                            time.sleep(2)
                            print(u"---开售倒计时，刷新等待---")
                            break
                    except:
                        continue

            if seeelebutton_text == "缺货登记":
                while True:
                    try:
                        if (self.buy_time - time.time() < float(self.wait_time)):
                            self.status = 2
                            self.driver.refresh()
                            time.sleep(2)
                            print(u"---缺货登记，刷新等待---")
                            break
                    except:
                        continue

            if seeelebutton_text == "售罄":
                while True:
                    try:
                        if (self.buy_time - time.time() < float(self.wait_time)):
                            self.status = 2
                            self.driver.refresh()
                            time.sleep(2)
                            print(u"---售罄，刷新等待---")
                            break
                    except:
                        continue

            if seeelebutton_text == "结算":
                while True:
                    try:
                        if (self.buy_time - time.time() < float(self.wait_time)):
                            self.status = 4
                            print("抢购票数为:{}".format(self.ticket_num))
                            for i in range(self.ticket_num - 1):  # 设置增加票数
                                ticket_num_up.click()
                            settlebutton.click()
                            # 解决确定制遮罩
                            try:
                                mask = WebDriverWait(self.driver, 1, 0.1).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, 'bried-next-btn')))
                                mask.click()
                                break
                            except:
                                print(u"***Error: 确定遮罩关闭失败***")
                                self.driver.refresh()
                    except:
                        continue

    def check_order(self):

        print(u"###进入待付款页面，准备提交订单###")
        while self.driver.title.find('支付宝') == -1:  # 如果跳转到了支付宝页面就算这步成功了，否则继续执行此步
            self.num += 1  # 尝试次数加1

            try:
                box = WebDriverWait(self.driver, 1, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ticket-purchase-detail')))
            except:
                raise Exception(u"***Error：购买详情页面元素获取失败***")

            print(u'###开始确认订单###')

            try:
                if WebDriverWait(box, 1, 0.1).until(EC.presence_of_element_located((By.CLASS_NAME, 'pay-able'))):
                    pay_able = box.find_element_by_class_name('pay-able')
                    pay_able.click()
            except:
                print(u"***Error：立即支付元素变灰 不断点击捡漏***")
                box.find_element_by_class_name('pay-dis').click()
                # self.driver.refresh()
                continue

            # 点击同意协议
            try:
                if WebDriverWait(self.driver, 1, 0.1).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'mask_pay_btn'))):
                    pay_dot = WebDriverWait(self.driver, 1, 0.1).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'mask_pay_btn')))
                    pay_dot.click()
            except:
                print(u"***Error: 同意协议 获取失败 ***")
                self.driver.refresh()

            print("本次抢票时间：", time.time() - self.time_start)

            # 判断title是不是支付宝
            print(u"###等待跳转到--付款界面--###")
            try:
                WebDriverWait(self.driver, 1, 0.1).until(EC.title_contains('支付宝'))
            except:
                print(u'***Error: 跳转不到付款界面***')
                self.driver.refresh()
                # break

            self.status = 6
            print(u'###成功提交订单,请在5分钟内手动支付###')
            self.time_end = time.time()

def main():
    try:
        with open('./config.json', 'r', encoding='utf-8') as f:
            config = loads(f.read())
            con = Concert(config['date'], config["session"], config["ticket_type"], config["ticket_num"],
                          config['target_url'], config['driver_path'], config['buy_time'], config['wait_time'],
                          config['phone'])
            con.enter_concert()
            time.sleep(1)
    except Exception as e:
        print(e)

    while True:
        try:
            con.choose_date()
            con.choose_session_type()
            con.check_order()
        except Exception as e:
            print(e)
            continue

        if con.status == 6:
            while True:
                print(u"###经过%d轮奋斗，共耗时%.1f秒，抢票成功！请确认订单信息###" % (con.num, round(con.time_end - con.time_start, 3)))

if __name__ == '__main__':
    main()