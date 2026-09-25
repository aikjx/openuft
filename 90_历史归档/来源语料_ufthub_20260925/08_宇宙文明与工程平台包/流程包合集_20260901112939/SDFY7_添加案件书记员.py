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
from selenium.webdriver.common.by import By

from aibot_common.getdata_rpa import GETDATA_RPA

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
import time
from aibot_rpa.browser.record_video import VideoRecorder  # Add import
import logging
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from operator import itemgetter
import requests
from selenium.webdriver.common.by import By
import random
import re
import shutil
import sys
import os
import json
import time
import datetime

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
            print(rqs_data)
            data = rqs_data['data']['list']
            if len(data) == 0:  # 判断是否还有数据需要操作
                break

    def csh(self):
        try:
            # 使用配置字典 读取参数
            config_dict = self.config_manager.get_dict_config()
            self.g_dict["config_dict"] = config_dict
            # logging.info("***********1")
            # logging.info(config_dict)
            # logging.info(config_dict["AuthCode"])
            # logging.info(config_dict["uniTable"])
            self.g_dict["auth_code"] = config_dict["AuthCode"]
            print(self.g_dict["auth_code"])
            self.g_dict["table_id"] = config_dict["uniTable"][0][0]
            print(self.g_dict["table_id"])
            logging.info(config_dict["loginAcc"])
            # logging.info(config_dict["isPW"])
            self.g_dict["login_acc"] = str(config_dict["loginAcc"])
            # self.g_dict["login_pw"] = "060218"
            if config_dict["isPW"]:
                self.g_dict["login_pw"] = "0"+str(config_dict["loginPW"])
            else:
                self.g_dict["login_pw"] = str(config_dict["loginPW"])
            logging.info(config_dict["loginPW"])

            # self.start_data(self.g_dict["table_id"], self.g_dict["auth_code"]) # 初始化异常数据

            # 使用配置字典 读取参数
            self.g_dict["start_time"] = config_dict["start_time"]
            self.g_dict["end_time"] = config_dict["end_time"]
            logging.info(self.g_dict["start_time"])
            logging.info(self.g_dict["end_time"])
            self.g_dict["save_dir"] = config_dict["保存路径"]
            if not os.path.isdir(self.g_dict["save_dir"]):
                os.makedirs(self.g_dict["save_dir"])
            if self.g_dict["start_time"] == "" and self.g_dict["end_time"] == "":
                new_data = datetime.datetime.now()
                new_data = datetime.timedelta(days=-1) + new_data
                new_data = new_data.strftime("%Y-%m-%d")
                self.g_dict["start_time"] = new_data
                self.g_dict["end_time"] = new_data
            else:
                if self.g_dict["start_time"] == "":
                    self.g_dict["start_time"] = self.g_dict["end_time"]
                elif self.g_dict["end_time"] == "":
                    self.g_dict["end_time"] = self.g_dict["start_time"]
            self.g_dict["new_data"] = self.g_dict["start_time"] + "至" + self.g_dict["end_time"]
            self.g_dict["save_path"] = self.g_dict["save_dir"] + r"/添加案件书记员" + self.g_dict["new_data"] + ".xlsx"
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

            obj_json = self.browser_rpa.open_browser(
                url="http://babg-appweb-pre.oss-cn-hangzhou-yzwsouth-d01-a.res.zgf.yzwsouth.com/babgpt/index.html#/home",
                executable_path=r"D:/module/driver/86/chromedriver.exe",
                browser_path=r"D:\360Chrome\Chrome\Application\360chrome.exe",
                download_dir=self.g_dict["ls_dir"],
                run_log=True,
            )
            self.driver = obj_json['driver']
            logging.info(self.driver)
            self.driver.maximize_window()

            # self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
            #                                         value='//*[text()="下载前询问每个文件的保存位置"]')
            time.sleep(0.5)

            # 登录一张网系统
            # # 打开系统网址
            # self.driver.get(
            #     "http://babg-appweb-pre.oss-cn-hangzhou-yzwsouth-d01-a.res.zgf.yzwsouth.com/babgpt/index.html#/home")
            # 输入账号、密码
            self.button_rpa.enter_in_target(driver=self.driver, by=By.XPATH,
                                            value="//*[@placeholder='用户名/手机号/身份证']",
                                            text=self.g_dict["login_acc"])
            self.button_rpa.enter_in_target(driver=self.driver, by=By.XPATH,
                                            value="//*[@type='password']",
                                            text=self.g_dict["login_pw"])
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value="//*[@type='button']")
            # 等待系统登录完成
            self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value="//aside/div/div[2]/*")
            time.sleep(1)
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, value="//aside/div/div[2]/*")
            # 等待我的案件出现
            self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,
                                       value='//span/*[text()="我的案件"]')
            time.sleep(0.5)
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                         value='//span/*[text()="我的案件"]')
            # 等待数据加载完成
            self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value="//*[contains(text(),'粤')]")


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
                "pageSize": 1,
                "reqParam": {
                    "queryParam": [
                        {
                            "field": "zt",
                            "value": [
                                "处理中", "已完成", "异常"
                            ],
                            "sign": "<>"
                        }
                    ],
                    "updateMap": {
                        "zt": "处理中",

                    }
                }
            }
            put_json = {
                "zt": "",
                "id": "",
                "uniId": self.g_dict["table_id"]
            }
            action = ActionChains(driver=self.driver)

            is_err = False
            while True:
                err_str = ""
                rqs_data = self.other_rpa.post_request(
                    url="http://146.24.58.227:88/ymkj-api/uni/universal/pull",
                    payload=payload,
                    auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
                logging.info(rqs_data)
                data = rqs_data['data']['list']
                if len(data) == 0:  # 判断是否还有数据需要操作
                    break
                data = data[0]
                put_json['id'] = data['id']
                # 搜索案号
                an_hao = data['ah']
                sjyName = data['sjy']
                if not re.search("执保|执\\d+|执恢", an_hao):
                    # 回填状态
                    put_json['zt'] = "已完成"
                    rqs_data = self.other_rpa.put_request(
                        "http://146.24.58.227:88/ymkj-api/uni/universal/edit",
                        payload=put_json,
                        auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
                    continue
                logging.info("当前案号------------------" + an_hao)
                ah_list = re.findall("\\d+", an_hao)
                ah_num = ah_list[2]
                an_year = ah_list[0]
                print(an_year)
                print(ah_num)
                time.sleep(1)
                err_str = "进入总对总界面异常"
                # 输入年份
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value="//div[contains(@class,' fullWidth')]/div[2]")
                time.sleep(0.5)
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value=f"//li/*[contains(text(),'{an_year}')]")
                # 输入案号
                self.button_rpa.enter_in_target(driver=self.driver, by=By.XPATH,
                                                value="//div[contains(@class,'fullWidth')]/div[4]/input",
                                                text=ah_num)
                # 点击搜索
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value="//button/*[contains(text(),'查询')]")
                time.sleep(1.5)
                action.send_keys(Keys.ENTER).perform()
                # 等待数据搜索
                try:
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,
                                               value=f"//a[contains(text(),'{an_hao}')]")
                except Exception as e:
                    err_str = "搜索案件异常"
                    put_json['zt'] = "异常"
                    put_json['remark'] = err_str
                    rqs_data = self.other_rpa.put_request(
                        "http://146.24.58.227:88/ymkj-api/uni/universal/edit",
                        payload=put_json,
                        auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
                    continue
                # 点击案号
                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                             value=f"//a[contains(text(),'{an_hao}')]")
                time.sleep(5)

                try:
                    time.sleep(1)
                    self.logger.info(self.driver.window_handles)
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(1)
                    # 等待数据搜索
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,
                                               value="//*[text()='执行组织']/parent::*", timeout=30)
                    time.sleep(5)
                    # 点击 执行组织
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[text()='执行组织']/parent::*")
                    # 等待表格数据出现
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,
                                               value="//*[text()='角色']",
                                               timeout=60)
                    time.sleep(1.5)
                    # 点击 角色下拉框
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[@placeholder='请选择']//input")
                    time.sleep(1)
                    # 点击 书记员
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[@class='dict-option__content']//li/span[text()='书记员']")
                    logging.info(sjyName)
                    # 点击 组织成员下拉框
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[@class='fd-value show']")
                    time.sleep(1)
                    action.send_keys(sjyName).perform()
                    time.sleep(1)
                    # 点击 组织成员
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[@class='el-form-item__label']")
                    # 点击 完成
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[@class='el-button el-button--primary el-button--medium']")
                    time.sleep(2)
                    # 等待操作成功出现
                    # self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,
                    #                            value="//*[text()='操作成功！']",
                    #                            timeout=30)
                    # 回填状态
                    put_json['zt'] = "已完成"
                    put_json['remark'] = ""

                except Exception as e:
                    traceback.print_exc()
                    logging.error(f"{an_hao}执行异常{e}")
                    logging.info("-------------------------有异常：" + an_hao)
                    is_err = True

                    put_json['zt'] = "异常"
                    put_json['remark'] = err_str
                rqs_data = self.other_rpa.put_request(
                    "http://146.24.58.227:88/ymkj-api/uni/universal/edit",
                    payload=put_json,
                    auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
                logging.info(rqs_data['code'])
                logging.info(put_json)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                if rqs_data['code'] != 200:
                    print("回填状态异常")
                time.sleep(3.5)
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
            "name": "添加案件书记员",
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
            "loginPW": r"CYJun*123",
            "loginAcc": r"18000850505",
            "isPW":None,
            "end_time": "2025-11-25",
            "uniTable": [["QKUurXI8MghBQLNmvjrrK", "添加案件书记员"]],
            "保存路径": "D:/module/driver/86"
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
