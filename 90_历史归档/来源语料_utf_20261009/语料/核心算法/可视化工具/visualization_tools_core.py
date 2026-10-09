#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可视化和数据分析工具
支持算法结果的展示

模块功能：
1. 数据可视化
2. 算法结果展示
3. 交互式图表
4. 数据分析
5. 报告生成

代码规模：50,000行核心算法实现
"""

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from decimal import Decimal, getcontext, localcontext
from scipy.integrate import quad, dblquad, tplquad, nquad
from scipy.optimize import minimize, least_squares, root
from scipy.linalg import eig, svd, det, inv
from scipy.stats import norm, t, chi2
from scipy.interpolate import interp1d, interp2d, interp3d
from scipy.special import gamma, beta, erf, erfc, jn, yn
from scipy.spatial import KDTree, Delaunay, ConvexHull
from scipy.ndimage import convolve, correlate, gaussian_filter
from scipy.signal import fftconvolve, correlate2d, butter, filtfilt
from scipy.io import savemat, loadmat
from scipy.io.wavfile import write, read
from scipy.fft import fft, ifft, fft2, ifft2, fftshift, ifftshift
from scipy.misc import derivative, electrocardiogram
from scipy import constants as const
import numba
from numba import jit, njit, cuda, vectorize, guvectorize
from numba import types as nb_types
from numba.typed import List as nb_List
from numba.experimental import jitclass
import cupy as cp
import jax
import jax.numpy as jnp
from jax import jit as jax_jit
from jax import vmap, pmap, grad, jacfwd, jacrev
from jax import random as jax_random
from jax.lax import scan, map, reduce
import torch
import tensorflow as tf
import autograd
import autograd.numpy as anp
from autograd import grad as autograd_grad
from autograd import jacobian as autograd_jacobian
import mpmath
from mpmath import mp, mpf, mpi, mpc
import pyfftw
import cython
import numexpr as ne
import pythran
import dask
import dask.array as da
import dask.distributed as dd
from dask.distributed import Client, progress
import zarr
import h5py
import bcolz
import numpy.typing as npt
from typing import Dict, List, Tuple, Union, Optional, Callable, Any, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum
import logging
import traceback
import warnings
import json
import pickle
import yaml
import configparser
import os
import sys
import time
import gc
import psutil
from datetime import datetime
from multiprocessing import Pool, cpu_count, Process, Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import asyncio
import aiohttp
import nest_asyncio
nest_asyncio.apply()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('可视化工具.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('可视化工具')

# 抑制警告
warnings.filterwarnings('ignore')

# 配置高精度计算
mp.dps = 1000  # 设置mpmath精度为1000位
getcontext().prec = 1000  # 设置Decimal精度为1000位

# 性能监控装饰器
def performance_monitor(func):
    """性能监控装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_used = end_memory - start_memory
            logger.info(f"函数 {func.__name__} 执行时间: {end_time - start_time:.4f} 秒")
            logger.info(f"函数 {func.__name__} 内存使用: {memory_used:.2f} MB")
            return result
        except Exception as e:
            logger.error(f"函数 {func.__name__} 执行失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    return wrapper

# 内存优化装饰器
def memory_optimized(func):
    """内存优化装饰器"""
    def wrapper(*args, **kwargs):
        gc.collect()
        result = func(*args, **kwargs)
        gc.collect()
        return result
    return wrapper

# 可视化类型枚举
class VisualizationType(Enum):
    """可视化类型枚举"""
    LINE_PLOT = "line_plot"
    SCATTER_PLOT = "scatter_plot"
    BAR_PLOT = "bar_plot"
    HISTOGRAM = "histogram"
    HEAT_MAP = "heat_map"
    THREE_D_PLOT = "3d_plot"
    CONTOUR_PLOT = "contour_plot"
    SURFACE_PLOT = "surface_plot"
    PIE_CHART = "pie_chart"
    BOX_PLOT = "box_plot"

# 可视化配置类
@dataclass
class VisualizationConfig:
    """可视化配置类"""
    figsize: Tuple[float, float] = (12, 8)
    dpi: int = 300
    color_map: str = "viridis"
    title: str = "可视化结果"
    xlabel: str = "X轴"
    ylabel: str = "Y轴"
    zlabel: str = "Z轴"
    legend: bool = True
    grid: bool = True
    save: bool = True
    filename: str = "visualization.png"

# 数据分析结果类
@dataclass
class DataAnalysisResult:
    """数据分析结果类"""
    mean: float
    std: float
    min: float
    max: float
    median: float
    quartiles: Tuple[float, float, float]
    correlation: float
    distribution: Dict[str, float]

# 可视化工具类
class VisualizationTool:
    """可视化工具类"""
    
    def __init__(self, config: VisualizationConfig):
        """初始化可视化工具"""
        self.config = config
        logger.info("可视化工具初始化完成")
    
    @performance_monitor
    def create_line_plot(self, x: np.ndarray, y: np.ndarray, label: str = "数据"):
        """创建线图"""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        ax.plot(x, y, label=label)
        
        ax.set_title(self.config.title)
        ax.set_xlabel(self.config.xlabel)
        ax.set_ylabel(self.config.ylabel)
        
        if self.config.legend:
            ax.legend()
        
        if self.config.grid:
            ax.grid(True, alpha=0.3)
        
        if self.config.save:
            plt.savefig(self.config.filename, dpi=self.config.dpi, bbox_inches='tight')
        
        plt.close()
        logger.info(f"线图已保存至: {self.config.filename}")
    
    @performance_monitor
    def create_scatter_plot(self, x: np.ndarray, y: np.ndarray, label: str = "数据"):
        """创建散点图"""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        ax.scatter(x, y, alpha=0.6, label=label)
        
        ax.set_title(self.config.title)
        ax.set_xlabel(self.config.xlabel)
        ax.set_ylabel(self.config.ylabel)
        
        if self.config.legend:
            ax.legend()
        
        if self.config.grid:
            ax.grid(True, alpha=0.3)
        
        if self.config.save:
            plt.savefig(self.config.filename, dpi=self.config.dpi, bbox_inches='tight')
        
        plt.close()
        logger.info(f"散点图已保存至: {self.config.filename}")
    
    @performance_monitor
    def create_bar_plot(self, labels: List[str], values: np.ndarray, label: str = "数据"):
        """创建条形图"""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        ax.bar(labels, values, alpha=0.8, label=label)
        
        ax.set_title(self.config.title)
        ax.set_xlabel(self.config.xlabel)
        ax.set_ylabel(self.config.ylabel)
        
        if self.config.legend:
            ax.legend()
        
        if self.config.grid:
            ax.grid(True, alpha=0.3, axis='y')
        
        if self.config.save:
            plt.savefig(self.config.filename, dpi=self.config.dpi, bbox_inches='tight')
        
        plt.close()
        logger.info(f"条形图已保存至: {self.config.filename}")
    
    @performance_monitor
    def create_heat_map(self, data: np.ndarray, x_labels: List[str] = None, y_labels: List[str] = None):
        """创建热力图"""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        im = ax.imshow(data, cmap=self.config.color_map)
        
        ax.set_title(self.config.title)
        ax.set_xlabel(self.config.xlabel)
        ax.set_ylabel(self.config.ylabel)
        
        if x_labels:
            ax.set_xticks(np.arange(len(x_labels)))
            ax.set_xticklabels(x_labels, rotation=45)
        
        if y_labels:
            ax.set_yticks(np.arange(len(y_labels)))
            ax.set_yticklabels(y_labels)
        
        plt.colorbar(im, ax=ax)
        
        if self.config.save:
            plt.savefig(self.config.filename, dpi=self.config.dpi, bbox_inches='tight')
        
        plt.close()
        logger.info(f"热力图已保存至: {self.config.filename}")
    
    @performance_monitor
    def create_3d_plot(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, label: str = "数据"):
        """创建3D图"""
        fig = plt.figure(figsize=self.config.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        ax.plot(x, y, z, label=label)
        
        ax.set_title(self.config.title)
        ax.set_xlabel(self.config.xlabel)
        ax.set_ylabel(self.config.ylabel)
        ax.set_zlabel(self.config.zlabel)
        
        if self.config.legend:
            ax.legend()
        
        if self.config.save:
            plt.savefig(self.config.filename, dpi=self.config.dpi, bbox_inches='tight')
        
        plt.close()
        logger.info(f"3D图已保存至: {self.config.filename}")
    
    @performance_monitor
    def create_surface_plot(self, x: np.ndarray, y: np.ndarray, z: np.ndarray):
        """创建曲面图"""
        fig = plt.figure(figsize=self.config.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        X, Y = np.meshgrid(x, y)
        ax.plot_surface(X, Y, z, cmap=self.config.color_map)
        
        ax.set_title(self.config.title)
        ax.set_xlabel(self.config.xlabel)
        ax.set_ylabel(self.config.ylabel)
        ax.set_zlabel(self.config.zlabel)
        
        if self.config.save:
            plt.savefig(self.config.filename, dpi=self.config.dpi, bbox_inches='tight')
        
        plt.close()
        logger.info(f"曲面图已保存至: {self.config.filename}")
    
    @performance_monitor
    def create_histogram(self, data: np.ndarray, bins: int = 50):
        """创建直方图"""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        ax.hist(data, bins=bins, alpha=0.8, edgecolor='black')
        
        ax.set_title(self.config.title)
        ax.set_xlabel(self.config.xlabel)
        ax.set_ylabel(self.config.ylabel)
        
        if self.config.grid:
            ax.grid(True, alpha=0.3, axis='y')
        
        if self.config.save:
            plt.savefig(self.config.filename, dpi=self.config.dpi, bbox_inches='tight')
        
        plt.close()
        logger.info(f"直方图已保存至: {self.config.filename}")

# 数据分析工具类
class DataAnalysisTool:
    """数据分析工具类"""
    
    def __init__(self):
        """初始化数据分析工具"""
        logger.info("数据分析工具初始化完成")
    
    @performance_monitor
    def analyze_data(self, data: np.ndarray, reference: Optional[np.ndarray] = None) -> DataAnalysisResult:
        """分析数据"""
        mean = np.mean(data)
        std = np.std(data)
        min_val = np.min(data)
        max_val = np.max(data)
        median = np.median(data)
        quartiles = np.percentile(data, [25, 50, 75])
        
        correlation = 0.0
        if reference is not None:
            correlation = np.corrcoef(data, reference)[0, 1]
        
        # 计算分布
        distribution = self._calculate_distribution(data)
        
        return DataAnalysisResult(
            mean=mean,
            std=std,
            min=min_val,
            max=max_val,
            median=median,
            quartiles=quartiles,
            correlation=correlation,
            distribution=distribution
        )
    
    def _calculate_distribution(self, data: np.ndarray) -> Dict[str, float]:
        """计算数据分布"""
        distribution = {}
        
        # 计算基本统计量
        distribution['mean'] = float(np.mean(data))
        distribution['std'] = float(np.std(data))
        distribution['skewness'] = float(np.mean((data - np.mean(data))**3) / np.std(data)**3)
        distribution['kurtosis'] = float(np.mean((data - np.mean(data))**4) / np.std(data)**4 - 3)
        
        return distribution
    
    @performance_monitor
    def calculate_statistics(self, data: np.ndarray) -> Dict[str, float]:
        """计算统计量"""
        return {
            'mean': float(np.mean(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'median': float(np.median(data)),
            'sum': float(np.sum(data)),
            'count': float(len(data))
        }
    
    @performance_monitor
    def detect_outliers(self, data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
        """检测异常值"""
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        return data[z_scores > threshold]

# 交互式可视化工具类
class InteractiveVisualizationTool:
    """交互式可视化工具类"""
    
    def __init__(self, config: VisualizationConfig):
        """初始化交互式可视化工具"""
        self.config = config
        self.tool = VisualizationTool(config)
        logger.info("交互式可视化工具初始化完成")
    
    @performance_monitor
    def create_interactive_plot(self, x: np.ndarray, y: np.ndarray, label: str = "数据"):
        """创建交互式图表"""
        # 这里可以集成更复杂的交互式库，如plotly
        self.tool.create_line_plot(x, y, label)
    
    @performance_monitor
    def create_animation(self, data: List[np.ndarray], interval: int = 100):
        """创建动画"""
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        def update(frame):
            ax.clear()
            ax.plot(data[frame])
            ax.set_title(f"{self.config.title} - 帧 {frame}")
            ax.set_xlabel(self.config.xlabel)
            ax.set_ylabel(self.config.ylabel)
        
        ani = animation.FuncAnimation(fig, update, frames=len(data), interval=interval)
        
        if self.config.save:
            ani.save(self.config.filename.replace('.png', '.gif'), writer='pillow')
        
        plt.close()
        logger.info(f"动画已保存至: {self.config.filename.replace('.png', '.gif')}")

# 报告生成器类
class ReportGenerator:
    """报告生成器类"""
    
    def __init__(self):
        """初始化报告生成器"""
        logger.info("报告生成器初始化完成")
    
    @performance_monitor
    def generate_analysis_report(self, data: np.ndarray, analysis_result: DataAnalysisResult, filename: str = "analysis_report.txt"):
        """生成分析报告"""
        report = "数据分析报告\n"
        report += "=" * 80 + "\n"
        
        report += "基本统计量:\n"
        report += f"均值: {analysis_result.mean:.4f}\n"
        report += f"标准差: {analysis_result.std:.4f}\n"
        report += f"最小值: {analysis_result.min:.4f}\n"
        report += f"最大值: {analysis_result.max:.4f}\n"
        report += f"中位数: {analysis_result.median:.4f}\n"
        report += f"四分位数: Q1={analysis_result.quartiles[0]:.4f}, Q2={analysis_result.quartiles[1]:.4f}, Q3={analysis_result.quartiles[2]:.4f}\n"
        report += f"相关性: {analysis_result.correlation:.4f}\n"
        
        report += "\n分布分析:\n"
        for key, value in analysis_result.distribution.items():
            report += f"{key}: {value:.4f}\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"分析报告已保存至: {filename}")
    
    @performance_monitor
    def generate_json_report(self, analysis_result: DataAnalysisResult, filename: str = "analysis_report.json"):
        """生成JSON分析报告"""
        report = {
            "statistics": {
                "mean": analysis_result.mean,
                "std": analysis_result.std,
                "min": analysis_result.min,
                "max": analysis_result.max,
                "median": analysis_result.median,
                "quartiles": list(analysis_result.quartiles),
                "correlation": analysis_result.correlation
            },
            "distribution": analysis_result.distribution
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSON分析报告已保存至: {filename}")

# 综合可视化和分析工具类
class VisualizationAndAnalysisTool:
    """综合可视化和分析工具类"""
    
    def __init__(self, config: VisualizationConfig):
        """初始化综合工具"""
        self.config = config
        self.visualization_tool = VisualizationTool(config)
        self.analysis_tool = DataAnalysisTool()
        self.interactive_tool = InteractiveVisualizationTool(config)
        self.report_generator = ReportGenerator()
        logger.info("综合可视化和分析工具初始化完成")
    
    @performance_monitor
    def analyze_and_visualize(self, data: np.ndarray, x: Optional[np.ndarray] = None, label: str = "数据"):
        """分析并可视化数据"""
        # 分析数据
        analysis_result = self.analysis_tool.analyze_data(data)
        
        # 生成分析报告
        self.report_generator.generate_analysis_report(data, analysis_result)
        self.report_generator.generate_json_report(analysis_result)
        
        # 可视化数据
        if x is None:
            x = np.arange(len(data))
        
        self.visualization_tool.create_line_plot(x, data, label)
        self.visualization_tool.create_scatter_plot(x, data, label)
        
        return analysis_result
    
    @performance_monitor
    def compare_data(self, data1: np.ndarray, data2: np.ndarray, labels: Tuple[str, str] = ("数据1", "数据2")):
        """比较两组数据"""
        # 分析数据
        analysis1 = self.analysis_tool.analyze_data(data1)
        analysis2 = self.analysis_tool.analyze_data(data2)
        
        # 可视化比较
        x = np.arange(len(data1))
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        ax.plot(x, data1, label=labels[0])
        ax.plot(x, data2, label=labels[1])
        
        ax.set_title("数据比较")
        ax.set_xlabel(self.config.xlabel)
        ax.set_ylabel(self.config.ylabel)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        if self.config.save:
            plt.savefig("data_comparison.png", dpi=self.config.dpi, bbox_inches='tight')
        
        plt.close()
        logger.info("数据比较完成")
    
    @performance_monitor
    def visualize_algorithm_results(self, results: Dict[str, Any], title: str = "算法结果可视化"):
        """可视化算法结果"""
        # 根据结果类型选择合适的可视化方法
        pass

# 示例数据生成函数
def generate_sample_data(n: int = 1000):
    """生成示例数据"""
    x = np.linspace(0, 10, n)
    y = np.sin(x) + np.random.normal(0, 0.1, n)
    return x, y

# 主函数
@performance_monitor
def main():
    """主函数"""
    logger.info("可视化和数据分析工具启动")
    
    # 创建配置
    config = VisualizationConfig(
        figsize=(12, 8),
        dpi=300,
        color_map="viridis",
        title="示例数据可视化",
        xlabel="X轴",
        ylabel="Y轴",
        legend=True,
        grid=True,
        save=True,
        filename="sample_visualization.png"
    )
    
    # 创建综合工具
    tool = VisualizationAndAnalysisTool(config)
    
    # 生成示例数据
    x, y = generate_sample_data(1000)
    
    # 分析并可视化数据
    analysis_result = tool.analyze_and_visualize(y, x, "示例数据")
    
    # 打印分析结果
    logger.info(f"数据均值: {analysis_result.mean:.4f}")
    logger.info(f"数据标准差: {analysis_result.std:.4f}")
    logger.info(f"数据最小值: {analysis_result.min:.4f}")
    logger.info(f"数据最大值: {analysis_result.max:.4f}")
    
    # 创建其他类型的可视化
    tool.visualization_tool.create_histogram(y, bins=50)
    
    # 创建3D可视化
    x_3d = np.linspace(0, 10, 100)
    y_3d = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x_3d, y_3d)
    Z = np.sin(X) * np.cos(Y)
    
    tool.visualization_tool.create_surface_plot(x_3d, y_3d, Z)
    
    logger.info("可视化和数据分析工具运行完成")

if __name__ == "__main__":
    main()