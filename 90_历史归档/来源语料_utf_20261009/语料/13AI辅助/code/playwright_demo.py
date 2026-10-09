#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Playwright Demo 测试脚本

基于 Playwright 模板开发，自动测试稳定的网站功能。
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

# 确保输出支持utf-8，避免打印emoji时报错
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from aibot_rpa.core.flow_pw import FlowPw

class PlaywrightDemoTest(FlowPw):
    """Playwright Demo 测试脚本"""
    
    # 测试用例定义
    TEST_CASES = [
        {
            "id": "test_python_org_search",
            "name": "Python官网搜索测试",
            "description": "测试Python官网的搜索功能",
            "url": "https://www.python.org/",
            "steps": [
                {"action": "wait_for_selector", "selector": "#id-search-field", "timeout": 10000},
                {"action": "fill", "selector": "#id-search-field", "text": "asyncio"},
                {"action": "click", "selector": "#submit"},
                {"action": "wait_for_selector", "selector": ".list-recent-events", "timeout": 10000},
                {"action": "screenshot", "path": "screenshot/python_search_result.png"}
            ]
        },
        {
            "id": "test_github_homepage",
            "name": "GitHub首页测试",
            "description": "测试GitHub首页加载",
            "url": "https://github.com/",
            "steps": [
                {"action": "wait_for_selector", "selector": "header", "timeout": 10000},
                {"action": "screenshot", "path": "screenshot/github_homepage.png"}
            ]
        }
    ]
    
    def __init__(self, config=None):
        """初始化测试"""
        # 获取当前脚本所在目录，确保输出文件放在脚本所在目录下的 output 文件夹中
        self.output_dir = Path(__file__).parent / "output"
        
        # 测试配置
        test_config = {
            "browser_type": "chromium",
            "headless": False,
            "viewport": {"width": 1366, "height": 768},
            "record_video": False,
            "live_push": False,
            "live_push_mode": "tcp",
            "video_path": str(self.output_dir / "video" / f"test_video_{int(time.time())}.webm"),
            "max_retries": 0,  # 禁用全局重试，测试用例失败不应重跑整个套件
            "timeout": 30000,
            "taskId":'demo_task_001999',
            "test_report_path": str(self.output_dir / "report" / f"test_report_{int(time.time())}.json")
        }
        
        # 合并用户配置
        if config:
            test_config.update(config)
        
        # 调用父类初始化
        super().__init__(test_config)
        
        # 测试结果
        self.test_results = []
        self.test_start_time = None
        self.test_end_time = None
        
        print("✅ Playwright测试Demo初始化完成")
        print(f"📋 测试配置: {test_config}")
    
    async def run_business_async(self):
        """
        执行测试逻辑
        
        Returns:
            bool: 执行成功返回True，失败返回False
        """
        try:
            self.logger.info("=== 开始执行测试任务 ===")
            
            # 每次执行前清空之前的测试结果（防止重试时重复追加）
            self.test_results.clear()
            
            # 记录测试开始时间
            self.test_start_time = time.time()
            
            # 执行所有测试用例
            await self._run_all_test_cases()
            
            # 生成测试报告
            await self._generate_test_report()
            
            self.test_end_time = time.time()
            test_duration = self.test_end_time - self.test_start_time
            
            self.logger.info(f"=== 测试任务执行完成 (耗时: {test_duration:.2f}秒) ===")
            
            # 判断是否全部通过
            all_passed = all(r["status"] == "passed" for r in self.test_results)
            return all_passed
            
        except Exception as e:
            self.logger.error(f"测试任务执行失败: {e}")
            # 错误时截图
            try:
                if self.page:
                    error_path = str(self.output_dir / "screenshot" / "test_error_screenshot.png")
                    error_dir = Path(error_path).parent
                    if not error_dir.exists():
                        error_dir.mkdir(parents=True, exist_ok=True)
                    await self.page.screenshot(path=error_path)
                    self.logger.info(f"错误截图已保存: {error_path}")
            except:
                pass
            return False
    
    async def _run_all_test_cases(self):
        """执行所有测试用例"""
        self.logger.info(f"开始执行 {len(self.TEST_CASES)} 个测试用例")
        
        for test_case in self.TEST_CASES:
            await self._run_test_case(test_case)
    
    async def _run_test_case(self, test_case: Dict[str, Any]):
        """执行单个测试用例"""
        test_id = test_case["id"]
        test_name = test_case["name"]
        test_url = test_case["url"]
        test_steps = test_case["steps"]
        
        self.logger.info(f"\n=== 开始测试: {test_name} ({test_id}) ===")
        
        test_result = {
            "id": test_id,
            "name": test_name,
            "description": test_case["description"],
            "url": test_url,
            "start_time": time.time(),
            "end_time": None,
            "duration": None,
            "status": "running",
            "steps": [],
            "error": None,
            "screenshots": []
        }
        
        try:
            # 打开测试网址
            await self.page.goto(test_url, wait_until='domcontentloaded')
            self.logger.info(f"成功打开测试网址: {test_url}")
            
            # 执行测试步骤
            for step_idx, step in enumerate(test_steps):
                step_result = await self._execute_test_step(step, step_idx + 1)
                test_result["steps"].append(step_result)
                
                # 如果步骤失败，中断测试
                if step_result["status"] == "failed":
                    raise Exception(step_result["error"])
            
            # 测试通过
            test_result["status"] = "passed"
            self.logger.info(f"✅ 测试通过: {test_name}")
            
        except Exception as e:
            test_result["status"] = "failed"
            test_result["error"] = str(e)
            self.logger.error(f"❌ 测试失败: {test_name} - {e}")
            
        finally:
            # 记录测试结束时间
            test_result["end_time"] = time.time()
            test_result["duration"] = test_result["end_time"] - test_result["start_time"]
            
            # 添加到测试结果列表
            self.test_results.append(test_result)
            
            # 截图保存
            screenshot_path = str(self.output_dir / "screenshot" / f"test_{test_id}_result.png")
            try:
                # 确保截图目录存在
                screenshot_dir = Path(screenshot_path).parent
                if not screenshot_dir.exists():
                    screenshot_dir.mkdir(parents=True, exist_ok=True)
                    
                await self.page.screenshot(path=screenshot_path, full_page=False)
                test_result["screenshots"].append(screenshot_path)
                self.logger.info(f"测试截图已保存(当前视口): {screenshot_path}")
            except Exception as e:
                self.logger.warning(f"截图保存失败: {e}")
    
    async def _execute_test_step(self, step: Dict[str, Any], step_number: int):
        """执行单个测试步骤"""
        action = step["action"]
        step_result = {
            "step": step_number,
            "action": action,
            "status": "running",
            "error": None,
            "duration": None
        }
        
        start_time = time.time()
        
        try:
            self.logger.info(f"步骤 {step_number}: {action}")
            
            if action == "fill":
                selector = step["selector"]
                text = step["text"]
                await self.page.fill(selector, text)
                self.logger.info(f"填写内容: {text} 到 {selector}")
                
            elif action == "click":
                selector = step["selector"]
                await self.page.click(selector)
                self.logger.info(f"点击元素: {selector}")
                
            elif action == "wait_for_selector":
                selector = step["selector"]
                timeout = step.get("timeout", self.timeout)
                await self.page.wait_for_selector(selector, timeout=timeout)
                self.logger.info(f"等待元素出现: {selector}")
                
            elif action == "screenshot":
                path = step["path"]
                if not Path(path).is_absolute():
                    path = str(self.output_dir / path)
                # 确保截图目录存在
                screenshot_dir = Path(path).parent
                if not screenshot_dir.exists():
                    screenshot_dir.mkdir(parents=True, exist_ok=True)
                await self.page.screenshot(path=path)
                self.logger.info(f"截图保存: {path}")
                
            elif action == "goto":
                url = step["url"]
                await self.page.goto(url, wait_until='domcontentloaded')
                self.logger.info(f"导航到: {url}")
                
            elif action == "evaluate":
                script = step["script"]
                result = await self.page.evaluate(script)
                self.logger.info(f"执行脚本结果: {result}")
                
            else:
                raise Exception(f"不支持的操作: {action}")
            
            step_result["status"] = "passed"
            
        except Exception as e:
            step_result["status"] = "failed"
            step_result["error"] = str(e)
            self.logger.error(f"步骤执行失败: {e}")
            
        finally:
            step_result["duration"] = time.time() - start_time
        
        return step_result
    
    async def _generate_test_report(self):
        """生成测试报告"""
        self.logger.info("生成测试报告...")
        
        # 统计测试结果
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["status"] == "passed")
        failed_tests = sum(1 for r in self.test_results if r["status"] == "failed")
        
        test_duration = self.test_end_time - self.test_start_time if self.test_end_time else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "start_time": self.test_start_time,
                "end_time": self.test_end_time,
                "duration": test_duration
            },
            "test_cases": self.test_results,
            "environment": {
                "browser_type": self.browser_type,
                "headless": self.headless,
                "viewport": self.viewport,
                "record_video": self.config.get_config('record_video', False)
            }
        }
        
        # 保存报告
        report_path = self.config.get_config('test_report_path', str(self.output_dir / "report" / f"test_report_{int(time.time())}.json"))
        
        # 确保报告目录存在
        report_dir = Path(report_path).parent
        if not report_dir.exists():
            report_dir.mkdir(parents=True, exist_ok=True)
            
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"测试报告已保存: {report_path}")
        self._print_test_summary(report["summary"])
    
    def _print_test_summary(self, summary: Dict[str, Any]):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("📊 测试执行摘要")
        print("=" * 60)
        print(f"总测试数: {summary['total_tests']}")
        print(f"通过测试: {summary['passed_tests']}")
        print(f"失败测试: {summary['failed_tests']}")
        print(f"通过率: {summary['pass_rate']:.1f}%")
        print(f"总耗时: {summary['duration']:.2f}秒")
        print("=" * 60)

def main():
    """主函数"""
    print(">>> 开始执行Playwright Demo测试任务...")
    print("--- Playwright Demo ---")
    print("=" * 60)
    
    # 测试配置选项
    test_config = {
        "browser_type": "chromium",  # 可选: chromium, firefox, webkit
        "headless": False,  # 是否无头模式
        "record_video": False,  # 是否录制视频
        "live_push": False,  # 测试环境默认关闭实时推流
        "viewport": {"width": 1920, "height": 1080}  # 视口大小
    }
    
    try:
        # 创建并运行测试任务
        test_runner = PlaywrightDemoTest(test_config)
        success = test_runner.execute()
        
        if success:
            print("\n✅ 测试任务执行完成！")
            print("📋 请查看测试报告获取详细结果")
        else:
            print("\n❌ 测试任务执行失败！")
            print("📋 请查看日志文件获取详细信息")
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断执行")
    except Exception as e:
        print(f"\n💥 程序异常: {e}")
    
    print("=" * 60)
    print("🎯 测试任务结束")

if __name__ == "__main__":
    main()
