#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
豆包图片生成自动化 - 优化版

基于 Playwright 同步框架，自动处理豆包图片生成任务。
参考 playwright_demo.py 的代码结构和最佳实践。
"""

import sys
import os
import re
import time
import json
import datetime
import random
import traceback
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any

# 确保输出支持utf-8，避免打印emoji时报错
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 第三方库
import requests
from playwright.sync_api import sync_playwright, Page, BrowserContext
from playwright._impl._errors import TargetClosedError

# 自定义模块
from aibot_rpa.core.flow import BaseFlow
from aibot_rpa.utils.decorators import RetryDecorator
from aibot_rpa.config.manager import ConfigManager


class DoubaoImageGenerator(BaseFlow):
    """豆包图片生成自动化流程 - 优化版"""
    
    def __init__(self, **kwargs):
        """初始化流程"""
        super().__init__(**kwargs)
        self.config_dict = {}
        self.data = None
        self.curData = None
        self.page: Optional[Page] = None
        self.browser_manager = None
        self.playwright = None
        self.put_json = {
            "stateDbAa": "",
            "id": "",
            "uniId": ""
        }
        self.task_results = []
        self.task_start_time = None
        self.task_end_time = None
        
        print("✅ 豆包图片生成器初始化完成")
    
    def _execute(self):
        """
        执行核心业务逻辑
        
        Returns:
            bool: 执行成功返回True，失败返回False
        """
        try:
            self.logger.info("=== 开始执行豆包图片生成任务 ===")
            
            # 清空之前的结果
            self.task_results.clear()
            
            # 记录任务开始时间
            self.task_start_time = time.time()
            
            # 读取配置
            self.config_dict = self.config.get_dict_config()
            self.logger.info(f"配置加载完成: {self.config_dict}")
            
            # 查询待处理数据
            self.data = self.get_data(stateDbAa=None)
            if len(self.data) == 0:
                self.logger.info("没有待处理的数据，任务结束")
                return True
            
            # 初始化浏览器
            self.run_local_browser()
            
            # 处理所有数据
            self.process_all_tasks()
            
            # 记录任务结束时间
            self.task_end_time = time.time()
            task_duration = self.task_end_time - self.task_start_time
            
            self.logger.info(f"=== 任务执行完成 (耗时: {task_duration:.2f}秒) ===")
            
            # 判断是否全部成功
            all_success = all(r["status"] == "success" for r in self.task_results)
            return all_success
            
        except Exception as e:
            self.logger.error(f"任务执行失败: {e}")
            # 错误时截图
            try:
                if self.page:
                    error_path = str(Path(__file__).parent / "output" / "screenshot" / "error_screenshot.png")
                    error_dir = Path(error_path).parent
                    if not error_dir.exists():
                        error_dir.mkdir(parents=True, exist_ok=True)
                    self.page.screenshot(path=error_path)
                    self.logger.info(f"错误截图已保存: {error_path}")
            except:
                pass
            self.set_data(stateDbAa="处理异常")
            self.driver_quit()
            raise e
        finally:
            # 确保关闭浏览器
            self.driver_quit()
    
    def get_data(self, stateDbAa="处理中"):
        """
        获取待处理数据
        
        Args:
            stateDbAa: 状态筛选
            
        Returns:
            list: 数据列表
        """
        auth_code = self.config_dict["authcode"]
        table_id = self.config_dict["unitable"][0][0]
        
        query_param = []
        if stateDbAa is not None:
            query_param.append({
                "field": "stateDbAa",
                "value": ["处理中", "已完成", "处理异常", "等待超时"],
                "sign": "<>"
            })
        
        payload = {
            "uniId": table_id,
            "pageSize": 1,
            "reqParam": {
                "queryParam": query_param,
                "updateMap": {
                    "stateDbAa": stateDbAa if stateDbAa else "处理中",
                }
            }
        }
        
        self.put_json["uniId"] = table_id
        
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
        """
        回填数据状态
        
        Args:
            stateDbAa: 状态值
            
        Returns:
            dict: 响应数据
        """
        auth_code = self.config_dict["authcode"]
        self.put_json['stateDbAa'] = stateDbAa
        
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
    
    def process_all_tasks(self):
        """处理所有任务"""
        count = 0
        
        while True:
            self.data = self.get_data(stateDbAa="处理中")
            if len(self.data) == 0:
                self.logger.info("没有待处理的数据，处理完成")
                break
            
            count += 1
            if count % 10 == 1:
                self.switch_to_image_generation()
            
            for item in self.data:
                self.process_single_task(item)
            
            time.sleep(1)
    
    def switch_to_image_generation(self):
        """切换到图像生成页面"""
        try:
            self.page.click('div[title="图像生成"]', timeout=5000)
        except Exception:
            try:
                self.page.click("text=图像生成", timeout=5000)
            except Exception:
                pass
        self.page.wait_for_timeout(2000)
    
    def process_single_task(self, item: Dict[str, Any]):
        """处理单个任务"""
        task_result = {
            "id": item.get('id'),
            "prompt": item.get('prompt'),
            "start_time": time.time(),
            "end_time": None,
            "duration": None,
            "status": "processing",
            "error": None
        }
        
        self.curData = item
        self.put_json['id'] = self.curData['id']
        self.logger.info(f"开始处理任务: {self.curData}")
        
        max_retries = 2
        success = False
        
        for attempt in range(max_retries):
            try:
                self.process_prompt()
                task_result["status"] = "success"
                success = True
                break
            except TargetClosedError as e:
                self.logger.error(f"页面或浏览器已关闭，重试 {attempt+1}/{max_retries}: {e}")
                if attempt == max_retries - 1:
                    task_result["status"] = "failed"
                    task_result["error"] = str(e)
                    self.set_data(stateDbAa="处理异常")
                else:
                    self.driver_quit()
                    self.run_local_browser()
            except Exception as e:
                error_msg = str(e)
                self.logger.error(f"处理异常，重试 {attempt+1}/{max_retries}: {type(e).__name__}: {e}")
                
                if "Target page, context or browser has been closed" in error_msg or "has been closed" in error_msg:
                    self.logger.error("检测到页面或浏览器已关闭，尝试重启浏览器")
                    self.driver_quit()
                    self.run_local_browser()
                
                if "余额不足" in error_msg:
                    self.logger.error("检测到余额不足，停止处理")
                    task_result["status"] = "failed"
                    task_result["error"] = "余额不足"
                    self.set_data(stateDbAa="处理异常")
                    break
                
                if attempt == max_retries - 1:
                    task_result["status"] = "failed"
                    task_result["error"] = str(e)
                    self.set_data(stateDbAa="处理异常")
        
        if success:
            self.set_data(stateDbAa="已完成")
        
        task_result["end_time"] = time.time()
        task_result["duration"] = task_result["end_time"] - task_result["start_time"]
        self.task_results.append(task_result)
    
    def process_prompt(self):
        """
        处理图片生成
        
        使用 Playwright 实现豆包图片生成自动化：填写 prompt、点击生成。
        """
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
        
        # 填写 prompt
        try:
            container = page.query_selector(".container-wMk8bg")
            if container:
                # 先清空
                container.fill("")
                page.wait_for_timeout(500)
                # 填写内容
                full_prompt = self.curData["prompt"] + self.config.get_config("APPEND_PROMPT", "")
                container.fill(full_prompt)
            else:
                self.logger.warning("未找到输入框容器")
            page.wait_for_timeout(1000)
        except Exception as e:
            self.logger.error(f"填写 prompt 失败: {e}")
            raise e
        
        # 点击生成按钮
        try:
            # 再次检查弹窗
            credit_modal = page.query_selector(".creditInsufficientModalWrapper-IggTnn")
            if credit_modal:
                self.logger.error("点击生成前检测到余额不足弹窗")
                raise Exception("余额不足，无法生成图片")
            
            page.click("#flow-end-msg-send", timeout=10000)
            page.wait_for_timeout(2000)
        except Exception as e:
            if "Timeout" in str(e):
                self.logger.error("点击生成按钮超时，可能被弹窗拦截")
                raise Exception("点击生成按钮超时")
            self.logger.error(f"点击生成按钮失败: {e}")
            raise e
        
        # 等待生成结果
        completion_event = threading.Event()
        error_message = None
        
        def check_response(response):
            nonlocal error_message
            try:
                if "https://www.doubao.com/samantha/chat/completion" in response.url:
                    text = response.text()
                    if '"is_finish":true' in text:
                        if "无法生成" in text or "不符合" in text:
                            self.logger.error("检测到无法生成图片")
                            error_message = "抱歉，我无法生成你要求的图片。"
                        completion_event.set()
            except Exception as e:
                self.logger.error(f"检查响应失败: {e}")
                if not completion_event.is_set():
                    completion_event.set()
        
        page.on("response", check_response)
        
        try:
            finished = completion_event.wait(timeout=120)
            if not finished:
                self.logger.error("图片生成超时")
                raise Exception("图片生成超时")
            if error_message:
                raise Exception(error_message)
            self.logger.info("图片生成请求完成")
            page.wait_for_timeout(3000)
        finally:
            page.remove_listener("response", check_response)
    
    def get_browser_path(self):
        """获取浏览器路径"""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            return os.path.join(base_path, "ms-playwright", "chromium-1140", "chrome-win", "chrome.exe")
        else:
            return r"C:\Users\mo\AppData\Local\ms-playwright\chromium-1140\chrome-win\chrome.exe"
    
    def run_local_browser(self):
        """
        用 Playwright 启动浏览器，进入豆包图片生成页面。
        """
        try:
            self.playwright = sync_playwright().start()
            browser_path = self.get_browser_path()
            self.browser_manager = self.playwright.chromium.launch_persistent_context(
                self.config.get_config('USER_DATA_DIR'),
                headless=self.config.get_config('headless', False),
                executable_path=browser_path,
                args=['--start-maximized'],
            )
            self.page = self.browser_manager.pages[0] if self.browser_manager.pages else self.browser_manager.new_page()
            self.page.goto("https://www.doubao.com/chat/create-image", timeout=60000)
            self.page.wait_for_timeout(5000)
            
            self.run_business()
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            self.driver_quit()
    
    def run_business(self):
        """运行业务逻辑"""
        # 这个方法在 process_all_tasks 中已经处理
        pass
    
    def driver_quit(self):
        """关闭浏览器和清理资源"""
        if hasattr(self, 'browser_manager') and self.browser_manager:
            try:
                self.browser_manager.close()
            except:
                pass
        if hasattr(self, 'playwright') and self.playwright:
            try:
                self.playwright.stop()
            except:
                pass


def main():
    """主函数"""
    print(">>> 开始执行豆包图片生成任务...")
    print("--- 豆包图片生成器 ---")
    print("=" * 60)
    
    rpa = None
    rpa_flow = None
    
    try:
        # 初始化配置管理器
        config_manager = ConfigManager()
        
        # 处理命令行参数
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg.endswith('.json'):
                config_manager.load_json_file(arg)
            else:
                config_manager.load_json_string(arg)
        else:
            config_obj = {
                "headless": False,
                "USER_DATA_DIR": 'user_data_aa',
                "img_path": 'D:/imagination/guoke/weili/weili_hb.png',
                "APPEND_PROMPT": ' 量子级细节真实肉眼4D超清',
                "start_time": "2025-06-04",
                "authcode": "lmYXStbZEbJ2RrBf2ej0N",
                "log_path": "d:/rpa_profile/log/zRcouyi.img/zRcouyi.img_20250611102911865.log",
                "video_path": "d:/rpa_profile/video/zRcouyi.img/zRcouyi.img_20250611102911865.mp4",
                "name": "zRcouyi.img",
                "rpa_profile": "d:/rpa_profile",
                "unitable": [["X_4pM9f5G4FSZbF4KS2Mm", "zRcouyi.img"]]
            }
            config_manager.load_dict(config_obj)
        
        # 初始化RPA框架并执行流程
        from aibot_rpa import AibotRpa
        rpa = AibotRpa(config_manager=config_manager)
        rpa.logger.info(rpa.config.get_config())
        
        # 执行流程
        rpa_flow = rpa.run_flow(DoubaoImageGenerator)
        
        if rpa_flow:
            rpa.logger.info("豆包图片生成流程执行成功！")
            rpa.logger.info({"msg": "已完成"})
            print("\n✅ 任务执行完成！")
        else:
            rpa.logger.error("豆包图片生成流程执行失败！")
            rpa.logger.info({"error": "运行异常"})
            print("\n❌ 任务执行失败！")
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断执行")
    except Exception as e:
        traceback.print_exc()
        
        if rpa_flow:
            rpa.logger.error(f"程序执行异常: {e}", exc_info=True)
        return 1
    
    print("=" * 60)
    print("🎯 任务结束")
    return 0


if __name__ == "__main__":
    sys.exit(main())
