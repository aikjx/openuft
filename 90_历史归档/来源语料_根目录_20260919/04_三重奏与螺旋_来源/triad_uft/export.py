# -*- coding: utf-8 -*-
"""
triad_uft.export — 验证结果数据导出
====================================
将三重奏验证结果导出为 JSON / CSV 格式，便于工业级报告生成与数据持久化。
"""
import json
import csv
import os
import numpy as np
from .provenance import THEOREMS, ValidationStatus


def _convert(obj):
    """递归转换 numpy 类型为 Python 原生类型"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, dict):
        return {k: _convert(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_convert(v) for v in obj]
    if isinstance(obj, ValidationStatus):
        return obj.value
    return obj


def export_result_json(result, filepath):
    """
    导出验证结果为 JSON。

    Parameters
    ----------
    result : dict  验证结果字典（如 check_helix() 的返回值）
    filepath : str  输出文件路径
    """
    data = _convert(result)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filepath


def export_result_csv(result, filepath, key_mapping=None):
    """
    导出验证结果为 CSV（适合数组型结果，如轨迹的逐点验证）。

    Parameters
    ----------
    result : dict  必须包含数组字段（如 rel_errors, kappa2, tau2, x_pos）
    filepath : str  输出文件路径
    key_mapping : dict  字段名映射 {原key: CSV列名}
    """
    # 找出数组字段
    array_keys = [k for k, v in result.items()
                  if isinstance(v, np.ndarray) and v.ndim == 1]
    if not array_keys:
        raise ValueError("结果中无数组字段，无法导出CSV；请用export_result_json")

    n = len(result[array_keys[0]])
    if key_mapping is None:
        key_mapping = {k: k for k in array_keys}

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([key_mapping.get(k, k) for k in array_keys])
        for i in range(n):
            writer.writerow([float(result[k][i]) for k in array_keys])
    return filepath


def export_audit_json(filepath):
    """
    导出定理审计表为 JSON。

    Parameters
    ----------
    filepath : str  输出文件路径
    """
    data = {}
    for key, rec in THEOREMS.items():
        data[key] = {
            "name": rec.name,
            "status": rec.status.value,
            "precision": rec.precision,
            "round_ref": rec.round_ref,
            "note": rec.note,
        }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filepath


def export_audit_csv(filepath):
    """导出定理审计表为 CSV"""
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["key", "name", "status", "precision", "round_ref", "note"])
        for key, rec in THEOREMS.items():
            writer.writerow([
                key, rec.name, rec.status.value,
                rec.precision or "",
                f"R{rec.round_ref}" if rec.round_ref else "",
                rec.note,
            ])
    return filepath


def export_trajectory_csv(simulator, filepath):
    """
    导出粒子模拟器的轨迹为 CSV。

    Parameters
    ----------
    simulator : LorentzSimulator  已运行的模拟器
    filepath : str  输出文件路径
    """
    if simulator.trajectory is None:
        raise RuntimeError("Simulator not run yet. Call run() first.")
    traj = simulator.trajectory
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["t", "x", "y", "z"])
        for i in range(len(traj)):
            t = i * simulator.dt
            writer.writerow([t, traj[i, 0], traj[i, 1], traj[i, 2]])
    return filepath


def batch_export(output_dir, simulator=None, prefix="triad_uft"):
    """
    批量导出：审计表(JSON+CSV) + 可选轨迹。

    Parameters
    ----------
    output_dir : str  输出目录
    simulator : LorentzSimulator  可选，已运行的模拟器
    prefix : str  文件名前缀

    Returns
    -------
    dict: {导出类型: 文件路径}
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = {}
    paths["audit_json"] = export_audit_json(
        os.path.join(output_dir, f"{prefix}_audit.json"))
    paths["audit_csv"] = export_audit_csv(
        os.path.join(output_dir, f"{prefix}_audit.csv"))
    if simulator is not None:
        paths["trajectory_csv"] = export_trajectory_csv(
            simulator, os.path.join(output_dir, f"{prefix}_trajectory.csv"))
        triad_result = simulator.triad_check()
        paths["triad_json"] = export_result_json(
            triad_result, os.path.join(output_dir, f"{prefix}_triad.json"))
        paths["triad_csv"] = export_result_csv(
            triad_result, os.path.join(output_dir, f"{prefix}_triad_points.csv"))
    return paths
