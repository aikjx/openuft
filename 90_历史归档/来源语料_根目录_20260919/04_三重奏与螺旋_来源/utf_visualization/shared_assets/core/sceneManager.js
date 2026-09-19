/**
 * Three.js场景管理类
 */
class SceneManager {
    /**
     * 构造函数
     * @param {HTMLElement} container - 容器元素
     * @param {Object} options - 配置选项
     */
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            antialias: true,
            powerPreference: 'high-performance',
            backgroundColor: 0xf8fafc,
            showAxes: true,
            showGrid: true,
            enableOrbitControls: true,
            ...options
        };
        
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.animationId = null;
        this.isAnimating = false;
        
        this.init();
    }
    
    /**
     * 初始化场景
     */
    init() {
        try {
            // 检测浏览器兼容性
            const browserInfo = PerformanceUtils ? PerformanceUtils.detectBrowserCompatibility() : {
                supportedFeatures: { webgl: true }
            };
            
            // 检查WebGL支持
            if (!browserInfo.supportedFeatures.webgl) {
                this.showCompatibilityWarning('您的浏览器不支持WebGL，无法显示3D可视化效果');
                return;
            }
            
            // 创建场景
            this.scene = new THREE.Scene();
            this.scene.background = new THREE.Color(this.options.backgroundColor);
            
            // 创建相机
            const aspectRatio = this.container.clientWidth / this.container.clientHeight;
            this.camera = new THREE.PerspectiveCamera(75, aspectRatio, 0.1, 1000);
            this.camera.position.z = 5;
            
            // 创建渲染器
            try {
                this.renderer = new THREE.WebGLRenderer({
                    antialias: this.options.antialias,
                    powerPreference: this.options.powerPreference
                });
                this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
                this.container.appendChild(this.renderer.domElement);
            } catch (e) {
                console.error('WebGL渲染器初始化失败:', e);
                this.showCompatibilityWarning('WebGL渲染器初始化失败，请尝试更新浏览器');
                return;
            }
            
            // 初始化场景元素
            this.initSceneElements();
        } catch (e) {
            console.error('场景初始化失败:', e);
            this.showCompatibilityWarning('场景初始化失败，请尝试使用现代浏览器');
        }
    }
    
    /**
     * 初始化场景元素
     */
    initSceneElements() {
        // 添加坐标轴
        if (this.options.showAxes && this.scene) {
            const axesHelper = new THREE.AxesHelper(5);
            axesHelper.material.opacity = 0.7;
            axesHelper.material.transparent = true;
            this.scene.add(axesHelper);
        }
        
        // 添加网格
        if (this.options.showGrid && this.scene) {
            const gridHelper = new THREE.GridHelper(10, 10);
            gridHelper.material.opacity = 0.5;
            gridHelper.material.transparent = true;
            this.scene.add(gridHelper);
        }
        
        // 添加轨道控制器
        if (this.options.enableOrbitControls && this.camera && this.renderer) {
            try {
                this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
                this.controls.enableDamping = true;
                this.controls.dampingFactor = 0.05;
                this.controls.maxDistance = 15;
                this.controls.minDistance = 1;
            } catch (e) {
                console.error('轨道控制器初始化失败:', e);
            }
        }
        
        // 响应式处理
        this.handleResize = PerformanceUtils ? PerformanceUtils.debounce(() => {
            this.resize();
        }, 100) : () => {
            this.resize();
        };
        
        // 使用跨浏览器事件监听
        if (PerformanceUtils) {
            PerformanceUtils.addEventListener(window, 'resize', this.handleResize);
        } else {
            window.addEventListener('resize', this.handleResize);
        }
    }
    
    /**
     * 显示兼容性警告
     * @param {string} message - 警告消息
     */
    showCompatibilityWarning(message) {
        const warningElement = document.createElement('div');
        warningElement.className = 'fixed top-0 left-0 right-0 bg-warning text-white p-4 z-50 text-center';
        warningElement.style.backgroundColor = '#ff6b35';
        warningElement.style.color = 'white';
        warningElement.style.padding = '12px';
        warningElement.style.textAlign = 'center';
        warningElement.style.zIndex = '1000';
        warningElement.style.fontFamily = 'Arial, sans-serif';
        warningElement.innerHTML = `
            <div style="max-width: 800px; margin: 0 auto;">
                <i class="fa fa-exclamation-triangle mr-2"></i>
                ${message}
                <button onclick="this.parentElement.parentElement.remove()" style="margin-left: 10px; background: rgba(255,255,255,0.2); border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;">
                    关闭
                </button>
            </div>
        `;
        document.body.appendChild(warningElement);
    }
    
    /**
     * 开始动画循环
     * @param {Function} updateCallback - 每帧更新回调
     */
    startAnimation(updateCallback = null) {
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        let lastTime = performance.now();
        
        const animate = (timestamp) => {
            const delta = timestamp - lastTime;
            lastTime = timestamp;
            
            // 更新控制器
            if (this.controls) {
                this.controls.update();
            }
            
            // 执行回调
            if (updateCallback) {
                updateCallback(delta);
            }
            
            // 渲染场景
            if (this.renderer && this.scene && this.camera) {
                this.renderer.render(this.scene, this.camera);
            }
            
            // 检查元素是否可见
            if (PerformanceUtils && !PerformanceUtils.isElementInViewport(this.container)) {
                this.isAnimating = false;
                setTimeout(() => {
                    if (PerformanceUtils && PerformanceUtils.isElementInViewport(this.container)) {
                        this.startAnimation(updateCallback);
                    }
                }, 1000);
                return;
            }
            
            if (this.isAnimating) {
                this.animationId = PerformanceUtils ? PerformanceUtils.requestAnimationFrame(animate) : requestAnimationFrame(animate);
            }
        };
        
        this.animationId = PerformanceUtils ? PerformanceUtils.requestAnimationFrame(animate) : requestAnimationFrame(animate);
    }
    
    /**
     * 停止动画循环
     */
    stopAnimation() {
        if (this.animationId) {
            if (PerformanceUtils) {
                PerformanceUtils.cancelAnimationFrame(this.animationId);
            } else {
                cancelAnimationFrame(this.animationId);
            }
            this.animationId = null;
        }
        this.isAnimating = false;
    }
    
    /**
     * 调整大小
     */
    resize() {
        if (!this.camera || !this.renderer) return;
        
        const aspectRatio = this.container.clientWidth / this.container.clientHeight;
        this.camera.aspect = aspectRatio;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    /**
     * 添加对象到场景
     * @param {THREE.Object3D} object - 要添加的对象
     */
    add(object) {
        if (this.scene) {
            this.scene.add(object);
        }
    }
    
    /**
     * 从场景中移除对象
     * @param {THREE.Object3D} object - 要移除的对象
     */
    remove(object) {
        if (this.scene && object) {
            this.scene.remove(object);
        }
    }
    
    /**
     * 清理资源
     */
    dispose() {
        // 停止动画
        this.stopAnimation();
        
        // 移除事件监听器
        if (this.handleResize) {
            if (PerformanceUtils) {
                PerformanceUtils.removeEventListener(window, 'resize', this.handleResize);
            } else {
                window.removeEventListener('resize', this.handleResize);
            }
        }
        
        // 清理渲染器
        if (this.renderer) {
            this.renderer.dispose();
        }
        
        // 清理场景中的对象
        if (this.scene) {
            while (this.scene.children.length > 0) {
                const child = this.scene.children[0];
                this.remove(child);
                
                // 清理几何体和材质
                if (child.geometry) {
                    child.geometry.dispose();
                }
                if (child.material) {
                    if (Array.isArray(child.material)) {
                        child.material.forEach(material => material.dispose());
                    } else {
                        child.material.dispose();
                    }
                }
            }
        }
        
        // 清理引用
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
    }
    
    /**
     * 获取场景
     * @returns {THREE.Scene} 场景对象
     */
    getScene() {
        return this.scene;
    }
    
    /**
     * 获取相机
     * @returns {THREE.Camera} 相机对象
     */
    getCamera() {
        return this.camera;
    }
    
    /**
     * 获取渲染器
     * @returns {THREE.WebGLRenderer} 渲染器对象
     */
    getRenderer() {
        return this.renderer;
    }
    
    /**
     * 获取控制器
     * @returns {THREE.OrbitControls} 控制器对象
     */
    getControls() {
        return this.controls;
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SceneManager;
    module.exports.default = SceneManager;
} else if (typeof window !== 'undefined') {
    window.SceneManager = SceneManager;
}