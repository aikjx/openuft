/**
 * 性能监控和调试工具类
 */
class PerformanceMonitor {
    /**
     * 构造函数
     */
    constructor() {
        this.metrics = {
            loadTime: 0,
            renderTime: 0,
            fps: 0,
            memory: {
                used: 0,
                total: 0
            },
            requests: {
                count: 0,
                failed: 0,
                duration: 0
            },
            animations: {
                count: 0,
                active: 0
            }
        };
        
        this.fpsHistory = [];
        this.renderHistory = [];
        this.memoryHistory = [];
        
        this.lastFpsUpdate = performance.now();
        this.frameCount = 0;
        
        this.init();
    }
    
    /**
     * 初始化性能监控
     */
    init() {
        // 监听页面加载完成
        this.measureLoadTime();
        
        // 开始FPS监控
        this.startFpsMonitor();
        
        // 开始内存监控
        this.startMemoryMonitor();
        
        // 监听网络请求
        this.monitorNetworkRequests();
    }
    
    /**
     * 测量页面加载时间
     */
    measureLoadTime() {
        if (typeof window.performance !== 'undefined' && window.performance.timing) {
            const timing = window.performance.timing;
            window.addEventListener('load', () => {
                this.metrics.loadTime = timing.loadEventEnd - timing.navigationStart;
                this.log('页面加载时间:', this.metrics.loadTime, 'ms');
            });
        }
    }
    
    /**
     * 开始FPS监控
     */
    startFpsMonitor() {
        const updateFps = () => {
            const now = performance.now();
            const elapsed = now - this.lastFpsUpdate;
            
            if (elapsed > 1000) {
                this.metrics.fps = Math.round((this.frameCount * 1000) / elapsed);
                this.fpsHistory.push(this.metrics.fps);
                
                // 保持历史记录长度
                if (this.fpsHistory.length > 30) {
                    this.fpsHistory.shift();
                }
                
                this.lastFpsUpdate = now;
                this.frameCount = 0;
                
                // 每5秒记录一次FPS
                if (Math.random() > 0.95) {
                    this.log('当前FPS:', this.metrics.fps);
                }
            }
            
            this.frameCount++;
            requestAnimationFrame(updateFps);
        };
        
        requestAnimationFrame(updateFps);
    }
    
    /**
     * 开始内存监控
     */
    startMemoryMonitor() {
        if (typeof performance !== 'undefined' && performance.memory) {
            setInterval(() => {
                const memory = performance.memory;
                this.metrics.memory = {
                    used: Math.round(memory.usedJSHeapSize / 1024 / 1024 * 100) / 100,
                    total: Math.round(memory.totalJSHeapSize / 1024 / 1024 * 100) / 100
                };
                
                this.memoryHistory.push(this.metrics.memory.used);
                
                // 保持历史记录长度
                if (this.memoryHistory.length > 30) {
                    this.memoryHistory.shift();
                }
                
                // 每10秒记录一次内存使用情况
                if (Math.random() > 0.9) {
                    this.log('内存使用:', this.metrics.memory.used, 'MB /', this.metrics.memory.total, 'MB');
                }
            }, 1000);
        }
    }
    
    /**
     * 监控网络请求
     */
    monitorNetworkRequests() {
        if (typeof window.performance !== 'undefined' && window.performance.getEntriesByType) {
            setInterval(() => {
                const entries = performance.getEntriesByType('navigation');
                if (entries.length > 0) {
                    const navigation = entries[0];
                    this.log('导航时间:', {
                        redirect: navigation.redirectEnd - navigation.redirectStart,
                        dns: navigation.domainLookupEnd - navigation.domainLookupStart,
                        tcp: navigation.connectEnd - navigation.connectStart,
                        ssl: navigation.secureConnectionStart ? (navigation.connectEnd - navigation.secureConnectionStart) : 0,
                        ttfb: navigation.responseStart - navigation.requestStart,
                        download: navigation.responseEnd - navigation.responseStart,
                        dom: navigation.domContentLoadedEventEnd - navigation.navigationStart,
                        load: navigation.loadEventEnd - navigation.navigationStart
                    });
                }
            }, 30000); // 每30秒记录一次
        }
    }
    
    /**
     * 记录渲染时间
     * @param {string} taskName - 任务名称
     * @param {Function} task - 要执行的任务
     * @returns {*} 任务执行结果
     */
    measureRenderTime(taskName, task) {
        const startTime = performance.now();
        const result = task();
        const endTime = performance.now();
        const duration = endTime - startTime;
        
        this.metrics.renderTime = duration;
        this.renderHistory.push(duration);
        
        // 保持历史记录长度
        if (this.renderHistory.length > 30) {
            this.renderHistory.shift();
        }
        
        this.log(`${taskName} 渲染时间:`, duration.toFixed(2), 'ms');
        return result;
    }
    
