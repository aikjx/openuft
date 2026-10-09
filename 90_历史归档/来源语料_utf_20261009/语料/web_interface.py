#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论验证系统Web管理界面
基于Flask的Web管理系统
"""

import os
import sys
import json
import time
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from thesis_verification_system import ThesisVerificationSystem
except ImportError:
    print("警告: 无法导入验证系统模块")
    ThesisVerificationSystem = None

app = Flask(__name__)
CORS(app)

# 全局验证系统实例
verification_system = None

# 报告目录
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
os.makedirs(REPORT_DIR, exist_ok=True)

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/api/init', methods=['POST'])
def init_system():
    """初始化验证系统"""
    global verification_system
    
    try:
        data = request.get_json()
        base_dir = data.get('base_dir', os.path.join(os.path.dirname(os.path.abspath(__file__)), '01-核心论文'))
        
        if ThesisVerificationSystem is None:
            return jsonify({
                'status': 'error',
                'message': '验证系统模块未找到'
            })
        
        verification_system = ThesisVerificationSystem(base_dir)
        
        # 查找论文文件
        thesis_files = verification_system.find_thesis_files()
        
        return jsonify({
            'status': 'success',
            'message': f'验证系统初始化成功，找到 {len(thesis_files)} 篇论文',
            'thesis_count': len(thesis_files)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'初始化失败: {str(e)}'
        })

@app.route('/api/thesis/list')
def list_thesis():
    """获取论文列表"""
    global verification_system
    
    try:
        if verification_system is None:
            return jsonify({
                'status': 'error',
                'message': '系统未初始化'
            })
        
        thesis_files = verification_system.thesis_files
        thesis_list = []
        
        for file_path in thesis_files:
            thesis_list.append({
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': os.path.getsize(file_path),
                'modified': time.ctime(os.path.getmtime(file_path))
            })
        
        return jsonify({
            'status': 'success',
            'thesis_list': thesis_list,
            'total_count': len(thesis_list)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取论文列表失败: {str(e)}'
        })

@app.route('/api/thesis/analyze', methods=['POST'])
def analyze_thesis():
    """分析单个论文"""
    global verification_system
    
    try:
        data = request.get_json()
        file_path = data.get('file_path', '')
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({
                'status': 'error',
                'message': '论文文件不存在'
            })
        
        if verification_system is None:
            return jsonify({
                'status': 'error',
                'message': '系统未初始化'
            })
        
        # 提取公式
        formulas = verification_system.extract_formulas(file_path)
        
        return jsonify({
            'status': 'success',
            'file_path': file_path,
            'formula_count': len(formulas),
            'formulas': formulas
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'分析论文失败: {str(e)}'
        })

@app.route('/api/verify/batch', methods=['POST'])
def batch_verify():
    """批量验证论文"""
    global verification_system
    
    try:
        data = request.get_json()
        max_workers = data.get('max_workers', 4)
        
        if verification_system is None:
            return jsonify({
                'status': 'error',
                'message': '系统未初始化'
            })
        
        # 运行批量验证
        verification_system.run_batch_verification(max_workers=max_workers)
        
        # 生成报告
        report_path = verification_system.generate_report()
        
        return jsonify({
            'status': 'success',
            'message': '批量验证完成',
            'report_path': report_path,
            'verification_count': len(verification_system.verification_results)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'批量验证失败: {str(e)}'
        })

@app.route('/api/report/list')
def list_reports():
    """获取报告列表"""
    try:
        reports = []
        
        if os.path.exists(REPORT_DIR):
            for file in os.listdir(REPORT_DIR):
                if file.endswith('.json') or file.endswith('.md'):
                    file_path = os.path.join(REPORT_DIR, file)
                    reports.append({
                        'name': file,
                        'path': file_path,
                        'size': os.path.getsize(file_path),
                        'modified': time.ctime(os.path.getmtime(file_path))
                    })
        
        return jsonify({
            'status': 'success',
            'reports': reports,
            'total_count': len(reports)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取报告列表失败: {str(e)}'
        })

@app.route('/api/report/<report_name>')
def get_report(report_name):
    """获取报告内容"""
    try:
        report_path = os.path.join(REPORT_DIR, report_name)
        
        if not os.path.exists(report_path):
            return jsonify({
                'status': 'error',
                'message': '报告文件不存在'
            })
        
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'status': 'success',
            'report_name': report_name,
            'content': content
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取报告失败: {str(e)}'
        })

@app.route('/api/report/download/<report_name>')
def download_report(report_name):
    """下载报告文件"""
    try:
        report_path = os.path.join(REPORT_DIR, report_name)
        
        if not os.path.exists(report_path):
            return jsonify({
                'status': 'error',
                'message': '报告文件不存在'
            })
        
        return send_file(report_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'下载报告失败: {str(e)}'
        })

@app.route('/api/status')
def get_status():
    """获取系统状态"""
    global verification_system
    
    try:
        status = {
            'initialized': verification_system is not None,
            'thesis_count': len(verification_system.thesis_files) if verification_system else 0,
            'verification_count': len(verification_system.verification_results) if verification_system else 0,
            'report_count': len([f for f in os.listdir(REPORT_DIR) if f.endswith('.json') or f.endswith('.md')]) if os.path.exists(REPORT_DIR) else 0
        }
        
        return jsonify({
            'status': 'success',
            'system_status': status
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取状态失败: {str(e)}'
        })

@app.route('/api/optimize', methods=['POST'])
def optimize_system():
    """优化系统性能"""
    try:
        # 这里可以实现系统性能优化逻辑
        # 例如：清理缓存、调整线程池大小等
        
        return jsonify({
            'status': 'success',
            'message': '系统优化完成'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'优化失败: {str(e)}'
        })

# 创建模板目录
def create_templates():
    """创建Web界面模板"""
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    os.makedirs(template_dir, exist_ok=True)
    
    # 创建index.html模板
    index_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>统一场论验证系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.umd.min.js"></script>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background-color: #f8f9fa;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        .card {
            margin-bottom: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .card-header {
            background-color: #667eea;
            color: white;
            font-weight: bold;
        }
        .status-badge {
            font-size: 0.8rem;
            padding: 0.25rem 0.5rem;
            border-radius: 1rem;
        }
        .badge-success {
            background-color: #28a745;
        }
        .badge-error {
            background-color: #dc3545;
        }
        .badge-warning {
            background-color: #ffc107;
            color: #212529;
        }
        .progress-bar {
            transition: width 0.3s ease;
        }
        .formula-card {
            background-color: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            border-radius: 0.25rem;
        }
        .thesis-item {
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        .thesis-item:hover {
            background-color: #f8f9fa;
        }
        .report-item {
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        .report-item:hover {
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1 class="display-4">统一场论验证系统</h1>
            <p class="lead">高性能数学公式验证与分析平台</p>
        </div>
    </div>

    <div class="container">
        <!-- 系统状态 -->
        <div class="card">
            <div class="card-header">
                系统状态
            </div>
            <div class="card-body">
                <div class="row" id="system-status">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">初始化状态</h5>
                                <p class="card-text" id="init-status">未初始化</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">论文数量</h5>
                                <p class="card-text" id="thesis-count">0</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">验证完成</h5>
                                <p class="card-text" id="verification-count">0</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">报告数量</h5>
                                <p class="card-text" id="report-count">0</p>
                            </div>
                        </div>
                    </div>
                </div>
                <button class="btn btn-primary mt-3" id="init-btn">初始化系统</button>
            </div>
        </div>

        <!-- 批量验证 -->
        <div class="card">
            <div class="card-header">
                批量验证
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label for="max-workers" class="form-label">线程数</label>
                    <input type="number" class="form-control" id="max-workers" value="4" min="1" max="16">
                </div>
                <button class="btn btn-success" id="batch-verify-btn">开始批量验证</button>
                <div class="mt-3" id="verification-progress" style="display: none;">
                    <div class="progress">
                        <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <p class="mt-2" id="progress-text">准备开始...</p>
                </div>
            </div>
        </div>

        <!-- 论文列表 -->
        <div class="card">
            <div class="card-header">
                论文列表
            </div>
            <div class="card-body">
                <div class="input-group mb-3">
                    <input type="text" class="form-control" placeholder="搜索论文..." id="thesis-search">
                    <button class="btn btn-outline-secondary" type="button" id="search-btn">搜索</button>
                </div>
                <div class="overflow-auto" style="max-height: 400px;">
                    <table class="table table-striped" id="thesis-table">
                        <thead>
                            <tr>
                                <th>论文名称</th>
                                <th>大小</th>
                                <th>修改时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td colspan="4" class="text-center">请先初始化系统</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- 报告列表 -->
        <div class="card">
            <div class="card-header">
                验证报告
            </div>
            <div class="card-body">
                <div class="overflow-auto" style="max-height: 400px;">
                    <table class="table table-striped" id="report-table">
                        <thead>
                            <tr>
                                <th>报告名称</th>
                                <th>大小</th>
                                <th>修改时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td colspan="4" class="text-center">暂无报告</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- 论文分析模态框 -->
    <div class="modal fade" id="thesis-modal" tabindex="-1" aria-labelledby="thesis-modal-label" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="thesis-modal-label">论文分析</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div id="thesis-analysis-content">
                        <p>分析中...</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                </div>
            </div>
        </div>
    </div>

    <!-- 报告查看模态框 -->
    <div class="modal fade" id="report-modal" tabindex="-1" aria-labelledby="report-modal-label" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="report-modal-label">报告查看</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div id="report-content">
                        <p>加载中...</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 全局变量
        let currentThesisPath = '';
        let currentReportName = '';

        // 初始化页面
        document.addEventListener('DOMContentLoaded', function() {
            loadSystemStatus();
            loadReports();
        });

        // 加载系统状态
        function loadSystemStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const status = data.system_status;
                        document.getElementById('init-status').textContent = status.initialized ? '已初始化' : '未初始化';
                        document.getElementById('thesis-count').textContent = status.thesis_count;
                        document.getElementById('verification-count').textContent = status.verification_count;
                        document.getElementById('report-count').textContent = status.report_count;

                        if (status.initialized) {
                            loadThesisList();
                        }
                    }
                });
        }

        // 初始化系统
        document.getElementById('init-btn').addEventListener('click', function() {
            this.disabled = true;
            this.textContent = '初始化中...';

            fetch('/api/init', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                    loadSystemStatus();
                } else {
                    alert('初始化失败: ' + data.message);
                }
            })
            .finally(() => {
                this.disabled = false;
                this.textContent = '初始化系统';
            });
        });

        // 加载论文列表
        function loadThesisList() {
            fetch('/api/thesis/list')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const tbody = document.getElementById('thesis-table').querySelector('tbody');
                        tbody.innerHTML = '';

                        data.thesis_list.forEach(thesis => {
                            const row = document.createElement('tr');
                            row.className = 'thesis-item';
                            row.dataset.path = thesis.path;

                            const size = (thesis.size / 1024).toFixed(2) + ' KB';

                            row.innerHTML = `
                                <td>${thesis.name}</td>
                                <td>${size}</td>
                                <td>${thesis.modified}</td>
                                <td>
                                    <button class="btn btn-sm btn-info analyze-btn">分析</button>
                                </td>
                            `;

                            tbody.appendChild(row);
                        });

                        // 添加分析按钮事件
                        document.querySelectorAll('.analyze-btn').forEach(btn => {
                            btn.addEventListener('click', function() {
                                const row = this.closest('tr');
                                const thesisPath = row.dataset.path;
                                analyzeThesis(thesisPath);
                            });
                        });
                    }
                });
        }

        // 分析论文
        function analyzeThesis(path) {
            currentThesisPath = path;

            fetch('/api/thesis/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ file_path: path })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const modal = new bootstrap.Modal(document.getElementById('thesis-modal'));
                    const content = document.getElementById('thesis-analysis-content');

                    let html = `
                        <h6>论文: ${data.file_path.split('/').pop()}</h6>
                        <p>公式数量: ${data.formula_count}</p>
                        <hr>
                    `;

                    if (data.formulas.length > 0) {
                        html += '<h6>公式列表:</h6>';
                        data.formulas.forEach((formula, index) => {
                            html += `
                                <div class="formula-card">
                                    <strong>公式 ${index + 1} (${formula.type}):</strong>
                                    <p>${formula.content}</p>
                                </div>
                            `;
                        });
                    } else {
                        html += '<p>该论文中未找到公式</p>';
                    }

                    content.innerHTML = html;
                    modal.show();
                } else {
                    alert('分析失败: ' + data.message);
                }
            });
        }

        // 批量验证
        document.getElementById('batch-verify-btn').addEventListener('click', function() {
            const maxWorkers = document.getElementById('max-workers').value;
            const progressDiv = document.getElementById('verification-progress');
            const progressBar = progressDiv.querySelector('.progress-bar');
            const progressText = document.getElementById('progress-text');

            this.disabled = true;
            progressDiv.style.display = 'block';
            progressBar.style.width = '0%';
            progressBar.setAttribute('aria-valuenow', '0');
            progressText.textContent = '准备开始...';

            fetch('/api/verify/batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ max_workers: maxWorkers })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    progressBar.style.width = '100%';
                    progressBar.setAttribute('aria-valuenow', '100');
                    progressText.textContent = '验证完成!';
                    alert(data.message);
                    loadSystemStatus();
                    loadReports();
                } else {
                    progressText.textContent = '验证失败';
                    alert('验证失败: ' + data.message);
                }
            })
            .finally(() => {
                this.disabled = false;
                setTimeout(() => {
                    progressDiv.style.display = 'none';
                }, 2000);
            });
        });

        // 加载报告列表
        function loadReports() {
            fetch('/api/report/list')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const tbody = document.getElementById('report-table').querySelector('tbody');
                        tbody.innerHTML = '';

                        if (data.reports.length > 0) {
                            data.reports.forEach(report => {
                                const row = document.createElement('tr');
                                row.className = 'report-item';
                                row.dataset.name = report.name;

                                const size = (report.size / 1024).toFixed(2) + ' KB';

                                row.innerHTML = `
                                    <td>${report.name}</td>
                                    <td>${size}</td>
                                    <td>${report.modified}</td>
                                    <td>
                                        <button class="btn btn-sm btn-primary view-btn">查看</button>
                                        <a href="/api/report/download/${report.name}" class="btn btn-sm btn-outline-secondary">下载</a>
                                    </td>
                                `;

                                tbody.appendChild(row);
                            });

                            // 添加查看按钮事件
                            document.querySelectorAll('.view-btn').forEach(btn => {
                                btn.addEventListener('click', function() {
                                    const row = this.closest('tr');
                                    const reportName = row.dataset.name;
                                    viewReport(reportName);
                                });
                            });
                        } else {
                            tbody.innerHTML = '<tr><td colspan="4" class="text-center">暂无报告</td></tr>';
                        }
                    }
                });
        }

        // 查看报告
        function viewReport(name) {
            currentReportName = name;

            fetch('/api/report/' + name)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const modal = new bootstrap.Modal(document.getElementById('report-modal'));
                        const content = document.getElementById('report-content');

                        let html = '';
                        if (name.endsWith('.json')) {
                            // JSON格式报告
                            const jsonObj = JSON.parse(data.content);
                            html = '<pre>' + JSON.stringify(jsonObj, null, 2) + '</pre>';
                        } else if (name.endsWith('.md')) {
                            // Markdown格式报告
                            html = '<div class="markdown-body">' + data.content + '</div>';
                        } else {
                            html = '<pre>' + data.content + '</pre>';
                        }

                        content.innerHTML = html;
                        modal.show();
                    } else {
                        alert('加载失败: ' + data.message);
                    }
                });
        }

        // 搜索论文
        document.getElementById('search-btn').addEventListener('click', function() {
            const searchTerm = document.getElementById('thesis-search').value.toLowerCase();
            const rows = document.querySelectorAll('#thesis-table tbody tr');

            rows.forEach(row => {
                const thesisName = row.querySelector('td:first-child').textContent.toLowerCase();
                if (thesisName.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>
'''
        
    with open(os.path.join(template_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

def main():
    """主函数"""
    # 创建模板
    create_templates()
    
    # 启动Flask应用
    print("统一场论验证系统Web界面启动中...")
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()