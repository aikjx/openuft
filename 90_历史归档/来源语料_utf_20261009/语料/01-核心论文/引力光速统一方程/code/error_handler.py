# -*- coding: utf-8 -*-
"""
统一错误处理模块
Unified Error Handling Module

提供系统化的错误处理、日志记录和异常管理功能，确保整个项目的错误处理机制一致且高效。

Author: Quality Assurance Team
Date: 2025-09-16
"""

import sys
import os
import traceback
import logging
import datetime
from enum import Enum, auto
from typing import Union, Tuple, Optional, Dict, Any

# 配置日志记录
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志文件名：包含日期时间
LOG_FILE = os.path.join(LOG_DIR, f'error_log_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('UnifiedFieldTheory')

class ErrorType(Enum):
    """错误类型枚举"""
    SYNTAX_ERROR = auto()          # 语法错误
    IMPORT_ERROR = auto()          # 导入错误
    CALCULATION_ERROR = auto()     # 计算错误
    DIMENSION_ERROR = auto()       # 量纲错误
    PHYSICS_ERROR = auto()         # 物理概念错误
    VISUALIZATION_ERROR = auto()   # 可视化错误
    FILE_ERROR = auto()            # 文件操作错误
    CONFIG_ERROR = auto()          # 配置错误
    OTHER_ERROR = auto()           # 其他错误

class FormulaError(Enum):
    """公式相关错误类型"""
    INTEGRAL_ERROR = auto()        # 积分错误
    GEOMETRIC_FACTOR_ERROR = auto() # 几何因子错误
    UNIT_CONVERSION_ERROR = auto() # 单位转换错误
    PHYSICAL_CONSTANT_ERROR = auto() # 物理常数错误
    DERIVATION_ERROR = auto()      # 推导错误

class UnifiedErrorHandler:
    """统一错误处理器"""
    
    def __init__(self):
        self.error_history = []
        self.total_errors = 0
        self.error_stats = {error_type: 0 for error_type in ErrorType}
    
    def handle_error(self, error_type: ErrorType, message: str, 
                    exception: Optional[Exception] = None, 
                    context: Optional[Dict[str, Any]] = None):
        """
        处理错误并记录到日志
        
        Args:
            error_type: 错误类型
            message: 错误消息
            exception: 异常对象（可选）
            context: 错误上下文信息（可选）
        
        Returns:
            error_id: 错误标识符
        """
        self.total_errors += 1
        self.error_stats[error_type] += 1
        
        error_id = f"ERR_{self.total_errors}_{datetime.datetime.now().strftime('%H%M%S')}"
        
        # 构建错误信息
        error_info = {
            'error_id': error_id,
            'error_type': error_type.name,
            'message': message,
            'timestamp': datetime.datetime.now().isoformat(),
            'context': context or {},
        }
        
        # 如果有异常，添加堆栈信息
        if exception:
            error_info['exception_type'] = type(exception).__name__
            error_info['exception_message'] = str(exception)
            error_info['traceback'] = traceback.format_exc()
        
        # 记录到历史
        self.error_history.append(error_info)
        
        # 记录到日志
        log_level = logging.ERROR if error_type in [ErrorType.SYNTAX_ERROR, ErrorType.CALCULATION_ERROR, ErrorType.PHYSICS_ERROR] else logging.WARNING
        logger.log(log_level, f"{error_id} - {error_type.name}: {message}")
        
        # 如果有异常，记录堆栈
        if exception:
            logger.debug(f"Exception details for {error_id}:\n{error_info['traceback']}")
        
        return error_id
    
    def validate_integral(self, result: float, expected: float, tolerance: float = 1e-6) -> bool:
        """
        验证积分结果是否在容差范围内
        
        Args:
            result: 计算结果
            expected: 预期结果
            tolerance: 容差范围
        
        Returns:
            bool: 是否通过验证
        """
        try:
            if abs(result - expected) > tolerance:
                error_id = self.handle_error(
                    ErrorType.CALCULATION_ERROR,
                    f"Integral validation failed: result={result}, expected={expected}, difference={abs(result-expected)} > tolerance={tolerance}",
                    context={'result': result, 'expected': expected, 'tolerance': tolerance}
                )
                return False
            return True
        except Exception as e:
            self.handle_error(ErrorType.CALCULATION_ERROR, "Failed to validate integral", e)
            return False
    
    def validate_dimensions(self, calculated_dims: str, expected_dims: str) -> bool:
        """
        验证物理量的量纲是否正确
        
        Args:
            calculated_dims: 计算得到的量纲
            expected_dims: 预期的量纲
        
        Returns:
            bool: 是否通过验证
        """
        try:
            if calculated_dims != expected_dims:
                error_id = self.handle_error(
                    ErrorType.DIMENSION_ERROR,
                    f"Dimension validation failed: calculated={calculated_dims}, expected={expected_dims}",
                    context={'calculated_dims': calculated_dims, 'expected_dims': expected_dims}
                )
                return False
            return True
        except Exception as e:
            self.handle_error(ErrorType.DIMENSION_ERROR, "Failed to validate dimensions", e)
            return False
    
    def generate_error_report(self, output_file: Optional[str] = None) -> str:
        """
        生成错误报告
        
        Args:
            output_file: 输出文件路径（可选）
        
        Returns:
            str: 错误报告内容
        """
        report = [
            "=" * 80,
            "UNIFIED FIELD THEORY ERROR REPORT",
            f"Generated on: {datetime.datetime.now().isoformat()}",
            f"Total errors: {self.total_errors}",
            "=" * 80,
            "\nERROR STATISTICS:",
            "-----------------"
        ]
        
        # 添加错误统计
        for error_type, count in self.error_stats.items():
            if count > 0:
                report.append(f"{error_type.name}: {count}")
        
        # 添加详细错误信息
        if self.error_history:
            report.extend([
                "\nDETAILED ERROR INFORMATION:",
                "---------------------------"
            ])
            
            for error in self.error_history:
                report.append(f"\nError ID: {error['error_id']}")
                report.append(f"Type: {error['error_type']}")
                report.append(f"Message: {error['message']}")
                report.append(f"Timestamp: {error['timestamp']}")
                
                if 'exception_type' in error:
                    report.append(f"Exception: {error['exception_type']}: {error['exception_message']}")
                
                if 'context' in error and error['context']:
                    report.append("Context:")
                    for key, value in error['context'].items():
                        report.append(f"  {key}: {value}")
                
                report.append("-" * 60)
        
        report_str = "\n".join(report)
        
        # 如果指定了输出文件，保存报告
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_str)
                logger.info(f"Error report saved to {output_file}")
            except Exception as e:
                self.handle_error(ErrorType.FILE_ERROR, f"Failed to save error report to {output_file}", e)
        
        return report_str
    
    def reset(self):
        """重置错误处理器状态"""
        self.error_history = []
        self.total_errors = 0
        self.error_stats = {error_type: 0 for error_type in ErrorType}

