/**
 * 统一场论可视化系统 - 工具函数库
 * 提供通用的数学计算、动画控制和3D渲染辅助功能
 */

class UTFUtils {
    /**
     * 格式化数字，保留指定小数位
     * @param {number} num - 要格式化的数字
     * @param {number} decimals - 小数位数
     * @returns {string} 格式化后的数字
     */
    static formatNumber(num, decimals = 2) {
        return Number(num).toFixed(decimals);
    }

    /**
     * 将3D坐标转换为屏幕坐标
     * @param {THREE.Vector3} position - 3D位置
     * @param {THREE.Camera} camera - 相机
     * @param {HTMLElement} container - 容器元素
     * @returns {Object} 屏幕坐标 {x, y}
     */
    static worldToScreen(position, camera, container) {
        const screenPosition = position.clone();
        screenPosition.project(camera);
        
        const rect = container.getBoundingClientRect();
        
        return {
            x: (screenPosition.x * 0.5 + 0.5) * rect.width + rect.left,
            y: (-screenPosition.y * 0.5 + 0.5) * rect.height + rect.top
        };
    }

    /**
     * 创建颜色渐变
     * @param {number} value - 0到1之间的值
     * @param {number} color1 - 起始颜色
     * @param {number} color2 - 结束颜色
     * @returns {number} 渐变后的颜色
     */
    static lerpColor(value, color1 = 0x165DFF, color2 = 0x7B61FF) {
        const r1 = (color1 >> 16) & 255;
        const g1 = (color1 >> 8) & 255;
        const b1 = color1 & 255;
        
        const r2 = (color2 >> 16) & 255;
        const g2 = (color2 >> 8) & 255;
        const b2 = color2 & 255;
        
        const r = Math.floor(r1 + (r2 - r1) * value);
        const g = Math.floor(g1 + (g2 - g1) * value);
        const b = Math.floor(b1 + (b2 - b1) * value);
        
        return (r << 16) + (g << 8) + b;
    }

    /**
     * 平滑动画函数 - 使用缓动方程
     * @param {number} t - 当前时间（0-1）
     * @param {string} easing - 缓动类型
     * @returns {number} 缓动后的值
     */
    static ease(t, easing = 'easeInOut') {
        switch(easing) {
            case 'easeIn':
                return t * t;
            case 'easeOut':
                return t * (2 - t);
            case 'easeInOut':
                return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
            case 'linear':
            default:
                return t;
        }
    }

    /**
     * 创建动画控制器
     * @param {Function} updateFn - 每帧更新函数
     * @param {number} duration - 动画持续时间（毫秒）
     * @param {Object} options - 配置选项
     * @returns {Object} 动画控制器
     */
    static createAnimation(updateFn, duration = 1000, options = {}) {
        const { easing = 'easeInOut', onComplete = null } = options;
        let startTime = null;
        let animationFrameId = null;
        let isPlaying = false;
        
        const animate = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const elapsed = timestamp - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = UTFUtils.ease(progress, easing);
            
            updateFn(easedProgress);
            
            if (progress < 1 && isPlaying) {
                animationFrameId = requestAnimationFrame(animate);
            } else if (progress >= 1 && onComplete) {
                onComplete();
            }
        };
        