    /**
     * 记录动画性能
     * @param {string} animationName - 动画名称
     * @param {boolean} isActive - 是否激活
     */
    trackAnimation(animationName, isActive) {
        if (isActive) {
            this.metrics.animations.active++;
        } else {
            this.metrics.animations.active = Math.max(0, this.metrics.animations.active - 1);
        }
        
        this.metrics.animations.count++;
        
        if (Math.random() > 0.9) {
            this.log('动画状态:', {
                active: this.metrics.animations.active,
                total: this.metrics.animations.count
            });
        }
    }
    
    /**
     * 获取性能报告
     * @returns {Object} 性能报告
     */
    getReport() {
        return {
            metrics: this.metrics,
            history: {
                fps: this.fpsHistory,
                render: this.renderHistory,
                memory: this.memoryHistory
            },
            average: {
                fps: this.fpsHistory.length > 0 ? Math.round(this.fpsHistory.reduce((a, b) => a + b, 0) / this.fpsHistory.length) : 0,
                renderTime: this.renderHistory.length > 0 ? Math.round(this.renderHistory.reduce((a, b) => a + b, 0) / this.renderHistory.length * 100) / 100 : 0,
                memory: this.memoryHistory.length > 0 ? Math.round(this.memoryHistory.reduce((a, b) => a + b, 0) / this.memoryHistory.length * 100) / 100 : 0
            }
        };
    }
    
    /**
     * 生成性能摘要
     * @returns {string} 性能摘要
     */
    generateSummary() {
        const report = this.getReport();
        return `
性能监控摘要:
- 页面加载时间: ${this.metrics.loadTime}ms
- 平均FPS: ${report.average.fps}
- 平均渲染时间: ${report.average.renderTime}ms
- 平均内存使用: ${report.average.memory}MB
- 活动动画数: ${this.metrics.animations.active}
- 总动画数: ${this.metrics.animations.count}
        `.trim();
    }
    
    /**
     * 显示性能面板
     */
    showPerformancePanel() {
        // 创建性能面板元素
        const panel = document.createElement('div');
        panel.id = 'performance-panel';
        panel.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            z-index: 10000;
            max-width: 300px;
            max-height: 400px;
            overflow-y: auto;
        `;
        
        // 更新面板内容
        const updatePanel = () => {
            const report = this.getReport();
            panel.innerHTML = `
                <div style="margin-bottom: 8px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 4px;">
                    性能监控
                </div>
                <div style="margin-bottom: 4px;">FPS: ${report.average.fps}</div>
                <div style="margin-bottom: 4px;">内存: ${report.average.memory}MB</div>
                <div style="margin-bottom: 4px;">渲染: ${report.average.renderTime}ms</div>
                <div style="margin-bottom: 4px;">动画: ${this.metrics.animations.active}/${this.metrics.animations.count}</div>
                <div style="margin-bottom: 4px;">加载: ${this.metrics.loadTime}ms</div>
                <button onclick="this.parentElement.remove()" style="margin-top: 8px; background: rgba(255,255,255,0.2); border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; color: white; font-size: 10px;">
                    关闭
                </button>
            `;
        };
        
        // 初始更新
        updatePanel();
        
        // 定期更新
        const interval = setInterval(updatePanel, 1000);
        
        // 添加到页面
        document.body.appendChild(panel);
        
        // 点击关闭时清理
        panel.querySelector('button').addEventListener('click', () => {
            clearInterval(interval);
        });
    }
    
    /**
     * 记录日志
     * @param {...*} args - 日志参数
     */
    log(...args) {
        if (process.env.NODE_ENV !== 'production' || window.DEBUG) {
            console.log('[Performance Monitor]', ...args);
        }
    }
    
    /**
     * 记录警告
     * @param {...*} args - 警告参数
     */
    warn(...args) {
        console.warn('[Performance Monitor]', ...args);
    }
    
    /**
     * 记录错误
     * @param {...*} args - 错误参数
     */
    error(...args) {
        console.error('[Performance Monitor]', ...args);
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceMonitor;
    module.exports.default = PerformanceMonitor;
} else if (typeof window !== 'undefined') {
    window.PerformanceMonitor = PerformanceMonitor;
}
