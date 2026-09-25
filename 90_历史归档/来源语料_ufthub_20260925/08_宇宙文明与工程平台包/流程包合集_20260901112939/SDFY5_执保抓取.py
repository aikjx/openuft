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
from aibot_common.getdata_rpa import GETDATA_RPA
import logging

from selenium.webdriver.common.action_chains import ActionChains
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import re
import shutil
import sys
import os
import time

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
                        "field": "sfzq",
                        "value": [
                            "处理中"
                        ],
                        "sign": "=",
                        "append": "or"
                    }, {
                        "field": "sfzq",
                        "value": [
                            "异常"
                        ],
                        "sign": "=",
                        "append": "or"
                    }
                ],
                "updateMap": {
                    "sfzq": "",

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
            self.g_dict["auth_code"] = config_dict["AuthCode"]
            print(self.g_dict["auth_code"])
            self.g_dict["table_id"] = config_dict["uniTable"][0][0]
            self.g_dict["dsr_table"] = config_dict["uniTable"][1][0]
            # self.g_dict["login_acc"] = "lijw0218"
            logging.info(config_dict["loginAcc"])
            logging.info(config_dict["isPW"])
            self.g_dict["login_acc"] = str(config_dict["loginAcc"])
            # self.g_dict["login_pw"] = "060218"
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

            obj_json = self.browser_rpa.open_browser(
                url="http://babg-appweb-pre.oss-cn-hangzhou-yzwsouth-d01-a.res.zgf.yzwsouth.com/babgpt/index.html#/home",
                executable_path=r"D:/module/driver/86/chromedriver.exe",
                browser_path=r"D:/app/360Chrome/Chrome/Application/360chrome.exe",
                download_dir=self.g_dict["ls_dir"],
                run_log=True,
            )
            self.driver = obj_json['driver']
            self.driver.maximize_window()
            action = ActionChains(driver=self.driver)

            time.sleep(0.5)

            # 登录一张网系统
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
            # try:
            #     # 等待数据加载完成
            #     self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value="//*[contains(text(),'粤')]")
            # except Exception as e:
            #     print("无数据")
            time.sleep(1)
            # 点击案件查询
            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                         value="//*[@class='el-tabs__nav-scroll']//*[text()='案件查询']")
            # 数据抓取
            # self.get_zb_data()

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
                            "field": "sfzq",
                            "value": [
                                "非执保", "已抓取"
                            ],
                            "sign": "<>"
                        }
                    ],
                    "updateMap": {
                        "sfzq": "处理中",

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
                data = rqs_data['data']['list']
                if len(data) == 0:  # 判断是否还有数据需要操作
                    break
                data = data[0]
                logging.info(data)
                put_json['id'] = data['id']
                an_hao = data['ah']
                if not re.search("执保", an_hao):
                    # 回填状态
                    put_json['zt'] = "非执保"
                    rqs_data = self.other_rpa.put_request(
                        "http://146.44.17.124:88/ymkj-api/uni/universal/edit",
                        payload=put_json,
                        auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
                    continue
                ah_list = re.findall("\\d+", an_hao)
                ah_num = ah_list[2]
                an_year = ah_list[0]
                try:
                    # 点击重置
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[text()='重置']")
                    # //*[@content='展开查询区']
                    zk_obj = self.driver.find_elements(By.XPATH,
                                                       "//*[@content='展开查询区']")
                    if len(zk_obj) > 0:
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                     value="//*[@content='展开查询区']")
                    # 选择年份
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[@placeholder='年度']")
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=-1,
                                                 value=f"//*[contains(text(),'{an_year}')]")
                    # 选择待字

                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[@placeholder='代字']")
                    time.sleep(1)
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[@class='tdh-select-case-number-btnSpread-left']//*[contains(text(),'执行案件')]")
                    time.sleep(1)
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value=f"//ul[@class='tdh-select-case-number-box']//*[contains(text(),'执保')]")
                    time.sleep(1)
                    # 输入案号
                    self.button_rpa.enter_in_target(driver=self.driver, by=By.XPATH,
                                                    value="//*[@placeholder='序号']",
                                                    text=ah_num)
                    time.sleep(1)
                    cxObj = self.driver.find_element(By.XPATH, "//*[text()='查询']")
                    action.click(cxObj).perform()
                    # # 点击搜索
                    # self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=-1,
                    #                              value=f"//*[text()='查询']")
                    # time.sleep(3)
                    # self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=-1,
                    #                              value=f"//*[text()='查询']")
                    # 等待案号
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value=f"//*[text()='{an_hao}']")
                    # 点击案号
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=-1,
                                                 value=f"//*[text()='{an_hao}']")
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value=f"//*[text()='{an_hao}']")
                    time.sleep(1.5)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    # 点击  案件信息
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//*[contains(text(),'案件信息')]")
                    time.sleep(1.5)
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH,
                                               value=f"//iframe[@class='async-iframe']")
                    # 切换iframe
                    aj_info_iframe = self.driver.find_element(By.XPATH,
                                                              "//iframe[@class='async-iframe']")
                    self.driver.switch_to.frame(aj_info_iframe)
                    # 等待元素
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value=f"//*[text()='收案登记']")
                    time.sleep(5)
                    # 获取收案途径
                    satj = self.driver.find_element(By.XPATH,
                                                    "//*[text()='收案途径']/parent::*/parent::*/following-sibling::li[1]//input/following-sibling::*").text
                    # 获取保全金额
                    bdeEle = self.driver.find_element(By.XPATH,
                                                    "//*[text()='保全金额']/parent::*/parent::*/following-sibling::li[1]//input/following-sibling::*")
                    bde = bdeEle.get_attribute("value")
                    # 获取依据文号
                    print(satj)
                    yjwhEle = self.driver.find_element(By.XPATH,
                                                    "//*[@class='fd-wswh-content']//input")
                    yjwh = yjwhEle.get_attribute("value")
                    logging.info(yjwh)
                    # 获取依据主文
                    yjzwEle = self.driver.find_element(By.XPATH,
                                                    "//*[@class='aty-textarea']")
                    yjzw = yjzwEle.get_attribute("value")
                    # 点击当事人
                    self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                 value="//span[text()='当事人信息']")
                    self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value=f"//*[text()='联系方式/现住址']")
                    # 定位表格table
                    dsr_obj_list = self.driver.find_element(By.XPATH,
                                                            "(//*[contains(@class,'aty-table__body-wrapper is-scrolling-none')]//tbody)[2]")
                    dsr_list = self.get_data_rpa.get_table_data(table_obj=dsr_obj_list)
                    is_fr = False
                    send_dict = {}
                    nameAndZjhm = {}  # 映射名字与证件号码
                    for dsrIdx, dsrData in enumerate(dsr_list):
                        dsrName = dsrData[2]
                        ssdw = dsrName.split("\n")[0]
                        dsrName = dsrName.split("\n")[1]
                        dsrZjhm = dsrData[4].split("：")[1]
                        nameAndZjhm[dsrName] = dsrZjhm
                        if not send_dict.get(dsrZjhm):
                            send_dict[dsrZjhm] = {}
                        # lxfs = re.search("\d+", dsrData[5])
                        # lxfs = lxfs.group()  # 后续记得加密上传 电话号码
                        # if len(lxfs) < 8:
                        #     lxfs = ""
                        dz = dsrData[5].split("\n")
                        if len(dz) > 1:
                            dz = dz[1]
                        else:
                            dz = dz[0]
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=dsrIdx + 1, value="//*[text()='查看']")
                        if re.match("统一", dsrData[4]) or re.match("组织", dsrData[4]):
                            is_fr = True
                            time.sleep(1.5)
                            # 获取注册地
                            zcdEle = self.driver.find_element(By.XPATH,
                                                           "//*[text()='注册地']/parent::*/following-sibling::*//input")
                            zcd = zcdEle.get_attribute("value")
                            # 获取统一社会信用代码证
                            frzj_el = self.driver.find_element(By.XPATH,
                                                              "//*[text()='统一社会信用代码证']/parent::*/parent::*/parent::*/following-sibling::*/following-sibling::*//input")
                            frzj = frzj_el.get_attribute("value")
                            send_dict[dsrZjhm]["zjhm"] = frzj
                            send_dict[dsrZjhm]["dsrlx"] = '法人'
                        else:
                            # 获取注册地
                            zcdEle = self.driver.find_element(By.XPATH,
                                                              "//*[text()='户籍所在地']/parent::*/following-sibling::*//input")
                            zcd = zcdEle.get_attribute("value")
                            send_dict[dsrZjhm]["zjhm"] = dsrZjhm
                            send_dict[dsrZjhm]["dsrlx"] = '自然人'

                        send_dict[dsrZjhm]["zbh"] = an_hao
                        send_dict[dsrZjhm]["yjwh"] = yjwh
                        send_dict[dsrZjhm]["yjzw"] = yjzw
                        send_dict[dsrZjhm]["bde"] = bde
                        send_dict[dsrZjhm]["satj"] = satj
                        send_dict[dsrZjhm]["mc"] = dsrName
                        send_dict[dsrZjhm]["ssdw"] = ssdw
                        send_dict[dsrZjhm]["dz"] = dz
                        # send_dict[dsrZjhm]["lxfs"] = lxfs
                        send_dict[dsrZjhm]["hjzcd"] = zcd
                    if is_fr:
                        try:
                            # 抓取相关当事人信息
                            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                         value="//span[text()='相关人信息']")
                            # 等待数据加载
                            self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value=f"//*[text()='证件信息']")
                            # 定位表格table
                            xgr_obj_list = self.driver.find_element(By.XPATH,
                                                                    "(//*[contains(@class,'aty-table__body-wrapper is-scrolling-none')])[2]")
                            xgr_list = self.get_data_rpa.get_table_data(table_obj=xgr_obj_list)
                            for xgrIdx, xgrData in enumerate(xgr_list):
                                fdDbrName = xgrData[2]
                                fdDbrName = fdDbrName.split("\n")[1]
                                fdDbrZjhm = re.search(r"[1-9]\d{16}[\dXx]", xgrData[3])
                                logging.info(fdDbrZjhm)
                                if fdDbrZjhm is not None:
                                    fdDbrZjhm = fdDbrZjhm.group()  # 后续记得加密上传 证件号码
                                else:
                                    fdDbrZjhm = ''
                                self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=xgrIdx + 1,
                                                             value="//*[text()='查看']")
                                time.sleep(1.5)
                                # 获取关联当事人
                                gldsr = self.driver.find_element(By.XPATH,
                                                                 "//*[text()='关联当事人']/parent::*/following-sibling::*//input/following-sibling::span").text
                                dsrZjhm = nameAndZjhm[gldsr]
                                send_dict[dsrZjhm]["fr"] = fdDbrName
                        except:
                            pass

                    try:
                        # 点击代理人信息
                        self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH,
                                                     value="//span[text()='代理人信息']")
                        # 等待数据加载
                        self.page_rpa.wait_element(driver=self.driver, by=By.XPATH, value=f"//*[text()='代理种类/姓名']")
                        # 定位表格table
                        dlr_obj_list = self.driver.find_element(By.XPATH,
                                                                "(//*[contains(@class,'aty-table__body-wrapper is-scrolling-none')]//tbody)[2]")
                        dlr_list = self.get_data_rpa.get_table_data(table_obj=dlr_obj_list)
                        for dlrIdx, dlrData in enumerate(dlr_list):
                            dlrName = dlrData[2]
                            dlDsrName = dlrData[3]
                            dlrLxfs = dlrData[4].split("\n")[0]
                            dlrLsmc = dlrData[4].split("\n")[1]
                            # dlrZjhm = dlrZjhm.group()  # 后续记得加密上传 证件号码
                            self.mouse_rpa.click_element(driver=self.driver, by=By.XPATH, idx=dlrIdx + 1,
                                                         value="//*[text()='查看']")
                            time.sleep(1.5)
                            # 获取代理人身份证
                            dlrZjhmEle = self.driver.find_element(By.XPATH,
                                                             "//*[text()='证件号码']/parent::*/following-sibling::*//input")
                            dlrZjhm = dlrZjhmEle.get_attribute("value")
                            # 获取律师执业证号
                            dlrZyzhEle = self.driver.find_element(By.XPATH,
                                                             "//*[text()='律师执业证号']/parent::*/following-sibling::*//input")
                            dlrZyzh = dlrZyzhEle.get_attribute("value")
                            dsrZjhm = nameAndZjhm[dlDsrName]
                            send_dict[dsrZjhm]["dlr"] = dlrName
                            send_dict[dsrZjhm]["dlrzjhm"] = dlrZjhm
                            send_dict[dsrZjhm]["dldsr"] = dlDsrName
                            send_dict[dsrZjhm]["dlrlxfs"] = dlrLxfs
                            send_dict[dsrZjhm]["dlrlsmc"] = dlrLsmc
                            send_dict[dsrZjhm]["dlrzyzh"] = dlrZyzh
                    except:
                        pass
                    # 写入当事人信息到表格
                    for key, value in send_dict.items():
                        logging.info(value)
                        value["uniId"] = self.g_dict["dsr_table"]
                        rqs_data = self.other_rpa.post_request(
                            url="http://146.24.58.227:88/ymkj-api/uni/universal/add",
                            payload=value,
                            auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
                    # 回填状态
                    put_json['sfzq'] = "已抓取"
                    put_json['yj'] = yjwh
                    put_json['remark'] = ""

                except Exception as e:
                    traceback.print_exc()
                    logging.error(f"{an_hao}执行异常{e}")
                    logging.info("-------------------------有异常：" + an_hao)
                    put_json['sfzq'] = "异常"
                    put_json['remark'] = err_str
                rqs_data = self.other_rpa.put_request(
                    url="http://146.24.58.227:88/ymkj-api/uni/universal/edit",
                    payload=put_json,
                    auth_token='AuthCode {}'.format(self.g_dict["auth_code"]))
                windowNum = self.driver.window_handles
                if len(windowNum) > 1:
                    while len(windowNum) > 1:
                        self.driver.close()
                        windowNum = self.driver.window_handles
                self.driver.switch_to.window(windowNum[0])
                if rqs_data['code'] != 200:
                    print("回填状态异常")
                time.sleep(3.5)

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
            "name": "执保抓取",
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
            "AuthCode": "NGqw9Ik0xiKQL0VpXZJ2o",
            # "loginPW": r"tata1234#",
            # "loginAcc": r"18000850370",
            "loginPW": r"kiwi.123",
            "loginAcc": r"15113721138",
            "isPW": None,
            "end_time": "2025-11-25",
            "uniTable": [["NrosOw_GmtBHP5V13AnK4", "执保抓取"],["N5MTtHFPOUiGcgQ4epSY2","当事人信息"]],
            # "保存路径": r"\\146.24.58.227\机器人相关"
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