        return {
            play: () => {
                if (isPlaying) return;
                isPlaying = true;
                startTime = null;
                animationFrameId = requestAnimationFrame(animate);
            },
            pause: () => {
                isPlaying = false;
                if (animationFrameId) {
                    cancelAnimationFrame(animationFrameId);
                }
            },
            stop: () => {
                isPlaying = false;
                if (animationFrameId) {
                    cancelAnimationFrame(animationFrameId);
                }
                updateFn(0);
            }
        };
    }

    /**
     * 计算两点之间的距离
     * @param {Object} point1 - 点1 {x, y, z}
     * @param {Object} point2 - 点2 {x, y, z}
     * @returns {number} 距离
     */
    static distance(point1, point2) {
        const dx = point2.x - point1.x;
        const dy = point2.y - point1.y;
        const dz = point2.z - point1.z;
        return Math.sqrt(dx * dx + dy * dy + dz * dz);
    }

    /**
     * 生成球体表面均匀分布的点
     * @param {number} radius - 球体半径
     * @param {number} count - 点的数量
     * @returns {Array} 点数组 [{x, y, z}]
     */
    static generateSpherePoints(radius = 1, count = 100) {
        const points = [];
        const phi = Math.PI * (3 - Math.sqrt(5)); // 黄金角
        
        for (let i = 0; i < count; i++) {
            const y = 1 - (i / (count - 1)) * 2; // y从1到-1
            const radius_at_y = Math.sqrt(1 - y * y); // 半径在当前y处
            
            const theta = phi * i; // 黄金角增量旋转
            
            const x = Math.cos(theta) * radius_at_y;
            const z = Math.sin(theta) * radius_at_y;
            
            points.push({
                x: x * radius,
                y: y * radius,
                z: z * radius
            });
        }
        
        return points;
    }

    /**
     * 解析数学表达式
     * @param {string} expression - 数学表达式
     * @param {Object} variables - 变量值对象
     * @returns {number|null} 计算结果
     */
    static evaluateExpression(expression, variables = {}) {
        try {
            // 简单的表达式解析器，替换变量后计算
            let evaluatedExpression = expression;
            
            // 替换变量
            Object.keys(variables).forEach(key => {
                const regex = new RegExp(key, 'g');
                evaluatedExpression = evaluatedExpression.replace(regex, variables[key]);
            });
            
            // 安全计算（使用Function而非eval以提供更好的上下文隔离）
            const result = new Function('return ' + evaluatedExpression)();
            return isFinite(result) ? result : null;
        } catch (error) {
            console.error('Expression evaluation error:', error);
            return null;
        }
    }

    /**
     * 渲染KaTeX数学公式
     * @param {string} latex - LaTeX公式
     * @param {HTMLElement} element - 目标元素
     * @param {Object} options - KaTeX选项
     * @returns {boolean} 是否成功
     */
    static renderKaTeX(latex, element, options = {}) {
        try {
            katex.render(latex, element, {
                throwOnError: false,
                displayMode: true,
                ...options
            });
            return true;
        } catch (error) {
            console.error('KaTeX rendering error:', error);
            return false;
        }
    }

    /**
     * 创建Three.js箭头
     * @param {THREE.Vector3} start - 起点
     * @param {THREE.Vector3} end - 终点
     * @param {Object} options - 配置选项
     * @returns {THREE.ArrowHelper} 箭头对象
     */
    static createArrow(start, end, options = {}) {
        const { 
            color = 0x165DFF, 
            headLength = 0.2, 
            headWidth = 0.1 
        } = options;
        
        const direction = new THREE.Vector3()
            .subVectors(end, start)
            .normalize();
        
        const length = new THREE.Vector3()
            .subVectors(end, start)
            .length();
        
        const arrow = new THREE.ArrowHelper(
            direction,
            start,
            length,
            color,
            headLength,
            headWidth
        );
        
        return arrow;
    }

    /**
     * 创建粒子系统
     * @param {number} count - 粒子数量
     * @param {Object} options - 配置选项
     * @returns {THREE.Points} 粒子系统
     */
    static createParticleSystem(count = 1000, options = {}) {
        const { 
            size = 0.05, 
            color = 0xffffff, 
            transparent = true, 
            opacity = 0.8,
            range = 100
        } = options;
        
        const particlesGeometry = new THREE.BufferGeometry();
        const positions = new Float32Array(count * 3);
        
        for (let i = 0; i < count * 3; i++) {
            positions[i] = (Math.random() - 0.5) * range;
        }
        
        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const particlesMaterial = new THREE.PointsMaterial({
            size,
            color,
            transparent,
            opacity
        });
        
        return new THREE.Points(particlesGeometry, particlesMaterial);
    }

    /**
     * 检测设备类型
     * @returns {Object} 设备信息 {isMobile, isTablet, isDesktop}
     */
    static detectDevice() {
        const width = window.innerWidth;
        return {
            isMobile: width < 768,
            isTablet: width >= 768 && width < 1024,
            isDesktop: width >= 1024
        }
    }

    /**
     * 添加防抖功能
     * @param {Function} func - 要防抖的函数
     * @param {number} wait - 等待时间（毫秒）
     * @returns {Function} 防抖后的函数
     */
    static debounce(func, wait = 300) {
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
     * 限制数值范围
     * @param {number} value - 输入值
     * @param {number} min - 最小值
     * @param {number} max - 最大值
     * @returns {number} 限制后的值
     */
    static clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }

    /**
     * 线性插值
     * @param {number} start - 起始值
     * @param {number} end - 结束值
     * @param {number} t - 插值因子（0-1）
     * @returns {number} 插值结果
     */
    static lerp(start, end, t) {
        return start + (end - start) * UTFUtils.clamp(t, 0, 1);
    }

    /**
     * 深拷贝对象
     * @param {Object} obj - 要拷贝的对象
     * @returns {Object} 拷贝后的对象
     */
    static deepClone(obj) {
        if (obj === null || typeof obj !== 'object') return obj;
        if (obj instanceof Date) return new Date(obj.getTime());
        if (obj instanceof Array) return obj.map(item => UTFUtils.deepClone(item));
        if (typeof obj === 'object') {
            const clonedObj = {};
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    clonedObj[key] = UTFUtils.deepClone(obj[key]);
                }
            }
            return clonedObj;
        }
    }

    /**
     * 检测浏览器是否支持WebGL
     * @returns {boolean} 是否支持
     */
    static isWebGLSupported() {
        try {
            const canvas = document.createElement('canvas');
            return !!(window.WebGLRenderingContext && 
                (canvas.getContext('webgl') || 
                 canvas.getContext('experimental-webgl')));
        } catch (e) {
            return false;
        }
    }

    /**
     * 显示错误消息
     * @param {string} message - 错误消息
     * @param {string} type - 消息类型 (error, warning, info)
     */
    static showNotification(message, type = 'info') {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 translate-y-16 opacity-0 z-50`;
        
        // 设置样式根据类型
        switch(type) {
            case 'error':
                notification.classList.add('bg-red-500', 'text-white');
                break;
            case 'warning':
                notification.classList.add('bg-amber-500', 'text-white');
                break;
            case 'info':
            default:
                notification.classList.add('bg-primary', 'text-white');
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // 显示动画
        setTimeout(() => {
            notification.classList.remove('translate-y-16', 'opacity-0');
        }, 10);
        
        // 自动消失
        setTimeout(() => {
            notification.classList.add('translate-y-16', 'opacity-0');
            setTimeout(() => {
                if (notification.parentNode) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    /**
     * 初始化统一的Three.js场景
     * @param {HTMLElement} container - 容器元素
     * @param {Object} options - 配置选项
     * @returns {Object} 场景对象 {scene, camera, renderer, controls}
     */
    static initThreeScene(container, options = {}) {
        const {
            backgroundColor = 0x050a15,
            cameraPosition = { x: 5, y: 5, z: 5 },
            cameraLookAt = { x: 0, y: 0, z: 0 },
            enableGrid = true,
            enableAxes = true
        } = options;
        
        // 创建场景
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(backgroundColor);
        
        // 创建相机
        const camera = new THREE.PerspectiveCamera(
            75,
            container.clientWidth / container.clientHeight,
            0.1,
            1000
        );
        camera.position.set(cameraPosition.x, cameraPosition.y, cameraPosition.z);
        camera.lookAt(cameraLookAt.x, cameraLookAt.y, cameraLookAt.z);
        
        // 创建渲染器
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);
        
        // 创建控制器
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        
        // 添加网格
        if (enableGrid) {
            const gridHelper = new THREE.GridHelper(10, 10, 0x333333, 0x222222);
            scene.add(gridHelper);
        }
        
        // 添加坐标轴
        if (enableAxes) {
            const axesHelper = new THREE.AxesHelper(5);
            scene.add(axesHelper);
        }
        
        // 响应式处理
        const handleResize = UTFUtils.debounce(() => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }, 100);
        
        window.addEventListener('resize', handleResize);
        
        return {
            scene,
            camera,
            renderer,
            controls,
            cleanup: () => window.removeEventListener('resize', handleResize)
        }
    }
}

// 导出UTFUtils类
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = UTFUtils;
} else if (typeof window !== 'undefined') {
    window.UTFUtils = UTFUtils;
}