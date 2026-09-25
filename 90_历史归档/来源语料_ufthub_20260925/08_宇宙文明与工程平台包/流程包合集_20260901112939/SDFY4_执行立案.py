#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简模版 - 优化版
作者：YMKJ团队
版本：2.5
更新时间：2025-10-22

最简化的RPA开发模版，完全使用aibot_common的浏览器操作组件
"""

import sys
from pathlib import Path

from aibot_common.getdata_rpa import GETDATA_RPA
from selenium.webdriver.support.wait import WebDriverWait

# from setuptools.sandbox import save_path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from aibot_rpa.utils.logger import LoggerInit
from aibot_rpa.core.flow import BaseFlow
from aibot_rpa.utils.decorators import get_retry_count
from aibot_common.browser_rpa import BROWSER_RPA
from aibot_common.mouse_rpa import MOUSE_RPA
from aibot_common.page_rpa import PAGE_RPA
from aibot_common.button_rpa import BUTTON_RPA
from aibot_common.other_rpa import OTHER_RPA
from aibot_common.excel_rpa import EXCEL_RPA
import logging

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    NoSuchElementException
)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback
from selenium.webdriver.common.by import By
import random
import time
import shutil
import sys
import re
import os
import time

# ================================ 全维度反爬机制破解方案（Python/Selenium 实战版） ================================
# 反爬对抗的核心逻辑是：**消除自动化特征 + 模拟真人行为 + 合规化请求策略**。以下从「基础特征隐藏→行为模拟→请求层对抗→验证码突破→高级反爬破解」全维度拆解，所有方案均附可落地的代码实现。

# 核心反爬类型与对抗思路
'''
| 反爬类型                | 检测手段                          | 核心对抗策略                          |
|-------------------------|-----------------------------------|---------------------------------------|
| 自动化特征检测          | 检测 `webdriver`、浏览器指纹      | 隐藏自动化标识、伪造浏览器指纹        |
| 行为特征检测            | 固定点击间隔、无随机操作、极速滑动 | 随机化行为、模拟真人操作轨迹          |
| 请求层反爬              | UA/Referer 校验、IP 封禁、Cookie 校验 | 动态请求头、IP 代理池、Cookie 持久化  |
| 验证码                  | 滑块、点选、图文、短信验证        | 自动化识别/第三方打码/模拟真人交互    |
| 动态页面/数据加密       | JS 加密参数、异步加载、DOM 动态渲染 | 逆向 JS、Hook 加密函数、等待渲染完成  |
| 高级反爬（指纹/设备锁） | Canvas 指纹、WebGL 指纹、设备验证  | 统一指纹、模拟真实设备环境            |
'''

# 构建请求头池
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/121.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile/15E148 Safari/604.1"
]

REFERER_POOL = [
    "https://www.baidu.com/",
    "https://www.google.com/",
    "https://example.com/",
    ""  # 空Referer（部分场景）
]


def get_random_headers():
    """获取随机请求头"""
    return {
        "User-Agent": random.choice(UA_POOL),
        "Referer": random.choice(REFERER_POOL),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }


def random_sleep(min_time=0.5, max_time=3.0):
    """随机等待（模拟真人思考/操作间隔）"""
    time.sleep(random.uniform(min_time, max_time))


def human_input(elem, text):
    """模拟真人输入（逐字输入，随机间隔）"""
    elem.click()
    for char in text:
        elem.send_keys(char)
        random_sleep(0.05, 0.2)  # 每个字符间隔0.05-0.2秒


def human_scroll(driver, direction='down', distance=500):
    """模拟真人滚动页面（随机距离+速度）"""
    scroll_script = f"window.scrollBy(0, {distance if direction=='down' else -distance})"
    driver.execute_script(scroll_script)
    random_sleep(0.3, 1.0)


def init_chrome_driver():
    """初始化无特征的Chrome驱动"""
    chrome_options = Options()
    
    # 1. 基础参数（隐藏自动化标识）
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 关闭自动化提示
    chrome_options.add_experimental_option('useAutomationExtension', False)  # 禁用自动化扩展
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 核心：禁用webdriver检测
    
    # 2. 模拟正常浏览器参数
    chrome_options.add_argument('--no-sandbox')  # 取消沙盒模式
    chrome_options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速（避免部分环境报错）
    chrome_options.add_argument('--start-maximized')  # 最大化窗口（模拟真人）
    chrome_options.add_argument('--disable-extensions')  # 禁用扩展
    chrome_options.add_argument('--disable-popup-blocking')  # 禁用弹窗拦截
    
    # 3. 随机化UA
    chrome_options.add_argument(f'user-agent={random.choice(UA_POOL)}')
    
    # 初始化驱动
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # 4. 覆盖navigator.webdriver（关键）
    driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    
    return driver


try:
    import undetected_chromedriver as uc
    
    def init_undetected_driver():
        """初始化无指纹的Chrome驱动（对抗高级检测）"""
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        # 可选：添加代理
        # chrome_options.add_argument('--proxy-server=http://127.0.0.1:7890')
        
        # 初始化（自动规避检测）
        driver = uc.Chrome(options=chrome_options)
        return driver
except ImportError:
    # 如果未安装undetected-chromedriver，则使用普通驱动
    pass

# ================================ 全局变量初始化 ================================
g_log = LoggerInit.init(__name__)


class MinimalRPAFlow(BaseFlow):
    """极简RPA流程类 - 使用aibot_common"""

    def __init__(self, config_manager=None, **kwargs):
        super().__init__(config_manager=config_manager, **kwargs)
        # 使用预导入的BROWSER_RPA实例
        self.browser_rpa = BROWSER_RPA
        self.button_rpa = BUTTON_RPA
        self.page_rpa = PAGE_RPA
        self.mouse_rpa = MOUSE_RPA
        self.config_manager = config_manager
        self.other_rpa = OTHER_RPA
        self.get_data_rpa = GETDATA_RPA
        self.excel_rpa = EXCEL_RPA
        self.g_dict = {}

    def start_data(self, table_id, auth_code):  # 初始化异常数据
        print("--------------数据初始化")
        payload = {
            "uniId": table_id,
            "pageSize": 1,
            "reqParam": {
                "queryParam": [
                    {
                        "field": "zt",
                        "value": [
                            "处理中"
                        ],
                        "sign": "=",
                        "append": "or"
                    }, {
                        "field": "zt",
                        "value": [
                            "异常"
                        ],
                        "sign": "=",
                        "append": "or"
                    }
                ],
                "updateMap": {
                    "zt": "",

                }
            }
        }
        while True:
            rqs_data = self.other_rpa.post_request(
                url="http://146.24.58.227:88/ymkj-api/uni/universal/pull",
                payload=payload,
                auth_token=f'AuthCode {auth_code}')
            data = rqs_data['data']['list']
            if len(data) == 0:  # 判断是否还有数据需要操作
                break

    def csh(self):
        try:
            # 使用配置字典 读取参数
            config_dict = self.config_manager.get_dict_config()
            self.g_dict["config_dict"] = config_dict
            self.g_dict["auth_code"] = config_dict["AuthCode"]
            print(self.g_dict["auth_code"])
            self.g_dict["table_id"] = config_dict["uniTable"][0][0]
            print(self.g_dict["table_id"])
            self.g_dict["laspr"] = config_dict["laSpr"]
            self.g_dict["login_acc"] = str(config_dict["loginAcc"])
            if config_dict["isPW"]:
                self.g_dict["login_pw"] = "0" + str(config_dict["loginPW"])
            else:
                self.g_dict["login_pw"] = str(config_dict["loginPW"])
            # self.start_data(self.g_dict["table_id"], self.g_dict["auth_code"]) # 初始化异常数据

            # self.g_dict["new_data"] = self.g_dict["start_time"] + "至" + self.g_dict["end_time"]
            # self.g_dict["save_path"] = self.g_dict["保存路径"] + r"/执行立案_" + self.g_dict["new_data"] + ".xlsx"
            ls_id = random.randint(1, 1000000)
            ls_id = str(ls_id)
            self.g_dict["ls_dir"] = "D:/临时下载/" + ls_id
            if not os.path.isdir(self.g_dict["ls_dir"]):
                os.makedirs(self.g_dict["ls_dir"])
        except Exception as e:
            self.g_dict["err"] = True
            logging.info(e)
            traceback.print_exc()

    def yw_csh(self):
        try:
            # 打开浏览器 - set driver first
            # 打开系统网址

            # 构建反爬浏览器参数
            anti_crawl_args = "--disable-blink-features=AutomationControlled --no-sandbox --disable-dev-shm-usage --disable-gpu --disable-extensions --disable-popup-blocking"
            
            # 随机选择UA
            random_ua = random.choice(UA_POOL)
            anti_crawl_args += f" --user-agent={random_ua}"

            obj_json = self.browser_rpa.open_browser(
                url="http://babg-appweb-pre.oss-cn-hangzhou-yzwsouth-d01-a.res.zgf.yzwsouth.com/babgpt/index.html#/home",
                executable_path=r"D:/module/driver/86/chromedriver.exe",
                browser_path=r"D:/app/360Chrome/Chrome/Application/360chrome.exe",
                download_dir=self.g_dict["ls_dir"],
                run_log=True,
                browser_args=anti_crawl_args
            )
            self.driver = obj_json['driver']
            self.driver.maximize_window()
            action = ActionChains(driver=self.driver)
            
            time.sleep(0.5)

            # 登录一张网系统
            # 输入账号、密码
            username_elem = self.driver.find_element(By.XPATH, "//*[@placeholder='用户名/手机号/身份证']")
            password_elem = self.driver.find_element(By.XPATH, "//*[@type='password']")
            
            # 模拟真人输入
            human_input(username_elem, self.g_dict["login_acc"])
            random_sleep(0.8, 1.5)  # 输入账号后随机等待
            
            human_input(password_elem, self.g_dict["login_pw"])
            random_sleep(1, 2)  # 输入密码后随机等待
            
            # 点击登录按钮
            self.driver.find_element(By.XPATH, "//*[@type='button']").click()
            # 等待系统登录完成
            self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value="//aside/div/div[2]/*")
            random_sleep(1, 2)  # 等待页面加载
            # 点击办案
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value="//aside/div/div[2]/*")
            # 等待我的案件出现
            self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value='//span/*[text()="我的案件"]')
            random_sleep(1.5, 2.5)  # 点击后随机等待
            # 点击立案审核
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value='//span/*[text()="立案审核"]')
            random_sleep(0.5, 1)  # 点击后随机等待

        except Exception as e:
            self.g_dict["err"] = True
            logging.info(e)
            traceback.print_exc()

    def yw_cl(self):
        try:
            # 开始循环写入数据
            print("开始录入基本信息")
            payload = {
                "uniId": self.g_dict["table_id"],
                "pageSize": 1000,
                "reqParam": {
                    "queryParam": [
                        {
                            "field": "zt",
                            "value": [
                                "已完成"
                            ],
                            "sign": "<>"
                        }
                    ],
                    "updateMap": {
                        "zt": "",

                    }
                }
            }
            put_json = {
                "zt": "",
                "id": "",
                "uniId": self.g_dict["table_id"]
            }
            rqs_data = self.other_rpa.post_request(
                url="http://146.24.58.227:88/ymkj-api/uni/universal/list",
                payload=payload,
                auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
            data = rqs_data['data']['list']
            action = ActionChains(driver=self.driver)
            aj_info_dict = {}
            wait = WebDriverWait(self.driver,timeout=10)
            for infoVal in data:
                zbh = infoVal['zbh']
                # 以执保号为唯一值
                if not aj_info_dict.get(zbh):
                    aj_info_dict[zbh] = {}
                    aj_info_dict[zbh]["info"] = {}
                    aj_info_dict[zbh]["dsrkey"] = {}
                    aj_info_dict[zbh]["yjwh"] = infoVal["yjwh"]
                dsrName = infoVal['mc']
                aj_info_dict[zbh]["info"][dsrName] = infoVal
                aj_info_dict[zbh]["dsrkey"][dsrName] = True
                if infoVal.get("dlr") != "" and infoVal.get("dlr") is not None:
                    dlrName = infoVal.get("dlr")
                    # 说明这个代理人要勾选
                    aj_info_dict[zbh]["dsrkey"][dlrName] = True
            logging.info(aj_info_dict)
            for zbhId, ajInfo in aj_info_dict.items():
                info_dsr_names = set(ajInfo['info'].keys())
                yjwh = ajInfo["yjwh"]
                ah_list = re.findall("\\d+", yjwh)
                ah_dz = re.findall(r'[民刑行][初辖终]',yjwh)[0]
                ah_year = ah_list[0]
                ah_num = ah_list[2]


                for i in range(1,11):
                    try:
                        time.sleep(i+1)
                        # 使用js来定位元素，返回节点的某个属性
                        js = '''
                        var el = document.evaluate(
                          "//*[@id='app']/section/header/form//button/span[contains(text(),'新收登记')]",
                          document,
                          null,
                          XPathResult.FIRST_ORDERED_NODE_TYPE,
                          null
                        ).singleNodeValue;
                        return el ? el.textContent : null;
                        '''
                        element = self.driver.execute_script(js)
                        if element:
                            g_log.info("用JS定位能找到元素")
                            # 使用js来点击
                            js_click = '''
                            var el = document.evaluate(
                              "//*[@id='app']/section/header/form//button/span[contains(text(),'新收登记')]",
                              document,
                              null,
                              XPathResult.FIRST_ORDERED_NODE_TYPE,
                              null
                            ).singleNodeValue;
                            if (el) { el.click(); return true; } else { return false; }
                            '''
                            self.driver.execute_script(js_click)

                        else:
                            g_log.info("用JS定位不到元素")
                        break
                    except:
                        self.driver.save_screenshot(f"error_screenshot_{i}.png")
                        time.sleep(i)
                        g_log.info(f'第---------{i}次点击新收登记失败---------')
                        traceback.print_exc()
                        continue
                g_log.info(f'-----------------点击<新收登记>成功------------')

                time.sleep(2.5)
                # 点击首次执行案件 [执]
                for i in range(1, 11):
                    try:
                        time.sleep(i + 1)
                        # 使用js来定位元素，返回节点的某个属性
                        js = '''
                        var el = document.evaluate(
                          "//span[contains(text(),'首次执行案件')]",
                          document,
                          null,
                          XPathResult.FIRST_ORDERED_NODE_TYPE,
                          null
                        ).singleNodeValue;
                        return el ? el.textContent : null;
                        '''
                        element = self.driver.execute_script(js)
                        if element:
                            g_log.info("用JS定位能找到元素")
                            # 使用js来点击
                            js_click = '''
                            var el = document.evaluate(
                              "//span[contains(text(),'首次执行案件')]",
                              document,
                              null,
                              XPathResult.FIRST_ORDERED_NODE_TYPE,
                              null
                            ).singleNodeValue;
                            if (el) {
                              // 触发双击事件
                              var event = new MouseEvent('dblclick', {
                                'view': window,
                                'bubbles': true,
                                'cancelable': true
                              });
                              el.dispatchEvent(event);
                              return true;
                            } else {
                              return false;
                            }
                            '''
                            self.driver.execute_script(js_click)

                        else:
                            g_log.info("用JS定位不到元素")
                        break
                    except:
                        self.driver.save_screenshot(f"error_screenshot_{i}.png")
                        time.sleep(i)
                        g_log.info(f'第---------{i}次点击新收登记失败---------')
                        traceback.print_exc()
                        continue

                # 切换到立案编辑界面
                time.sleep(3)
                # self.driver.switch_to.window(self.driver.window_handles[1])
                # 切换窗口
                self.driver.switch_to.window(self.driver.window_handles[1])
                # 等待立案编辑界面
                self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value="//*[text()='案号']")
                time.sleep(0.5)

                # 引入依据
                # 点击引入审判案件
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value='//*[text()="引入审判案件"]')
                # 等待立案编辑界面
                self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value="//*[@placeholder='年度']")
                time.sleep(0.5)
                # 输入年份
                self.driver.find_element(By.XPATH,"//*[@placeholder='年度']/input").send_keys(ah_year)
                # 输入代字
                self.driver.find_element(By.XPATH,"//*[@placeholder='代字']/input").send_keys(ah_dz)
                # 输入案号
                self.driver.find_element(By.XPATH,"//*[@placeholder='序号']/input").send_keys(ah_num)
                # 点击查询
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value='//*[text()="查询"]')
                time.sleep(2)
                # 点击确认
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value='//*[text()="确认"]', idx=2)
                # 等待立案编辑界面
                self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value="//*[text()='名称']")
                time.sleep(0.5)

                # 取消全选当事人
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value="//div/span[@class='aty-table-column-checkbox aty-table-column-checkbox-checked']")
                # 抓取当事人信息
                table_obj = self.driver.find_element(By.XPATH,
                                                     "//*[text()='请选择需要导入的当事人']/following-sibling::div[2]//table/tbody")
                page_dsr_info = self.get_data_rpa.get_table_data(table_obj=table_obj)

                page_dsr_names = set()
                # 选择当事人
                for dsrIdx, dsrData in enumerate(page_dsr_info):
                    page_dsr_name = dsrData[1]
                    if ajInfo["info"].get(page_dsr_name):
                        logging.info(ajInfo["info"].get(page_dsr_name))
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=dsrIdx,
                                                     value="//td/span[contains(@class,'aty-table-column-checkbox')]")
                        page_dsr_names.add(page_dsr_name)
                    else:
                        continue
                    yjzw = ajInfo["info"][page_dsr_name].get("yjzw")
                    bde = ajInfo["info"][page_dsr_name].get("bde")
                    satj = ajInfo["info"][page_dsr_name].get("satj")
                extra_dsr_names = info_dsr_names - page_dsr_names
                logging.info(extra_dsr_names)

                # 抓取代理人信息
                dlr_table_obj = self.driver.find_element(By.XPATH,
                                                     "//*[text()='请选择需要导入的代理人']/following-sibling::div[1]//table/tbody")
                page_dlr_info = self.get_data_rpa.get_table_data(table_obj=dlr_table_obj)
                if len(page_dlr_info) != 0:
                    # 取消全选代理人
                    try:
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=1,
                                                     value="//div/span[@class='aty-table-column-checkbox aty-table-column-checkbox-checked']")
                    except:
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                     value="//div/span[@class='aty-table-column-checkbox aty-table-column-checkbox-checked']")
                    # 选择代理人
                    for dlrIdx, dlrData in enumerate(page_dlr_info):
                        logging.info(page_dlr_info)
                        page_dlr_name = dlrData[1]
                        if ajInfo["dsrkey"].get(page_dlr_name):
                            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=dlrIdx,
                                                         value="//td/span[@class='aty-table-column-checkbox']")

                # 点击确定
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value='//*[text()="确定"]')
                time.sleep(2)

                # 点击关闭
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value="(//*[text()='关闭'])[2]")

                # 点击收案途径
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value='//*[@id="sadj"]/div[2]//li[6]//div/span')
                time.sleep(0.5)
                # 选择收案途径
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value=f'//*[text()="{satj}"]')

                # 获取执行依据主文是否为空
                yjzwTx = self.driver.find_element(By.XPATH,"//*[@class='aty-textarea']").get_attribute('value')
                if yjzwTx == "":
                    # 输入执行依据主文
                    self.button_rpa.enter_in_target(driver=self.driver, by=By.XPATH,value="//*[@class='aty-textarea']",text=yjzw)
                # 勾选金钱给付
                self.driver.find_element(By.XPATH,"//*[text()='金钱给付']/preceding-sibling::input").click()
                # self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[text()='金钱给付']/preceding-sibling::input")
                # 点击金钱给付项目下拉框
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value="//*[text()='金钱给付项目']/parent::*/following-sibling::*//span[text()='请选择']")
                time.sleep(0.5)
                action.send_keys(Keys.ARROW_UP).perform()
                time.sleep(0.5)
                action.send_keys(Keys.ENTER).perform()
                # 输入标的额
                self.button_rpa.enter_in_target(driver=self.driver, by=By.XPATH,
                                                value="//*[text()='标的金额（元）']/parent::*/following-sibling::td//input",
                                                text=bde)
                # 点击计算
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value='//*[text()="计算"]')
                # 获取几个当事人
                form_list = self.driver.find_elements(By.XPATH,"//form[contains(@class,'fd-zxla-box-03 zrr aty-form')]")

                skzhIdx = 0
                for formDsrIdx, formObj in enumerate(form_list):
                    dsrLx = formObj.find_element(By.XPATH,
                                                 ".//*[text()='当事人类型']/parent::*/following-sibling::td[1]//span[@class='aty-select-selected-value']").text
                    if dsrLx == '自然人':
                        dsrName = formObj.find_element(By.XPATH,
                                                       ".//*[contains(text(),'姓名')]/parent::*/following-sibling::td[1]//input").get_attribute('value')
                    else:
                        dsrName = formObj.find_element(By.XPATH,
                                                       ".//*[contains(text(),'单位名称')]/parent::*/following-sibling::td[1]//input").get_attribute('value')
                    info_data = ajInfo["info"].get(dsrName)
                    ssdw_el = formObj.find_element(By.XPATH,
                                                   ".//*[contains(text(),'诉讼地位')]/parent::*/following-sibling::*//span[@class='aty-select-selected-value']")
                    ssdw = ssdw_el.text
                    if info_data.get('ssdw') == '申请保全人':
                        ssdwVal = '申请执行人'
                    elif info_data.get('ssdw') == '被保全人':
                        ssdwVal = '被执行人'
                    else:
                        ssdwVal = '被执行第三人'
                    if ssdw != ssdwVal:
                        ssdw_el.click()
                        time.sleep(1)
                        action.send_keys(Keys.ARROW_DOWN).perform()
                        action.send_keys(Keys.ARROW_DOWN).perform()
                        action.send_keys(Keys.ARROW_DOWN).perform()
                        time.sleep(0.5)
                        action.send_keys(Keys.ENTER).perform()

                    zjhm = formObj.find_element(By.XPATH,
                                                ".//*[contains(text(),'信息')]/parent::*/following-sibling::td//input[@placeholder='请填写证件号码']").get_attribute('value')
                    if zjhm != info_data.get('zjhm'):
                        zjhm_el = formObj.find_element(By.XPATH,
                                             ".//*[contains(text(),'信息')]/parent::*/following-sibling::td//input[@placeholder='请填写证件号码']")
                        zjhm_el.click()
                        zjhm_el.clear()
                        zjhm_el.send_keys(info_data.get('zjhm'))

                    time.sleep(1.5)
                    if dsrLx == '自然人':
                        # 点击验证
                        formObj.find_element(By.XPATH,".//*[text()='验证']").click()
                        time.sleep(3.5)
                        dz_el = formObj.find_element(By.XPATH,
                                                       ".//*[text()='现住址']/parent::*/following-sibling::td[1]//input")
                        dz = dz_el.get_attribute('value')
                        if dz != "" and info_data.get('dz') != dz:
                            self.driver.execute_script("arguments[0].click();",dz_el)
                            # dz_el.click()
                            dz_el.clear()
                            dz_el.send_keys(info_data.get('dz'))
                        if ssdw == '被执行人':
                            wcn_el = formObj.find_element(By.XPATH,
                                                 ".//*[text()='是否未成年']/parent::*/following-sibling::td[1]//*[text()='是']/preceding-sibling::input")
                            self.driver.execute_script("arguments[0].click();", wcn_el)
                    else:
                        # 点击查询
                        formObj.find_element(By.XPATH,
                                             ".//*[text()='查询']").click()
                        time.sleep(3.5)
                        dz_el = formObj.find_element(By.XPATH,
                                                     ".//*[text()='注册地']/parent::*/following-sibling::td[1]//input")
                        dz = dz_el.get_attribute('value')
                        if info_data.get('dz') != "" and info_data.get('dz') != dz:
                            self.driver.execute_script("arguments[0].click();",dz_el)
                            # dz_el.click()
                            dz_el.clear()
                            dz_el.send_keys(info_data.get('dz'))# .perform()
                        try:
                            tshy_el = formObj.find_element(By.XPATH,
                                                         ".//*[text()='特殊行业']/parent::*/following-sibling::td[1]//input[contains(@class,'aty-select-input')]")
                            tshy_el.click()
                            time.sleep(1)
                            action.send_keys(Keys.ARROW_DOWN).perform()
                            time.sleep(0.5)
                            action.send_keys(Keys.ENTER).perform()
                        except:
                            pass
                        try:
                            dwxz_el = formObj.find_element(By.XPATH,
                                                         ".//*[text()='单位性质']/parent::*/following-sibling::td[1]//span[contains(@class,'aty-select-placeholder')]")
                            dwxz_el.click()
                            time.sleep(1)
                            action.send_keys(Keys.ARROW_DOWN).perform()
                            time.sleep(0.5)
                            action.send_keys(Keys.ENTER).perform()
                        except:
                            pass
                        try:
                            dwlx_el = formObj.find_element(By.XPATH,
                                                        ".//*[text()='单位类型']/parent::*/following-sibling::td[1]//span[contains(@class,'aty-select-placeholder')]")
                            dwlx_el.click()
                            time.sleep(1)
                            action.send_keys(Keys.ARROW_UP).perform()
                            time.sleep(0.5)
                            action.send_keys(Keys.ENTER).perform()
                        except:
                            pass

                    # 签署送达地址确认书及电子送达选择
                    if info_data.get('ssdw') == "申请保全人":
                        if info_data.get('dlrlxfs') is not None:
                            dlrlxfs_el = formObj.find_element(By.XPATH,
                                                 ".//*[text()='联系方式']/parent::*/following-sibling::*//input[@class='aty-input']")
                            dlrlxfs_el.click()
                            dlrlxfs_el.send_keys(Keys.CONTROL,'a')
                            dlrlxfs_el.send_keys(Keys.BACKSPACE)
                            dlrlxfs_el.send_keys(info_data.get('dlrlxfs'))

                        # self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=formDsrIdx,
                        #                              value="//*[text()='签署送达地址确认书']/parent::*/following-sibling::td[1]//*[text()='是']/preceding-sibling::input")
                        qrs_el = formObj.find_element(By.XPATH,
                                             ".//*[text()='签署送达地址确认书']/parent::*/following-sibling::td[1]//*[text()='是']/preceding-sibling::input")
                        self.driver.execute_script("arguments[0].click();",qrs_el)
                        dzsd_el = formObj.find_element(By.XPATH,
                                             ".//*[text()='同意电子送达']/parent::*/following-sibling::td[1]//*[text()='是']/preceding-sibling::input")
                        self.driver.execute_script("arguments[0].click();", dzsd_el)
                    else:
                        qrs_el = formObj.find_element(By.XPATH,
                                              ".//*[text()='签署送达地址确认书']/parent::*/following-sibling::td[1]//*[text()='否']/preceding-sibling::input")
                        self.driver.execute_script("arguments[0].click();", qrs_el)
                        dzsd_el = formObj.find_element(By.XPATH,
                                             ".//*[text()='同意电子送达']/parent::*/following-sibling::td[1]//*[text()='否']/preceding-sibling::input")
                        self.driver.execute_script("arguments[0].click();", dzsd_el)
                    # 清空送达收件人
                    sjr = formObj.find_element(By.XPATH,".//*[text()='送达收件人']/parent::*/following-sibling::td[1]//input")
                    sjr.click()
                    sjr.send_keys(Keys.CONTROL, 'a')
                    sjr.send_keys(Keys.BACKSPACE)
                    # 清空送达电话
                    sddh = formObj.find_element(By.XPATH,".//*[text()='送达电话']/parent::*/following-sibling::td[1]//input")
                    sddh.send_keys(Keys.CONTROL,'a')
                    sddh.send_keys(Keys.BACKSPACE)
                    # 清空收件人证件号码
                    sjrzjhm = formObj.find_element(By.XPATH,".//*[text()='收件人证件号码']/parent::*/following-sibling::td[1]//input")
                    sjrzjhm.send_keys(Keys.CONTROL,'a')
                    sjrzjhm.send_keys(Keys.BACKSPACE)
                    # 清空送达地址
                    sddz = formObj.find_element(By.XPATH,".//*[text()='送达地址']/parent::*/following-sibling::td[1]//input")
                    sddz.send_keys(Keys.CONTROL, 'a')
                    sddz.send_keys(Keys.BACKSPACE)
                    # 点击确认
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=formDsrIdx,value="//*[text()='确认']")
                    if info_data.get('ssdw') == "申请保全人":
                        if dsrLx == '法人':
                            # 点击收款账户
                            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=skzhIdx, value=".//*[text()='收款账户']")
                            skzhIdx = skzhIdx + 1

                        time.sleep(2)
                        tk_iframe = self.driver.find_element(By.XPATH, "//iframe[@class='aty-iframe']")
                        self.driver.switch_to.frame(tk_iframe)
                        # 等待当事人收款账户界面
                        self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,value="//*[text()='保存']")
                        time.sleep(1)
                        # 点击收款人与当事人关系下拉框
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                     value="//*[contains(text(),'收款人与当事人关系')]/parent::*//input")
                        # 选择本人账户
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[contains(text(),'本人账户')]")
                        # 填写收款人证件号码
                        skrzjhm = self.driver.find_element(By.XPATH,"//*[contains(text(),'收款人证件号码')]/parent::*//input")
                        skrzjhm.send_keys(info_data.get('zjhm'))
                        # 填写账号
                        zh = self.driver.find_element(By.XPATH,"//*[contains(text(),'账号')]/parent::*//input")
                        zh.send_keys('0')
                        # 选择开户银行
                        khyh = self.driver.find_element(By.XPATH,"//*[contains(text(),'开户银行')]/parent::*//input")
                        khyh.send_keys('顺德农村商业银行')
                        time.sleep(1)
                        action.send_keys(Keys.ARROW_DOWN).perform()
                        time.sleep(1)
                        action.send_keys(Keys.ENTER).perform()
                        # 点击不允许
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                     value="//*[contains(text(),'允许他案使用')]/parent::*//*[text()='不允许']/preceding-sibling::*/input")
                        # 点击否
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                     value="//*[contains(text(),'是否确认')]/parent::*//*[text()='否']/preceding-sibling::*/input")
                        # 点击正常
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                     value="//*[contains(text(),'状态')]/parent::*//*[text()='正常']/preceding-sibling::*/input")
                        # 点击保存
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[text()='保存']")
                        time.sleep(2)
                        self.driver.switch_to.default_content()

                    # 获取几个法人
                    fr_form_list = self.driver.find_elements(By.XPATH,
                                                             "//*[@id='xgrxx']/form")
                    # 开始验证法人
                    if info_data.get('fr') != '':
                        # fr_from_obj  # 法人表单对象
                        for formfrIdx,fr_form_obj in enumerate(fr_form_list):
                            # 获取界面关联当事人
                            page_gldsr_name = fr_form_obj.find_element(By.XPATH,
                                                                        ".//*[text()='关联当事人']/parent::*/following-sibling::td[1]//div/span").text
                            if page_gldsr_name == info_data.get("mc"):  # 判断是不是这个当事人的法人
                                # 获取界面法人名称
                                page_frname_str = fr_form_obj.find_element(By.XPATH,
                                                                            ".//*[text()='姓名']/parent::*/following-sibling::td[1]//input").get_attribute('value')
                                if page_frname_str != info_data.get("fr"):  # 不等于法人名字
                                    # 修改法人名称
                                    frname_el = fr_form_obj.find_element(By.XPATH,
                                                             ".//*[text()='姓名']/parent::*/following-sibling::td[1]//input")
                                    frname_el.click()
                                    frname_el.clear()
                                    frname_el.send_keys(info_data.get("fr"))
                                try:
                                # 判断界面法人是否有证件号码
                                    page_frzjhm_str = fr_form_obj.find_element(By.XPATH,
                                           ".//*[contains(text(),'证件信息')]/parent::*/following-sibling::td/div//input[@class='aty-input']").get_attribute('value')
                                    fr_form_obj.find_element(By.XPATH, ".//*[text()='验证']").click()
                                except:
                                    page_frzjhm_str = None
                                # 判断法人证件号码是否为空
                                if page_frzjhm_str is None:
                                    if info_data.get('frzjhm') is None:
                                    # 点击法人提供证件为否
                                        fr_form_obj.find_element(By.XPATH,
                                                                 ".//*[text()='否']/preceding-sibling::input").click()
                                        # 填写法人无法提供证件原因
                                        fr_form_obj.find_element(By.XPATH,".//*[text()='无法提供证件原因']/parent::*/following-sibling::td[1]//input").send_keys('暂无身份证号码')
                                    else:
                                        # 点击法人提供证件为是
                                        fr_form_obj.find_element(By.XPATH,
                                                                 ".//*[text()='是']/preceding-sibling::input").click()
                                        # 点击证件号码下拉框
                                        fr_form_obj.find_element(By.XPATH,
                                                                 ".//*[text()='证件信息']/parent::*/following-sibling::td//*[@class='fd-lxfs-select']//div/span").click()
                                        time.sleep(1)
                                        action.send_keys(Keys.ARROW_DOWN).perform()
                                        time.sleep(0.5)
                                        action.send_keys(Keys.ENTER).perform()
                                        time.sleep(1)
                                        fr_form_obj.find_element(By.XPATH,
                                             ".//*[contains(text(),'证件信息')]/parent::*/following-sibling::td/div//input[@class='aty-input']").send_keys(info_data.get('frzjhm'))
                                        fr_form_obj.find_element(By.XPATH, ".//*[text()='验证']").click()
                                try:
                                    # 点击性别下拉框
                                    fr_form_obj.find_element(By.XPATH,".//*[text()='性别']/parent::*/following-sibling::td[1]//span[@class='aty-select-placeholder']").click()
                                    time.sleep(1)
                                    # 选择未说明的性别
                                    action.send_keys(Keys.ARROW_UP).perform()
                                    time.sleep(0.5)
                                    action.send_keys(Keys.ENTER).perform()
                                except:
                                    pass
                            # 点击确认
                            fr_form_obj.find_element(By.XPATH,".//*[text()='确认']").click()

                    # 获取几个代理人
                    dlr_form_list = self.driver.find_elements(By.XPATH,
                                                              "//*[@id='dlr']/form")
                    # 开始验证代理人
                    if info_data.get("dlr") is not None:
                        if not dlr_form_list:
                            logging.info('添加代理人---------------------')
                            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                         value="//*[text()='添加代理人']")
                            time.sleep(2)
                            dlr_form_list = self.driver.find_elements(By.XPATH,
                                                                      "//*[@id='dlr']/form")
                            for formdlrIdx, dlr_form_obj in enumerate(dlr_form_list):
                                dlr_form_obj.find_element(By.XPATH,".//*[text()='代理当事人']/parent::*/following-sibling::td[1]//div/span").click()
                                logging.info(info_data.get('dldsr'))
                                # 选取代理当事人
                                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,idx=1,
                                                             value=f"//div/ul/li[text()='{info_data.get('dldsr')}']")
                                # 选取代理当事人
                                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,idx=2,
                                                             value=f"//div/ul/li[text()='{info_data.get('dldsr')}']")
                                dlr_form_obj.find_element(By.XPATH,
                                                          ".//*[text()='是否法律援助']/parent::*/following-sibling::td[1]//*[text()='是']/preceding-sibling::input").click()
                                dlr_form_obj.find_element(By.XPATH,
                                                          ".//*[text()='姓名']/parent::*/following-sibling::td[1]//div/input").send_keys(info_data.get('dlr'))
                                if info_data.get('dlrzjhm') is None:
                                    dlrzjhm_el = dlr_form_obj.find_element(By.XPATH,
                                                              ".//*[text()='证件类型']/parent::*/following-sibling::td[1]//span[@class='aty-select-selected-value']")
                                    dlrzjhm_el.click()
                                    time.sleep(0.5)
                                    action.send_keys(Keys.ARROW_UP).perform()
                                    time.sleep(0.5)
                                    action.send_keys(Keys.ENTER).perform()
                                    dlr_form_obj.find_element(By.XPATH,
                                                              ".//*[text()='证件号码']/parent::*/following-sibling::td[1]//input").send_keys('无身份证信息')
                                else:
                                    dlr_form_obj.find_element(By.XPATH,
                                                              ".//*[text()='证件号码']/parent::*/following-sibling::td[1]//input").send_keys(info_data.get('dlrzjhm'))
                                dlr_form_obj.find_element(By.XPATH,
                                                          ".//*[text()='律所名称']/parent::*/following-sibling::td[1]//input").send_keys(info_data.get('dlrlsmc'))
                                dlr_form_obj.find_element(By.XPATH,
                                                          ".//*[text()='律师执业证号']/parent::*/following-sibling::td[1]//input").send_keys(info_data.get('dlrzyzh'))
                                dlr_form_obj.find_element(By.XPATH,
                                                          ".//*[text()='签署送达地址确认书']/parent::*/following-sibling::td[1]//*[text()='是']/preceding-sibling::input").click()
                                dlr_form_obj.find_element(By.XPATH,
                                                          ".//*[text()='同意电子送达']/parent::*/following-sibling::td[1]//*[text()='是']/preceding-sibling::input").click()
                                # 点击确认
                                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,idx=formdlrIdx,
                                                             value="//*[@id='dlr']//*[text()='确认']")
                        else:
                            # 说明有代理人 需要验证信息
                            for formdlrIdx,dlr_form_obj in enumerate(dlr_form_list):
                                page_dldsr_name = dlr_form_obj.find_element(By.XPATH,
                                                                            ".//*[text()='代理当事人']/parent::*/following-sibling::td[1]//div/span").text
                                if page_dldsr_name == info_data.get("dldsr"):  # 判断是不是对应代理当事人
                                    # # 点击代理类型下拉框
                                    # self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,idx=formdlrIdx,
                                    #                              value="//*[text()='代理类型']/parent::*/following-sibling::td[1]//div/span")
                                    # # 选择委托代理
                                    # self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,idx=formdlrIdx,value="//*[text()='委托代理']")
                                    # 获取界面代理人
                                    page_dlr_name_obj = dlr_form_obj.find_element(By.XPATH,
                                                                                  ".//*[text()='姓名']/parent::*/following-sibling::td[1]//input")
                                    page_dlr_name = page_dlr_name_obj.get_attribute('value')
                                    # 判断界面代理人与数据是否一致
                                    if page_dlr_name != info_data.get("dlrmc"):
                                        # 修改代理人名称
                                        page_dlr_name_obj.click()
                                        page_dlr_name_obj.clear()
                                        page_dlr_name_obj.send_keys(info_data.get("dlrmc"))

                                    # 获取界面代理当事人证件号码
                                    page_dlr_zjhm_obj = dlr_form_obj.find_element(By.XPATH,
                                                                                  ".//*[text()='证件号码']/parent::*/following-sibling::td[1]//input")
                                    page_dlr_zjhm = page_dlr_zjhm_obj.get_attribute('value')
                                    if page_dlr_zjhm != info_data.get("dlrzjhm") and info_data.get("dlrzjhm") != '':
                                        # 修改代理人名称
                                        page_dlr_zjhm_obj.click()
                                        page_dlr_zjhm_obj.clear()
                                        page_dlr_zjhm_obj.send_keys(info_data.get("dlrZjhm"))
                                    # 点击国家或地区下拉框
                                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=formdlrIdx,
                                                                 value="//*[text()='国家或地区']/parent::*/following-sibling::td[1]//div/span")
                                    # 选择中国
                                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,idx=formdlrIdx + len(fr_form_list) + 1,
                                                                 value="//*[@class='aty-select-dropdown-list']//*[text()='中国']")
                                    # 获取界面代理人律所名称
                                    page_dlr_lsmc_obj = dlr_form_obj.find_element(By.XPATH,
                                                                                  ".//*[text()='律所名称']/parent::*/following-sibling::td[1]//input")
                                    page_dlr_lsmc = page_dlr_lsmc_obj.get_attribute('value')
                                    if page_dlr_lsmc != info_data.get("dlrlsmc"):
                                        # 修改代理人律所名称
                                        page_dlr_lsmc_obj.click()
                                        page_dlr_lsmc_obj.clear()
                                        page_dlr_lsmc_obj.send_keys(info_data.get("dlrZjhm"))

                                    # 获取界面代理人律师执业证号
                                    page_dlr_zyzh_obj = dlr_form_obj.find_element(By.XPATH,
                                                                                  ".//*[text()='律师执业证号']/parent::*/following-sibling::td[1]//input")
                                    page_dlr_zyzh = page_dlr_zyzh_obj.get_attribute('value')
                                    if page_dlr_zyzh != info_data.get("dlrzyzh"):
                                        # 修改代理人名称
                                        page_dlr_zyzh.click()
                                        page_dlr_zyzh.clear()
                                        page_dlr_zyzh.send_keys(info_data.get("dlrzyzh"))

                                    dlr_form_obj.find_element(By.XPATH,
                                                         ".//*[text()='签署送达地址确认书']/parent::*/following-sibling::td[1]//*[text()='否']/preceding-sibling::input").click()
                                    dlr_form_obj.find_element(By.XPATH,
                                                         ".//*[text()='同意电子送达']/parent::*/following-sibling::td[1]//*[text()='否']/preceding-sibling::input").click()
                                # 点击确认
                                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                             idx=formdlrIdx + len(fr_form_list) + len(form_list),
                                                             value="//*[text()='确认']")
                for extra_dsr in extra_dsr_names:
                    info_data = ajInfo["info"].get(extra_dsr)
                    logging.info(info_data)
                    if info_data.get('dsrlx') == '自然人':
                        # 新增自然人
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value="//*[text()='新增自然人']")
                    else:
                        # 新增法人
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[text()='新增法人']")
                    time.sleep(3)
                    # 获取几个当事人
                    xz_form_list = self.driver.find_elements(By.XPATH,
                                                          "//form[contains(@class,'fd-zxla-box-03 zrr aty-form')]")
                    for xzIdx,xzObj in enumerate(xz_form_list):
                        # 诉讼地位选择被执行人
                        xzObj.find_element(By.XPATH,
                                           ".//*[contains(text(),'诉讼地位')]/parent::*/following-sibling::*//span[@class='aty-select-placeholder']").click()
                        time.sleep(0.5)
                        action.send_keys(Keys.ARROW_DOWN).perform()
                        time.sleep(0.5)
                        action.send_keys(Keys.ARROW_DOWN).perform()
                        time.sleep(0.5)
                        action.send_keys(Keys.ENTER).perform()
                        # 输入当事人名称
                        xzObj.find_element(By.XPATH,
                                           ".//*[contains(text(),'姓名')]/parent::*/following-sibling::td[1]//input").send_keys(extra_dsr)
                        # 选择性别
                        xzObj.find_element(By.XPATH,
                                                 ".//*[text()='性别']/parent::*/following-sibling::td[1]//span[@class='aty-select-placeholder']").click()
                        time.sleep(1)
                        # 选择未说明的性别
                        action.send_keys(Keys.ARROW_UP).perform()
                        time.sleep(0.5)
                        action.send_keys(Keys.ENTER).perform()
                        # 输入证件号码
                        xzObj.find_element(By.XPATH,
                                             ".//*[contains(text(),'信息')]/parent::*/following-sibling::td//input[@placeholder='请填写证件号码']").send_keys(info_data.get('zjhm'))
                        # 点击验证
                        xzObj.find_element(By.XPATH, ".//*[text()='验证']").click()
                        time.sleep(2)
                        # 输入地址
                        xzObj.find_element(By.XPATH,
                                             ".//*[text()='现住址']/parent::*/following-sibling::td[1]//input").send_keys(info_data.get('dz'))
                        time.sleep(1)
                        # 点击是
                        xzObj.find_element(By.XPATH,
                                           ".//*[text()='是否未成年']/parent::*/following-sibling::td[1]//*[text()='是']/preceding-sibling::input").click()
                        # 签署送达地址确认书及电子送达选择
                        xzObj.find_element(By.XPATH,
                                           ".//*[text()='同意电子送达']/parent::*/following-sibling::td[1]//*[text()='否']/preceding-sibling::input").click()
                        break
                    # 点击确认
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=xzIdx, value="//*[text()='确认']")

                # 点击审查人下拉框
                self.button_rpa.enter_in_target(driver=self.driver, by=By.XPATH,
                                                value="//*[text()='审查人']/parent::*/following-sibling::td//input",
                                                text=self.g_dict["laspr"])
                time.sleep(0.5)
                action.send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(0.5)
                action.send_keys(Keys.ENTER).perform()

                # self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[text()='暂存']")
                # 点击提交
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[text()='提交']")
                time.sleep(1)
                # 点击确定
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value="//div[@class='aty-modal-wrap']//button/span[text()='确定']")
                # 等待案件确认界面
                self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,value="//*[text()='保存并重新提交']")
                time.sleep(2)
                # 点击保存并重新提交
                self.driver.find_element(By.XPATH,"//*[text()='保存并重新提交']").click()
                time.sleep(1.5)
                # 点击确定
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value="//div[@class='aty-modal-wrap']//button/span[text()='确定']")
                try:
                    # 等待呈批界面
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,value="//*[text()='呈批']")
                except:
                    self.driver.find_element(By.XPATH,"//*[text()='拆分案件情形']/parent::*/following-sibling::*//span[text()='请选择']").click()
                    time.sleep(0.5)
                    action.send_keys(Keys.ARROW_UP).perform()
                    time.sleep(0.5)
                    action.send_keys(Keys.ENTER).perform()
                    # 点击保存并重新提交
                    self.driver.find_element(By.XPATH, "//*[text()='保存并重新提交']").click()
                    time.sleep(1.5)
                    # 点击确定
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//div[@class='aty-modal-wrap']//button/span[text()='确定']")
                    # 等待呈批界面
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value="//*[text()='呈批']")
                time.sleep(1.5)
                # 点击审批人下拉框
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value="//*[text()='审批人']/parent::*/following-sibling::*//span[text()='请选择']")
                time.sleep(1)
                # 选择审批人
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value=f"//*[@class='aty-select-dropdown-list']/*[text()='{self.g_dict['laspr']}']")
                # 点击呈批
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[text()='呈批']")
                # 回到主页
                window_list = self.driver.window_handles
                while len(window_list) > 1:
                    self.driver.switch_to.window(window_list[-1])
                    self.driver.close()
                    window_list = self.driver.window_handles
                window_list = self.driver.window_handles
                self.driver.switch_to.window(window_list[0])
                for p_val in ajInfo['info']:
                    logging.info(ajInfo['info'][p_val]['id'])
                    put_json['id'] = ajInfo['info'][p_val]['id']
                    put_json['zt'] = "已完成"
                    rqs_data = self.other_rpa.put_request(
                        url="http://146.24.58.227:88/ymkj-api/uni/universal/edit",
                        payload=put_json,
                        auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
                time.sleep(3)

            # 点击首页
            for i in range(1,11):
                try:
                    time.sleep(i+1)
                    # 使用js来定位元素，返回节点的某个属性
                    js = '''
                    var el = document.evaluate(
                      "//aside/div/div[1]/*",
                      document,
                      null,
                      XPathResult.FIRST_ORDERED_NODE_TYPE,
                      null
                    ).singleNodeValue;
                    return el ? el.textContent : null;
                    '''
                    element = self.driver.execute_script(js)
                    if element:
                        g_log.info("用JS定位能找到元素")
                        # 使用js来点击
                        js_click = '''
                        var el = document.evaluate(
                          "//aside/div/div[1]/*",
                          document,
                          null,
                          XPathResult.FIRST_ORDERED_NODE_TYPE,
                          null
                        ).singleNodeValue;
                        if (el) { el.click(); return true; } else { return false; }
                        '''
                        self.driver.execute_script(js_click)

                    else:
                        g_log.info("用JS定位不到元素")
                    break
                except:
                    self.driver.save_screenshot(f"error_screenshot_{i}.png")
                    time.sleep(i)
                    g_log.info(f'第---------{i}次点击新收登记失败---------')
                    traceback.print_exc()
                    continue
            time.sleep(2)
            # 点击更多
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[contains(text(),'更多')]")
            # 等待待办
            self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,value="(//*[text()='待办'])[2]")
            time.sleep(0.5)
            # 点击待办
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="(//*[text()='待办'])[2]")
            # 点击类型
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                         value="(//*[contains(@class,'yzw-babgpt-input yzw-babgpt-input')])[3]")
            # 点击 立案审批
            time.sleep(1.1)
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=-1, value="//*[text()='立案审批']")
            # 抓取待办数据
            while True:
                data_list = self.driver.find_elements(By.XPATH, "//*[@class='title-text link-text']")
                if len(data_list) > 0:
                    # 开始审批
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[@class='title-text link-text']")
                    time.sleep(2)
                    # # 切换iframe
                    tk_iframe = self.driver.find_element(By.XPATH, "//*[@class='yzw-app-window']")
                    self.driver.switch_to.frame(tk_iframe)
                    # 等待数据加载
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, timeout=20,value="//*[@class='el-button el-button--primary']/span")
                    time.sleep(1)
                    # 开始审批
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,value="//*[@class='el-button el-button--primary']/span")
                    self.driver.switch_to.default_content()
                    time.sleep(3)
                else:
                    break
            gb_el = self.driver.find_element(By.XPATH,"//body/div/div/div/button/i")
            self.driver.execute_script("arguments[0].click();",gb_el)

        except Exception as e:
            self.g_dict["err"] = True
            logging.info(e)
            traceback.print_exc()

    def get_zb_data(self):
        try:
            pass
        except Exception as e:
            self.g_dict["err"] = True
            logging.info(e)
            traceback.print_exc()

    def run_business(self):
        """实现具体的业务逻辑 - 完全使用aibot_common的浏览器操作组件"""
        try:
            g_log.info("开始执行业务逻辑...")
            # self.config.set_config("base_url", "http://www.qq.com")
            # self.init_browser()
            g_log.info("重试次数：%d", get_retry_count())
            g_log.info("业务逻辑执行中----")
            self.g_dict["err"] = False
            # 使用配置字典 读取参数
            g_log.info("---------------初始化开始")
            self.csh()
            g_log.info("---------------初始化结束")
            g_log.info("---------------业务初始化开始")
            self.yw_csh()
            g_log.info("---------------业务初始化开始结束")
            g_log.info("---------------业务处理开始")
            self.yw_cl()
            g_log.info("---------------业务处理结束")
            # 关闭谷歌浏览器
            # self.driver.close()
            time.sleep(1)
            self.logger.info("流程执行完毕")
            # 移除直接调用driver.quit()，避免与finally块中的driver_quit()重复
            # shutil.rmtree(self.g_dict["ls_dir"])
            if self.g_dict["err"]:
                raise Exception("存在异常，进入重试")

            g_log.info("业务逻辑执行完成")

            return True
        except Exception as e:
            g_log.exception(f"业务逻辑执行异常: {e}")
            return False
        finally:
            # 使用self.browser_rpa关闭浏览器
            try:
                g_log.info("使用self.browser_rpa关闭浏览器...")
                try:
                    shutil.rmtree(self.g_dict["ls_dir"])
                except Exception as e:
                    pass
                self.browser_rpa.close_browser()
            except Exception as e:
                g_log.warning(f"关闭浏览器时出错: {e}")
                # 降级使用原有的关闭方式
                self.driver_quit()


def main():
    """主函数"""
    from aibot_rpa.config.manager import ConfigManager

    exit_code = 0
    flow = None

    try:
        g_log.info("=== 程序启动 ===")

        # 1. 初始化配置管理器
        config_manager = ConfigManager()

        # 2. 加载配置
        config_template = {
            "taskId": "minimal_demo_001",
            "name": "执行立案",
            # "log_path": "d:/rpa_profile/log/极简demo/demo.log",
            # "video_path": "d:/rpa_profile/video/极简demo/demo.webm",
            # "executable_path": "d:/code/ymkj/ymkj-aibot/chromedriver.exe",
            # "browser_path": "D:/app/app/360Chrome/Chrome/Application/360chrome.exe",
            # "executable_path": "D:/module/driver/86/chromedriver.exe",
            # "browser_path": "C:/Users/mo/AppData/Local/360Chrome/Chrome/Application/360chrome.exe",
            "max_retries": 2,
            "retry_delay": 2,
            "timeout": 30,
            "record_video": True,
            "live_push": True,
            "headless": False,
            "start_time": "2025-11-20",
            "AuthCode": "2TR5gFSPA3DCbj374poHt",
            # "loginPW": r"tata1234#",
            # "loginAcc": r"18000850370",
            "loginPW": r"kiwi.123",
            "loginAcc": r"15113721138",
            "laSpr": r"邝咏宜",
            "isPW": None,
            "end_time": "2025-11-25",
            "uniTable": [["N5MTtHFPOUiGcgQ4epSY2","当事人信息"],["NrosOw_GmtBHP5V13AnK4", "执行立案"]],
            "保存路径": r"\\146.24.58.227\机器人相关"
            # "base_url": "http://www.baidu.com",
        }
        s = config_template["loginPW"]
        if s.startswith('0') and s.isdigit():
            config_template['isPW'] = True

        # 2. 加载配置（控制台没有就用config_template）
        config_manager.load_config_args(config_template)
        # 加载自定义配置
        config_manager.load_dict({
            "executable_path": r"D:/module/driver/86/chromedriver.exe",
            "browser_path": r"D:/app/360Chrome/Chrome/Application/360chrome.exe",
            "record_fps": 10,  # 降低帧率以确保更稳定的录制
            "record_video": True,
            "live_push": False  # 禁用直播推送，专注于本地录制
        })

        g_log.info(f"配置加载完成: {config_manager.get_config('name', 'Unknown')}")

        # 3. 执行流程
        g_log.info("开始执行RPA流程...")
        flow = MinimalRPAFlow(config_manager=config_manager)
        result = flow.execute()

        if result:
            g_log.info("✅ RPA流程执行成功！")
            g_log.info({"msg": "已完成"})
            exit_code = 0
        else:
            g_log.error("❌ RPA流程执行失败！")
            g_log.info({"error": "运行异常"})
            exit_code = 1

    except KeyboardInterrupt:
        g_log.warning("⚠️ 用户中断程序执行")
        exit_code = 2

    except Exception as e:
        g_log.exception(f"💥 程序执行异常: {e}")
        exit_code = 1

    finally:
        # 确保关闭浏览器
        try:
            if flow and hasattr(flow, 'driver') and flow.driver:
                flow.driver_quit()
                g_log.info("浏览器已关闭")
        except Exception as e:
            g_log.warning(f"关闭浏览器时出错: {e}")
        g_log.info("=== 程序结束 ===")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
