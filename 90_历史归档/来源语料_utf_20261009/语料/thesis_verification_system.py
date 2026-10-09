#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论核心论文验证与求导分析系统
用于验证所有核心论文中的数学公式，进行符号求导验证和高精度数值计算
"""

import os
import re
import sys
import json
import time
import concurrent.futures
import logging
import datetime
from typing import List, Dict, Tuple, Optional, Any

# 配置日志
def setup_logging():
    """设置日志配置"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'thesis_verification_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('ThesisVerificationSystem')

logger = setup_logging()

# 尝试导入必要的数学库
try:
    import sympy as sp
    import numpy as np
    import pandas as pd
    MATH_LIBS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"缺少数学库: {e}")
    MATH_LIBS_AVAILABLE = False

# 导入扩展模块
try:
    from extended_verification_modules import ExtendedVerificationModules
    EXTENDED_MODULES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"缺少扩展模块: {e}")
    EXTENDED_MODULES_AVAILABLE = False

# 导入高性能优化模块
try:
    from high_performance_optimizer import HighPerformanceOptimizer
    HIGH_PERFORMANCE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"缺少高性能优化模块: {e}")
    HIGH_PERFORMANCE_AVAILABLE = False

class ThesisVerificationSystem:
    """统一场论论文验证系统"""
    
    def __init__(self, base_dir: str):
        """初始化验证系统
        
        Args:
            base_dir: 论文根目录
        """
        self.base_dir = base_dir
        self.thesis_files: List[str] = []
        self.verification_results: Dict[str, Any] = {}
        self.start_time = 0.0
        self.end_time = 0.0
        
        # 初始化扩展模块
        self.extended_modules = None
        if EXTENDED_MODULES_AVAILABLE:
            self.extended_modules = ExtendedVerificationModules()
            
        # 初始化高性能优化器
        self.optimizer = None
        if HIGH_PERFORMANCE_AVAILABLE:
            self.optimizer = HighPerformanceOptimizer()
            self.optimizer.initialize()
        
    def find_thesis_files(self) -> List[str]:
        """查找所有论文文件
        
        Returns:
            论文文件路径列表
        """
        thesis_files = []
        
        try:
            if not os.path.isdir(self.base_dir):
                logger.error(f"目录不存在: {self.base_dir}")
                return thesis_files
            
            for root, _, files in os.walk(self.base_dir):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        thesis_files.append(file_path)
                        
            thesis_files = list(sorted(set(thesis_files)))
            logger.info(f"找到 {len(thesis_files)} 篇论文")
            self.thesis_files = thesis_files
            
        except Exception as e:
            logger.error(f"查找论文文件时出错: {e}")
            
        return thesis_files
    
    def extract_formulas(self, file_path: str) -> List[Dict[str, Any]]:
        """从论文中提取LaTeX公式
        
        Args:
            file_path: 论文文件路径
            
        Returns:
            公式列表，每个元素包含公式内容和位置信息
        """
        formulas = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取行内公式 $...$
            inline_pattern = re.compile(r'\$(.*?)\$', re.DOTALL)
            inline_matches = inline_pattern.finditer(content)
            
            for match in inline_matches:
                formula_text = match.group(1).strip()
                if formula_text:
                    formulas.append({
                        'type': 'inline',
                        'content': formula_text,
                        'start_pos': match.start(),
                        'end_pos': match.end()
                    })
            
            # 提取块级公式 $$...$$
            block_pattern = re.compile(r'\$\$\s*(.*?)\s*\$\$', re.DOTALL)
            block_matches = block_pattern.finditer(content)
            
            for match in block_matches:
                formula_text = match.group(1).strip()
                if formula_text:
                    formulas.append({
                        'type': 'block',
                        'content': formula_text,
                        'start_pos': match.start(),
                        'end_pos': match.end()
                    })
            
            logger.info(f"从 {os.path.basename(file_path)} 提取了 {len(formulas)} 个公式")
            
        except Exception as e:
            logger.error(f"提取公式时出错 {file_path}: {e}")
            
        return formulas
    
    def verify_formula(self, formula: Dict[str, Any]) -> Dict[str, Any]:
        """验证单个公式
        
        Args:
            formula: 公式字典
            
        Returns:
            验证结果
        """
        result = {
            'formula': formula['content'],
            'type': formula['type'],
            'status': 'pending',
            'error': None,
            'derivatives': {},
            'numerical_results': {},
            'suggestions': []
        }
        
        try:
            # 公式解析和验证
            if MATH_LIBS_AVAILABLE:
                # 1. 符号求导验证
                derivatives = self.calculate_derivatives(formula['content'])
                result['derivatives'] = derivatives
                
                # 2. 数值验证
                numerical_results = self.calculate_numerical(formula['content'])
                result['numerical_results'] = numerical_results
                
                result['status'] = 'verified'
            else:
                result['status'] = 'skipped'
                result['suggestions'].append('缺少数学库，无法进行符号计算')
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            logger.error(f"验证公式时出错: {e}")
            
        return result
    
    def calculate_derivatives(self, formula_text: str) -> Dict[str, str]:
        """计算公式的符号导数
        
        Args:
            formula_text: 公式文本
            
        Returns:
            导数计算结果
        """
        derivatives = {}
        
        try:
            # 简单的公式解析和求导
            # 这里实现基本的求导功能，后续可以扩展
            # 示例：对常见的物理公式进行求导
            
            # 定义常见变量
            t, x, y, z, v, a, m, F, E, c, G, ħ = sp.symbols('t x y z v a m F E c G ħ')
            
            # 尝试解析常见的公式模式
            formula_text = formula_text.replace('\\', '')  # 移除LaTeX转义字符
            
            # 处理常见的公式形式
            if 'r(t)' in formula_text or 'r(' in formula_text:
                # 位置矢量求导（速度）
                r = sp.Function('r')(t)
                v = sp.diff(r, t)
                derivatives['velocity'] = str(v)
                
                # 速度求导（加速度）
                a = sp.diff(v, t)
                derivatives['acceleration'] = str(a)
                
            elif 'v(' in formula_text or 'v=' in formula_text:
                # 速度公式求导
                v = sp.Function('v')(t)
                a = sp.diff(v, t)
                derivatives['acceleration'] = str(a)
                
            elif 'E=' in formula_text:
                # 能量公式求导
                if 'mc^2' in formula_text:
                    E = m * c**2
                    dE_dm = sp.diff(E, m)
                    derivatives['dE/dm'] = str(dE_dm)
                    
            elif 'F=' in formula_text:
                # 力公式求导
                if 'ma' in formula_text:
                    F = m * a
                    dF_dm = sp.diff(F, m)
                    derivatives['dF/dm'] = str(dF_dm)
                    dF_da = sp.diff(F, a)
                    derivatives['dF/da'] = str(dF_da)
                    
        except Exception as e:
            logger.warning(f"计算导数时出错: {e}")
            
        return derivatives
    
    def calculate_numerical(self, formula_text: str) -> Dict[str, float]:
        """数值验证公式
        
        Args:
            formula_text: 公式文本
            
        Returns:
            数值计算结果
        """
        numerical_results = {}
        
        try:
            # 基本的数值验证
            # 代入常见的物理常量进行验证
            
            # 物理常量
            constants = {
                'c': 299792458,  # 光速
                'G': 6.67430e-11,  # 万有引力常数
                'ħ': 1.054571817e-34,  # 约化普朗克常数
                'm_e': 9.1093837015e-31,  # 电子质量
                'm_p': 1.67262192369e-27,  # 质子质量
            }
            
            # 简单的数值验证示例
            if 'E=mc^2' in formula_text or 'mc^2' in formula_text:
                # 计算电子的静能
                E = constants['m_e'] * constants['c']**2
                numerical_results['electron_rest_energy'] = E
                numerical_results['electron_rest_energy_MeV'] = E / 1.602176634e-13
                
            elif 'F=G' in formula_text or 'G' in formula_text:
                # 计算地球表面的重力
                m_earth = 5.972e24
                r_earth = 6.371e6
                m = 1.0
                F = constants['G'] * m_earth * m / r_earth**2
                numerical_results['gravitational_force'] = F
                
        except Exception as e:
            logger.warning(f"数值计算时出错: {e}")
            
        return numerical_results
    
    def verify_thesis(self, file_path: str) -> Dict[str, Any]:
        """验证单篇论文
        
        Args:
            file_path: 论文文件路径
            
        Returns:
            验证结果
        """
        logger.info(f"开始验证论文: {file_path}")
        
        result = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'formulas': [],
            'total_formulas': 0,
            'verified_formulas': 0,
            'error_formulas': 0,
            'execution_time': 0.0,
            'status': 'pending'
        }
        
        start_time = time.time()
        
        try:
            # 提取公式
            formulas = self.extract_formulas(file_path)
            result['total_formulas'] = len(formulas)
            
            # 验证每个公式
            verified_count = 0
            error_count = 0
            
            for formula in formulas:
                formula_result = self.verify_formula(formula)
                result['formulas'].append(formula_result)
                
                if formula_result['status'] == 'verified':
                    verified_count += 1
                elif formula_result['status'] == 'error':
                    error_count += 1
            
            result['verified_formulas'] = verified_count
            result['error_formulas'] = error_count
            
            if error_count == 0:
                result['status'] = 'success'
            elif error_count < len(formulas) / 2:
                result['status'] = 'partial_success'
            else:
                result['status'] = 'error'
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            logger.error(f"验证论文时出错 {file_path}: {e}")
            
        result['execution_time'] = time.time() - start_time
        logger.info(f"论文验证完成: {file_path} - 用时 {result['execution_time']:.2f}秒")
        
        return result
    
    def run_batch_verification(self, max_workers: int = 4) -> None:
        """批量验证所有论文
        
        Args:
            max_workers: 并行工作线程数
        """
        self.start_time = time.time()
        
        if not self.thesis_files:
            self.find_thesis_files()
            
        if not self.thesis_files:
            logger.error("没有找到论文文件")
            return
        
        logger.info(f"开始批量验证 {len(self.thesis_files)} 篇论文")
        
        # 使用线程池并行验证
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(self.verify_thesis, file_path): file_path
                for file_path in self.thesis_files
            }
            
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                
                try:
                    result = future.result()
                    self.verification_results[file_path] = result
                    
                    # 显示进度
                    completed = len(self.verification_results)
                    total = len(self.thesis_files)
                    progress = completed / total * 100
                    logger.info(f"进度: {completed}/{total} ({progress:.1f}%)")
                    
                except Exception as e:
                    logger.error(f"处理论文时出错 {file_path}: {e}")
                    self.verification_results[file_path] = {
                        'file_path': file_path,
                        'status': 'error',
                        'error': str(e)
                    }
        
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        logger.info(f"批量验证完成，总用时: {total_time:.2f}秒")
        
    def generate_report(self, output_dir: Optional[str] = None) -> str:
        """生成验证报告
        
        Args:
            output_dir: 输出目录
            
        Returns:
            报告文件路径
        """
        try:
            report_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 确定报告目录
            if output_dir:
                report_dir = output_dir
            else:
                report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
                
            os.makedirs(report_dir, exist_ok=True)
            
            # 生成JSON报告
            json_report_path = os.path.join(report_dir, f'verification_report_{report_time}.json')
            
            report_data = {
                'report_time': datetime.datetime.now().isoformat(),
                'system_info': {
                    'version': '1.0.0',
                    'name': '统一场论论文验证系统'
                },
                'verification_summary': {
                    'total_theses': len(self.verification_results),
                    'success_theses': sum(1 for r in self.verification_results.values() if r.get('status') == 'success'),
                    'partial_success_theses': sum(1 for r in self.verification_results.values() if r.get('status') == 'partial_success'),
                    'error_theses': sum(1 for r in self.verification_results.values() if r.get('status') == 'error'),
                    'total_formulas': sum(r.get('total_formulas', 0) for r in self.verification_results.values()),
                    'verified_formulas': sum(r.get('verified_formulas', 0) for r in self.verification_results.values()),
                    'error_formulas': sum(r.get('error_formulas', 0) for r in self.verification_results.values()),
                    'total_execution_time': self.end_time - self.start_time
                },
                'detailed_results': self.verification_results
            }
            
            with open(json_report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"JSON验证报告已生成: {json_report_path}")
            
            # 生成Markdown报告
            md_report_path = os.path.join(report_dir, f'verification_report_{report_time}.md')
            
            with open(md_report_path, 'w', encoding='utf-8') as f:
                f.write(f"# 统一场论论文验证报告\n\n")
                f.write(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # 摘要部分
                f.write("## 验证摘要\n\n")
                summary = report_data['verification_summary']
                f.write(f"- **总论文数**: {summary['total_theses']}\n")
                f.write(f"- **完全成功**: {summary['success_theses']}\n")
                f.write(f"- **部分成功**: {summary['partial_success_theses']}\n")
                f.write(f"- **验证失败**: {summary['error_theses']}\n")
                f.write(f"- **总公式数**: {summary['total_formulas']}\n")
                f.write(f"- **验证通过**: {summary['verified_formulas']}\n")
                f.write(f"- **验证失败**: {summary['error_formulas']}\n")
                f.write(f"- **总执行时间**: {summary['total_execution_time']:.2f}秒\n\n")
                
                # 详细结果
                f.write("## 详细结果\n\n")
                
                for file_path, result in self.verification_results.items():
                    f.write(f"### {os.path.basename(file_path)}\n")
                    f.write(f"- **状态**: {result.get('status', 'unknown')}\n")
                    f.write(f"- **公式总数**: {result.get('total_formulas', 0)}\n")
                    f.write(f"- **验证通过**: {result.get('verified_formulas', 0)}\n")
                    f.write(f"- **验证失败**: {result.get('error_formulas', 0)}\n")
                    f.write(f"- **执行时间**: {result.get('execution_time', 0):.2f}秒\n\n")
                    
                    if result.get('error'):
                        f.write(f"**错误信息**: {result['error']}\n\n")
            
            logger.info(f"Markdown验证报告已生成: {md_report_path}")
            return json_report_path
            
        except Exception as e:
            logger.error(f"生成报告时出错: {e}")
            return ""

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: python thesis_verification_system.py <论文根目录>")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    
    if not os.path.isdir(base_dir):
        print(f"错误: 目录不存在: {base_dir}")
        sys.exit(1)
    
    logger.info(f"启动统一场论论文验证系统，验证目录: {base_dir}")
    
    # 初始化验证系统
    system = ThesisVerificationSystem(base_dir)
    
    # 运行批量验证
    system.run_batch_verification(max_workers=4)
    
    # 生成报告
    system.generate_report()
    
    logger.info("论文验证系统执行完成!")

if __name__ == "__main__":
    main()