# 创建全局错误处理器实例
error_handler = UnifiedErrorHandler()

def safe_execution(func):
    """
    安全执行装饰器，用于捕获函数执行过程中的异常
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SyntaxError as e:
            error_handler.handle_error(ErrorType.SYNTAX_ERROR, f"Syntax error in {func.__name__}", e)
            return None
        except ImportError as e:
            error_handler.handle_error(ErrorType.IMPORT_ERROR, f"Import error in {func.__name__}", e)
            return None
        except ValueError as e:
            error_handler.handle_error(ErrorType.CALCULATION_ERROR, f"Value error in {func.__name__}", e)
            return None
        except TypeError as e:
            error_handler.handle_error(ErrorType.CALCULATION_ERROR, f"Type error in {func.__name__}", e)
            return None
        except FileNotFoundError as e:
            error_handler.handle_error(ErrorType.FILE_ERROR, f"File not found in {func.__name__}", e)
            return None
        except Exception as e:
            error_handler.handle_error(ErrorType.OTHER_ERROR, f"Unexpected error in {func.__name__}", e)
            return None
    return wrapper

# 导出主要组件
export = {
    'error_handler': error_handler,
    'ErrorType': ErrorType,
    'FormulaError': FormulaError,
    'safe_execution': safe_execution
}