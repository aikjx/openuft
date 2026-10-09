# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import json
import datetime
import random
import traceback
import threading

from tkinter import filedialog, messagebox

# 第三方库
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from playwright.sync_api import sync_playwright
from playwright._impl._errors import TargetClosedError

# 自定义模块
from aibot_rpa import AibotRpa
from aibot_rpa.core.flow import BaseFlow
from aibot_rpa.utils.decorators import RetryDecorator
from aibot_rpa.config.manager import ConfigManager


# 步骤1：定义自定义流程
class MyFullDemoFlow(BaseFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = None
        self.browser_manager = None
        self.retry_decorator = RetryDecorator(self.config.get_all_config())
        # self.public_rpa = Aibotc()  # 移除
        self.config_dict = {}
        self.data = None
        self.page = None
        self.curData = None
        self.put_json = {
            "stateDbAa": "",
            "id": "",
            "uniId": ""
        }

    # 使用实例方法装饰器
    @property
    def execute_with_retry(self):
        return self.retry_decorator.retry(max_retries=0, delay=2)(self._execute)

    def get_data(self, stateDbAa="处理中"):
        auth_code = self.config_dict["authcode"]
        table_id = self.config_dict["unitable"][0][0]
        payload = {
            "uniId": table_id,
            "pageSize": 1,
            "reqParam": {
                "queryParam": [
                    {
                        "field": "stateDbAa",
                        "value": [
                            "处理中", "已完成", "处理异常", "等待超时"
                        ],
                        "sign": "<>"
                    }
                ],
                "updateMap": {
                    "stateDbAa": stateDbAa,
                }
            }
        }
        self.put_json["uniId"] = table_id
        # 使用requests发送POST请求
        try:
            resp = requests.post(
                url="http://localhost:38080/uni/universal/pull",
                json=payload,
                headers={"Authorization": f"AuthCode {auth_code}"}
            )
            resp.raise_for_status()
            rqs_data = resp.json()
            _data = rqs_data['data']['list']
            return _data
        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"获取数据失败: {e}")
            return []

    def set_data(self, stateDbAa="已完成"):
        auth_code = self.config_dict["authcode"]
        self.put_json['stateDbAa'] = stateDbAa
        # 使用requests发送PUT请求
        try:
            resp = requests.put(
                url="http://localhost:38080/uni/universal/edit",
                json=self.put_json,
                headers={"Authorization": f"AuthCode {auth_code}"}
            )
            resp.raise_for_status()
            rqs_data = resp.json()
            return rqs_data
        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"回填状态失败: {e}")
            return {"code": -1}

    def _execute(self):
        try:
            # 使用配置字典 读取参数
            self.config_dict = self.config.get_dict_config()
            print(self.config_dict)
            auth_code = self.config_dict["authcode"]
            print(auth_code)
            table_id = self.config_dict["unitable"][0][0]
            print(table_id)

            # ---- 先查询是否有待运行的数据 ----
            self.data = self.get_data(stateDbAa=None)
            if len(self.data) == 0:
                self.logger.info("没有数据，处理完成")
                return True

            # 初始化浏览器和页面（必须在run_business前调用，确保self.page已初始化）
            self.run_local_browser()

            self.logger.info("流程执行完毕")
            self.driver_quit()
            return True
        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"流程执行异常: {str(e)}")
            self.set_data(stateDbAa="处理异常")
            self.driver_quit()
            raise e
        finally:
            # 确保停止录制
            if self.browser_manager:
                try:
                    
                    self.driver_quit()
                except Exception as e:
                    traceback.print_exc()
                    self.logger.error(f"停止录制失败: {e}")

    def run_business(self):
        # 运行业务逻辑
        count = 0  # 新增计数器

        while True:
            self.data = self.get_data(stateDbAa="处理中")
            if len(self.data) == 0:
                self.logger.info("没有数据，处理完成")
                break

            count += 1
            if count % 10 == 1:  # 或 count % 10 == 0，看你需求
                try:
                    # 优先用 title 属性定位
                    self.page.click('div[title="图像生成"]', timeout=5000)
                except Exception:
                    try:
                        # 退而求其次用文本定位
                        self.page.click("text=图像生成", timeout=5000)
                    except Exception:
                        pass  # 有时页面结构不同，忽略
                self.page.wait_for_timeout(2000)

            for item in self.data:
                self.curData = item
                self.put_json['id'] = self.curData['id']
                self.logger.info(f"开始处理数据: {self.curData}")
                # 处理业务逻辑
                max_retries = 2

                for attempt in range(max_retries):
                    try:
                        self.process_prompt()
                        # 检查是否已完成
                        if self.curData.get('stateDbAa') == '已完成':
                            break
                    except TargetClosedError as e:
                        self.logger.error(f"页面或浏览器已关闭，重试 {attempt+1}/{max_retries}: {e}")
                        if attempt == max_retries - 1:
                            self.logger.error("重试超出最大次数，标记为处理异常")
                            self.set_data(stateDbAa="处理异常")
                            break
                    except Exception as e:
                        error_msg = str(e)
                        self.logger.error(f"处理异常，重试 {attempt+1}/{max_retries}: {type(e).__name__}: {e}")
                        # 检查是否是页面/浏览器关闭
                        if "Target page, context or browser has been closed" in error_msg or "has been closed" in error_msg:
                            self.logger.error("检测到页面或浏览器已关闭，尝试重启浏览器")
                            self.driver_quit()
                            self.run_local_browser()  # 重新打开浏览器和页面
                            if attempt == max_retries - 1:
                                self.logger.error("重试超出最大次数，标记为处理异常")
                                self.set_data(stateDbAa="处理异常")
                                break
                        elif "余额不足" in error_msg or "Timeout" in error_msg:
                            self.logger.error(f"检测到余额不足或超时异常，重试 {attempt+1}/{max_retries}: {e}")
                            if attempt == max_retries - 1:
                                self.logger.error("重试超出最大次数，标记为处理异常")
                                self.set_data(stateDbAa="处理异常")
                                break
                        else:
                            self.logger.error(f"其他处理异常，重试 {attempt+1}/{max_retries}: {e}")
                            if attempt == max_retries - 1:
                                self.logger.error("重试超出最大次数，标记为处理异常")
                                self.set_data(stateDbAa="处理异常")
                                break
                # 回填状态 已完成
                rqs_data = self.set_data()
                self.logger.info(rqs_data)
                print(rqs_data['code'])
                if rqs_data['code'] != 200:
                    print("回填状态异常")
                self.data = None
                time.sleep(1)

        #  没有数据时会自动退出
        pass

    # 动漫风格
    # APPEND_PROMPT = ' 4k, no text. --niji 6 --aspect 9:16 --stylize 401 --quality 1 --chaos 0'

    def get_browser_path(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            return os.path.join(base_path, "ms-playwright", "chromium-1140", "chrome-win", "chrome.exe")
        else:
            return r"C:\Users\mo\AppData\Local\ms-playwright\chromium-1140\chrome-win\chrome.exe"

    def process_prompt(self):
        """
        用 Playwright 实现豆包图片生成自动化：上传图片、填写 prompt、点击生成。
        """
        try:
            page = self.page
            
            # 检查是否有余额不足弹窗
            try:
                credit_modal = page.query_selector(".creditInsufficientModalWrapper-IggTnn")
                if credit_modal:
                    self.logger.error("检测到余额不足弹窗，无法继续操作")
                    raise Exception("余额不足，无法生成图片")
            except Exception as e:
                if "余额不足" in str(e):
                    raise e
                pass  # 其他异常忽略
            

                
            # 2. 上传图片
            # try:
            #     page.locator('input[type="file"]').set_input_files(self.config.get_config("img_path"))
            #     page.wait_for_timeout(12000)
            # except Exception as e:
            #     print("图片上传失败", e)
                
            # 3. 填写 prompt
            try:
                container = page.query_selector(".container-wMk8bg")
                if container and container.is_editable():
                    container.fill(self.curData["prompt"] + self.config.get_config("APPEND_PROMPT"))
                else:
                    # 兼容 contentEditable
                    page.evaluate(
                        "if(arguments[0].contentEditable === 'true'){arguments[0].innerText = arguments[1]}",
                        container, self.curData["prompt"] + self.config.get_config("APPEND_PROMPT")
                    )
                page.wait_for_timeout(1000)
            except Exception as e:
                print("填写 prompt 失败", e)
                
            # 4. 点击生成按钮
            try:
                # 再次检查弹窗
                credit_modal = page.query_selector(".creditInsufficientModalWrapper-IggTnn")
                if credit_modal:
                    self.logger.error("点击生成前检测到余额不足弹窗")
                    raise Exception("余额不足，无法生成图片")
                    
                page.click("#flow-end-msg-send", timeout=10000)  # 减少超时时间
                page.wait_for_timeout(2000)
            except Exception as e:
                if "Timeout" in str(e):
                    self.logger.error("点击生成按钮超时，可能被弹窗拦截")
                    raise Exception("点击生成按钮超时")
                print("点击生成按钮失败", e)
                
            # 5. 等待生成结果，通过监听网络请求判断是否完成
            completion_event = threading.Event()
            error_message = None

            def check_response(response):
                print(f"[DEBUG] response: {response}")
                nonlocal error_message
                try:
                    print(f"[DEBUG] response.url: {response.url}")
                    if "https://www.doubao.com/samantha/chat/completion" in response.url:
                        text = response.text()
                        print(f"[DEBUG] response.url: {response.url}, text: {text[:200]}")
                        if '"is_finish":true' in text:
                            if "无法生成" in text or "不符合" in text:
                                self.logger.error("检测到无法生成图片，10秒后自动跳过")
                                error_message = "抱歉，我无法生成你要求的图片。"
                                time.sleep(10)
                            completion_event.set()
                except Exception as e:
                    print(f"[DEBUG] check_response error: {e}")
                    if not completion_event.is_set():
                        completion_event.set()

            page.on("response", check_response)
            page.wait_for_timeout(60000)
            try:
                finished = completion_event.wait(timeout=60)
                if not finished:
                    self.logger.error("图片生成超时，未检测到完成信号")
                    raise Exception("图片生成超时")
                if error_message:
                    raise Exception(error_message)
                self.logger.info("图片生成请求完成。")
                page.wait_for_timeout(3000)
            finally:
                try:
                    page.remove_listener("response", check_response)
                except Exception as e:
                    print(f"[DEBUG] remove_listener error: {e}")
            
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred during prompt processing: {e}")
            raise e  # 重新抛出异常，让外层重试机制捕获

    def run_local_browser(self):
        """
        用 Playwright 启动浏览器，进入豆包图片生成页面。
        """
        try:
            with sync_playwright() as playwright:
                browser_path = self.get_browser_path()
                self.browser_manager = playwright.chromium.launch_persistent_context(
                    self.config.get_config('USER_DATA_DIR'),
                    headless=self.config.get_config('headless'),
                    executable_path=browser_path,
                    args=['--start-maximized'],
                )
                self.page = self.browser_manager.pages[0] if self.browser_manager.pages else self.browser_manager.new_page()
                self.page.goto("https://www.doubao.com/chat/create-image", timeout=60000)
                self.page.wait_for_timeout(5000)

                


                self.run_business()
                self.driver_quit()
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            self.driver_quit()

    def execute(self):
        # 调用带重试的方法
        try:
            return self.execute_with_retry()
        finally:
            self.driver_quit()

    def driver_quit(self):
        if hasattr(self, 'browser_manager') and self.browser_manager:
            try:
                self.browser_manager.close()
            except:
                pass
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.quit()
            except:
                pass


def main():
    rpa = None
    rpa_flow = None
    try:

        # 初始化配置管理器
        config_manager = ConfigManager()

        # 处理命令行参数
        if len(sys.argv) > 1:
            # 检查是否是JSON字符串还是配置文件路径
            arg = sys.argv[1]
            if arg.endswith('.json'):
                # 是配置文件路径
                config_manager.load_json_file(arg)
            else:
                # 是JSON字符串
                config_manager.load_json_string(arg)
        else:
            config_obj = {
                "headless": False,
                # "headless": True,
                # 存储浏览器上下文的目录 - 豆包专用
                "USER_DATA_DIR": 'user_data_aa',
                "img_path": 'D:/imagination/guoke/weili/weili_hb.png',
                # 真事风格
                # "APPEND_PROMPT": ' 4k, no text --version 6.1 --aspect 3:4 --stylize 400 --quality 1 --chaos 0 --iw 1.6',
                "APPEND_PROMPT": ' 量子级细节真实肉眼4D超清',
                "start_time": "2025-06-04", "authcode": "lmYXStbZEbJ2RrBf2ej0N",
                "log_path": "d:/rpa_profile/log/zRcouyi.img/zRcouyi.img_20250611102911865.log",
                "video_path": "d:/rpa_profile/video/zRcouyi.img/zRcouyi.img_20250611102911865.mp4",
                "name": "zRcouyi.img", "rpa_profile": "d:/rpa_profile",
                "unitable": [["X_4pM9f5G4FSZbF4KS2Mm", "zRcouyi.img"]]}

            config_manager.load_dict(config_obj)
        # 初始化RPA框架并执行流程
        rpa = AibotRpa(config_manager=config_manager)
        rpa.logger.info(rpa.config.get_config())
        # 执行流程 - 不再重复传递config
        rpa_flow = rpa.run_flow(MyFullDemoFlow)

        if rpa_flow:
            rpa.logger.info("完整演示流程执行成功！")
            rpa.logger.info({
                "msg": "已完成"
            })
        else:
            rpa.logger.error("完整演示流程执行失败！")
            rpa.logger.info({
                "error": f"运行异常"
            })
    except Exception as e:
        traceback.print_exc()

        if rpa_flow:
            rpa.logger.error(f"程序执行异常: {e}", exc_info=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
