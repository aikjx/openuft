/**
 * 性能优化相关工具函数
 */
class PerformanceUtils {
    /**
     * 检测浏览器兼容性
     * @returns {Object} 浏览器兼容性信息
     */
    static detectBrowserCompatibility() {
        const browserInfo = {
            name: 'unknown',
            version: 'unknown',
            isModern: true,
            supportedFeatures: {
                webgl: false,
                webgl2: false,
                es6: false,
                fetch: false,
                promis: false
            }
        };
        
        // 检测WebGL支持
        try {
            const canvas = document.createElement('canvas');
            browserInfo.supportedFeatures.webgl = !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
            browserInfo.supportedFeatures.webgl2 = !!(window.WebGL2RenderingContext && canvas.getContext('webgl2'));
        } catch (e) {
            browserInfo.supportedFeatures.webgl = false;
            browserInfo.supportedFeatures.webgl2 = false;
        }
        
        // 检测ES6支持
        browserInfo.supportedFeatures.es6 = typeof Promise !== 'undefined' && typeof fetch !== 'undefined';
        browserInfo.supportedFeatures.fetch = typeof fetch !== 'undefined';
        browserInfo.supportedFeatures.promise = typeof Promise !== 'undefined';
        browserInfo.supportedFeatures.classes = typeof class {} === 'function';
        browserInfo.supportedFeatures.arrowFunctions = typeof (() => {}) === 'function';
        browserInfo.supportedFeatures.modules = typeof module !== 'undefined' || 'noModule' in document.createElement('script');
        
        // 检测浏览器类型和版本
        const userAgent = navigator.userAgent.toLowerCase();
        if (userAgent.includes('chrome')) {
            browserInfo.name = 'chrome';
            browserInfo.version = userAgent.match(/chrome\/(\d+)/)?.[1] || 'unknown';
        } else if (userAgent.includes('firefox')) {
            browserInfo.name = 'firefox';
            browserInfo.version = userAgent.match(/firefox\/(\d+)/)?.[1] || 'unknown';
        } else if (userAgent.includes('safari') && !userAgent.includes('chrome')) {
            browserInfo.name = 'safari';
            browserInfo.version = userAgent.match(/version\/(\d+)/)?.[1] || 'unknown';
        } else if (userAgent.includes('edge')) {
            browserInfo.name = 'edge';
            browserInfo.version = userAgent.match(/edge\/(\d+)/)?.[1] || 'unknown';
        } else if (userAgent.includes('msie') || userAgent.includes('trident')) {
            browserInfo.name = 'ie';
            browserInfo.version = userAgent.match(/msie (\d+)/)?.[1] || 'unknown';
            browserInfo.isModern = false;
        }
        
        return browserInfo;
    }
    /**
     * 检测设备性能级别
     * @returns {string} 性能级别: 'high', 'medium', 'low'
     */
    static detectDevicePerformance() {
        try {
            // 综合检测多种性能指标
            const performance = {
                hardwareConcurrency: navigator.hardwareConcurrency || 2,
                devicePixelRatio: window.devicePixelRatio || 1,
                memory: navigator.deviceMemory || 4,
                performance: typeof window.performance !== 'undefined'
            };
            
            // 计算性能得分
            let score = 0;
            score += performance.hardwareConcurrency * 10;
            score += (8 / performance.devicePixelRatio) * 5;
            score += performance.memory * 5;
            score += performance.performance ? 10 : 0;
            
            if (score >= 120) {
                return 'high';
            } else if (score >= 70) {
                return 'medium';
            } else {
                return 'low';
            }
        } catch (e) {
            // 旧浏览器fallback
            return 'low';
        }
    }
    /**
     * 检测元素是否在视口中
     * @param {HTMLElement} el - 要检测的元素
     * @returns {boolean} 是否在视口中
     */
    static isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    /**
     * 防抖函数
     * @param {Function} func - 要防抖的函数
     * @param {number} wait - 等待时间（毫秒）
     * @returns {Function} 防抖后的函数
     */
    static debounce(func, wait = 100) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * 节流函数
     * @param {Function} func - 要节流的函数
     * @param {number} limit - 时间限制（毫秒）
     * @returns {Function} 节流后的函数
     */
    static throttle(func, limit = 100) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * 计算两点之间的距离
     * @param {Object} point1 - 第一个点 {x, y}
     * @param {Object} point2 - 第二个点 {x, y}
     * @returns {number} 距离
     */
    static distance(point1, point2) {
        const dx = point2.x - point1.x;
        const dy = point2.y - point1.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    /**
     * 跨浏览器事件监听
     * @param {Element} element - 元素
     * @param {string} event - 事件名称
     * @param {Function} handler - 事件处理函数
     */
    static addEventListener(element, event, handler) {
        if (element.addEventListener) {
            element.addEventListener(event, handler, false);
        } else if (element.attachEvent) {
            element.attachEvent('on' + event, handler);
        } else {
            element['on' + event] = handler;
        }
    }

    /**
     * 跨浏览器移除事件监听
     * @param {Element} element - 元素
     * @param {string} event - 事件名称
     * @param {Function} handler - 事件处理函数
     */
    static removeEventListener(element, event, handler) {
        if (element.removeEventListener) {
            element.removeEventListener(event, handler, false);
        } else if (element.detachEvent) {
            element.detachEvent('on' + event, handler);
        } else {
            element['on' + event] = null;
        }
    }

    /**
     * 跨浏览器请求动画帧
     * @param {Function} callback - 回调函数
     * @returns {number} 动画ID
     */
    static requestAnimationFrame(callback) {
        return (
            window.requestAnimationFrame ||
            window.webkitRequestAnimationFrame ||
            window.mozRequestAnimationFrame ||
            window.oRequestAnimationFrame ||
            window.msRequestAnimationFrame ||
            function(callback) {
                window.setTimeout(callback, 1000 / 60);
            }
        )(callback);
    }

    /**
     * 跨浏览器取消动画帧
     * @param {number} id - 动画ID
     */
    static cancelAnimationFrame(id) {
        (
            window.cancelAnimationFrame ||
            window.webkitCancelAnimationFrame ||
            window.mozCancelAnimationFrame ||
            window.oCancelAnimationFrame ||
            window.msCancelAnimationFrame ||
            window.clearTimeout
        )(id);
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceUtils;
    module.exports.default = PerformanceUtils;
} else if (typeof window !== 'undefined') {
    window.PerformanceUtils = PerformanceUtils;
}