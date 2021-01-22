import time
import re
from selenium import webdriver
from tqdm import tqdm

account = '2018213025'
password = 'wozhentmshuai919'

class Crawler_Paper(object):
    def __init__(self):
        print('...准备爬虫...')
    
    def write_to_file(self,content):
        with open('paper_result.txt', 'a', encoding='utf-8') as f:
            f.write(content)

    def crawler_begin(self,browser):
        browser.get("https://www.baidu.com")
        print('...进入百度...')
        ele_input1 = browser.find_element_by_id('kw')
        ele_input1.send_keys('合肥工业大学webvpn')
        print('...搜索合肥工业大学webvpn...')
        ele_srch = browser.find_element_by_id('su')
        sreach_window = browser.current_window_handle
        time.sleep(1)
        ele_srch.click()
        time.sleep(1)
        ele_find_web = browser.find_element_by_xpath("//*[@id='1']/h3/a")
        ele_find_web.click()
        print('...成功打开合肥工业大学webvpn...')
        time.sleep(2)
        n = browser.window_handles # 获取当前页句柄
        browser.switch_to.window (n[1]) # 切换到新的网页窗口
        ele_input_account = browser.find_element_by_xpath("//input[@id='user_name']")
        ele_input_account.send_keys(account)
        print('...输入账号...')
        time.sleep(1)
        ele_input_password = browser.find_element_by_xpath("//input[@name='password']")
        ele_input_password.send_keys(password)
        print('...输入密码...')
        time.sleep(1)
        ele_confirm = browser.find_element_by_xpath("//button[@id='login']")
        ele_confirm.click()
        time.sleep(2)
        print('...成功进入校园vpn...')
        n = browser.window_handles # 获取当前页句柄
        browser.switch_to.window (n[1]) # 切换到新的网页窗口
        #now_handle = browser.current_window_handle #获取当前窗口句柄
        #print(now_handle)   #输出当前获取的窗口句柄
        ele_find_web2 = browser.find_element_by_xpath("//p[@class='vpn-content-block-panel__url']")
        ele_find_web2.click()
        time.sleep(5)
        print('...成功进入中国知网...')
        n = browser.window_handles # 获取当前页句柄
        browser.switch_to.window (n[2]) # 切换到新的网页窗口
        #now_handle = browser.current_window_handle #获取当前窗口句柄
        #print(now_handle)   #输出当前获取的窗口句柄
        search_message = input("...想要搜索什么相关的论文...: ")
        print('...正在搜索 '+ search_message +' 相关的论文...')
        ele_search_paper_input = browser.find_element_by_xpath("//input[@id='txt_SearchText']")
        ele_search_paper_input.send_keys(search_message)
        #ele_search_paper_input.send_keys('深度学习')
        time.sleep(2)
        ele_search_paper_confirm = browser.find_element_by_xpath("//input[@type='button']")
        ele_search_paper_confirm.click()
        # time.sleep(5)
        print('...搜索成功...')
        time.sleep(5)
        ele_search_total_num = browser.find_element_by_xpath("//span[@class='pagerTitleCell']/em")
        print("...共找到" + ele_search_total_num.text + "条结果...\n...显示前100条结果...")
        total_num_text = browser.find_element_by_xpath("//span[@class='total']").text
        total_num = re.sub("\D","",total_num_text)
        # print(total_num)
        # print(type(total_num))
        total_num = int(total_num)
        # print(total_num)
        # print(type(total_num))
        print("...搜索的论文结果如下...")
        for i in tqdm(range(5)):
            time.sleep(0.5)
            eles = browser.find_elements_by_xpath("//table[@class='result-table-list']/tbody/tr")
            for ele in eles:
                ele_seq = ele.find_element_by_class_name('seq')
                self.write_to_file(ele_seq.text + '\t')
                print(ele_seq.text + '\t')
                ele_name = ele.find_element_by_class_name('fz14')
                self.write_to_file(ele_name.text + '\t')
                print(ele_name.text + '\t')
                ele_author = ele.find_element_by_class_name('author')
                self.write_to_file(ele_author.text + '\t')
                print(ele_author.text + '\t')
                ele_source = ele.find_element_by_class_name('source')
                self.write_to_file(ele_source.text + '\t')
                print(ele_source.text + '\t')
                ele_date = ele.find_element_by_class_name('date')
                self.write_to_file(ele_date.text + '\t')
                print(ele_date.text + '\t')
                ele_html_reader = ele.find_element_by_xpath("//a[@title='HTML阅读']")
                self.write_to_file(ele_html_reader.get_attribute("href")+ '\n')
                print(ele_html_reader.get_attribute("href") + '\t')
            #print("...下一页...")
            self.write_to_file('\n')
            time.sleep(1)
            ele_nextpage = browser.find_element_by_link_text("下一页")
            ele_nextpage.click()
            time.sleep(5)
        print("论文结果写入完成")
        browser.quit()

    def main(self):
        # chrome_options = webdriver.ChromeOptions()  # 获取 ChromeOptions 对象
        # chrome_options.add_argument('--headless')  # 添加 headless 参数
        # browser = webdriver.Chrome(chrome_options=chrome_options)  # 初始化 Chrome 对象
        browser = webdriver.Chrome()
        browser.maximize_window()
        self.crawler_begin(browser) 

if __name__ == '__main__':
    crawler_Paper = Crawler_Paper()
    crawler_Paper.main()
