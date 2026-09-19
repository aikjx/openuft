/**
 * 可视化对象管理类
 */
class VisualizationManager {
    /**
     * 构造函数
     * @param {SceneManager} sceneManager - 场景管理器实例
     */
    constructor(sceneManager) {
        this.sceneManager = sceneManager;
        this.visualizationObjects = {};
        this.currentEquation = null;
    }
    
    /**
     * 加载方程可视化
     * @param {string} equation - 方程类型
     * @param {Object} params - 可视化参数
     */
    loadEquation(equation, params = {}) {
        this.currentEquation = equation;
        
        // 清理现有对象
        this.cleanup();
        
        // 根据方程类型创建可视化
        switch(equation) {
            case 'spaceTime':
                this.createSpaceTimeVisualization(params);
                break;
            case 'momentum':
                this.createMomentumVisualization(params);
                break;
            case 'energy':
                this.createEnergyVisualization(params);
                break;
            case 'field':
                this.createFieldVisualization(params);
                break;
            case 'gravity':
                this.createGravityVisualization(params);
                break;
            default:
                console.warn(`Unknown equation type: ${equation}`);
        }
    }
    
    /**
     * 创建时空同一化方程可视化
     * @param {Object} params - 参数
     */
    createSpaceTimeVisualization(params = {}) {
        // 创建光锥
        const coneGeometry = new THREE.ConeGeometry(2, 4, 32);
        const coneMaterial = new THREE.MeshBasicMaterial({ 
            color: 0x165DFF, 
            transparent: true, 
            opacity: 0.3, 
            side: THREE.DoubleSide 
        });
        const lightCone = new THREE.Mesh(coneGeometry, coneMaterial);
        lightCone.rotation.x = Math.PI / 2;
        this.sceneManager.add(lightCone);
        this.visualizationObjects.lightCone = lightCone;
        
        // 创建空间点
        const pointGeometry = new THREE.SphereGeometry(0.1, 16, 16);
        const pointMaterial = new THREE.MeshBasicMaterial({ color: 0xFF6B8B });
        const spacePoint = new THREE.Mesh(pointGeometry, pointMaterial);
        this.sceneManager.add(spacePoint);
        this.visualizationObjects.spacePoint = spacePoint;
        
        // 创建世界线
        const curve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, 0, 3)
        ]);
        const lineGeometry = new THREE.TubeGeometry(curve, 100, 0.05, 8, false);
        const lineMaterial = new THREE.MeshBasicMaterial({ color: 0x7B61FF });
        const worldLine = new THREE.Mesh(lineGeometry, lineMaterial);
        this.sceneManager.add(worldLine);
        this.visualizationObjects.worldLine = worldLine;
    }
    
    /**
     * 创建动量公式可视化
     * @param {Object} params - 参数
     */
    createMomentumVisualization(params = {}) {
        // 创建光速矢量
        const cArrow = this.createArrow(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, 3), 0x165DFF);
        this.sceneManager.add(cArrow);
        this.visualizationObjects.cArrow = cArrow;
        
        // 创建速度矢量
        const vArrow = this.createArrow(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, -1), 0xFF6B8B);
        this.sceneManager.add(vArrow);
        this.visualizationObjects.vArrow = vArrow;
        
        // 创建动量矢量
        const pArrow = this.createArrow(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, 4), 0x7B61FF);
        this.sceneManager.add(pArrow);
        this.visualizationObjects.pArrow = pArrow;
    }
    
    /**
     * 创建能量方程可视化
     * @param {Object} params - 参数
     */
    createEnergyVisualization(params = {}) {
        // 创建能量球体
        const sphereGeometry = new THREE.SphereGeometry(1, 32, 32);
        const sphereMaterial = new THREE.MeshBasicMaterial({ 
            color: 0xFF6B8B, 
            transparent: true, 
            opacity: 0.7 
        });
        const energySphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
        this.sceneManager.add(energySphere);
        this.visualizationObjects.energySphere = energySphere;
        
        // 创建能量场线
        const fieldLines = [];
        for (let i = 0; i < 20; i++) {
            const angle = (i / 20) * Math.PI * 2;
            const radius = 1.5;
            const lineGeometry = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(radius * Math.cos(angle), 0, radius * Math.sin(angle)),
                new THREE.Vector3(radius * 1.8 * Math.cos(angle), 0, radius * 1.8 * Math.sin(angle))
            ]);
            const lineMaterial = new THREE.LineBasicMaterial({ color: 0x165DFF });
            const line = new THREE.Line(lineGeometry, lineMaterial);
            this.sceneManager.add(line);
            fieldLines.push(line);
        }
        this.visualizationObjects.fieldLines = fieldLines;
    }
    
    /**
     * 创建电场与磁场关系可视化
     * @param {Object} params - 参数
     */
    createFieldVisualization(params = {}) {
        // 创建电场环
        const eGeometry = new THREE.TorusGeometry(1, 0.05, 16, 100);
        const eMaterial = new THREE.MeshBasicMaterial({ color: 0x165DFF });
        const electricField = new THREE.Mesh(eGeometry, eMaterial);
        this.sceneManager.add(electricField);
        this.visualizationObjects.electricField = electricField;
        
        // 创建磁场线
        const bLines = [];
        for (let i = 0; i < 10; i++) {
            const height = -1 + (i / 9) * 2;
            const lineGeometry = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(-1.5, height, 0),
                new THREE.Vector3(1.5, height, 0)
            ]);
            const lineMaterial = new THREE.LineBasicMaterial({ color: 0xFF6B8B });
            const line = new THREE.Line(lineGeometry, lineMaterial);
            this.sceneManager.add(line);
            bLines.push(line);
        }
        this.visualizationObjects.magneticField = bLines;
    }
    
    /**
     * 创建引力场方程可视化
     * @param {Object} params - 参数
     */
    createGravityVisualization(params = {}) {
        // 创建质量源
        const massGeometry = new THREE.SphereGeometry(0.5, 32, 32);
        const massMaterial = new THREE.MeshBasicMaterial({ color: 0x1E293B });
        const massSource = new THREE.Mesh(massGeometry, massMaterial);
        this.sceneManager.add(massSource);
        this.visualizationObjects.massSource = massSource;
        
        // 创建引力场线
        const gravityLines = [];
        for (let i = 0; i < 12; i++) {
            const phi = (i / 12) * Math.PI * 2;
            for (let j = 0; j < 6; j++) {
                const theta = (j / 6) * Math.PI;
                const curve = new THREE.CatmullRomCurve3([
                    new THREE.Vector3(
                        2 * Math.sin(theta) * Math.cos(phi),
                        2 * Math.cos(theta),
                        2 * Math.sin(theta) * Math.sin(phi)
                    ),
                    new THREE.Vector3(
                        0.6 * Math.sin(theta) * Math.cos(phi),
                        0.6 * Math.cos(theta),
                        0.6 * Math.sin(theta) * Math.sin(phi)
                    )
                ]);
                const lineGeometry = new THREE.TubeGeometry(curve, 50, 0.02, 8, false);
                const lineMaterial = new THREE.MeshBasicMaterial({ 
                    color: 0x7B61FF,
                    transparent: true,
                    opacity: 0.8
                });
                const line = new THREE.Mesh(lineGeometry, lineMaterial);
                this.sceneManager.add(line);
                gravityLines.push(line);
            }
        }
        this.visualizationObjects.gravityLines = gravityLines;
    }
    
    /**
     * 创建箭头
     * @param {THREE.Vector3} start - 起点
     * @param {THREE.Vector3} end - 终点
     * @param {number} color - 颜色
     * @returns {THREE.ArrowHelper} 箭头对象
     */
    createArrow(start, end, color) {
        const direction = new THREE.Vector3().subVectors(end, start);
        const length = direction.length();
        
        const arrowHelper = new THREE.ArrowHelper(
            direction.normalize(),
            start,
            length,
            color,
            length * 0.2,
            length * 0.1
        );
        
        return arrowHelper;
    }
    
    /**
     * 更新可视化
     * @param {Object} params - 更新参数
     */
    update(params = {}) {
        const { velocity = 0.1, mass = 1, time = 0 } = params;
        
        switch(this.currentEquation) {
            case 'spaceTime':
                if (this.visualizationObjects.spacePoint) {
                    this.visualizationObjects.spacePoint.position.set(0, 0, time * 0.3);
                }
                break;
            case 'momentum':
                if (this.visualizationObjects.vArrow && this.visualizationObjects.pArrow) {
                    const vLength = parseFloat(velocity) * 3;
                    const pLength = parseFloat(mass) * (3 - vLength);
                    
                    this.visualizationObjects.vArrow.setLength(vLength);
                    this.visualizationObjects.pArrow.setLength(pLength);
                }
                break;
            case 'energy':
                if (this.visualizationObjects.energySphere) {
                    this.visualizationObjects.energySphere.scale.set(parseFloat(mass), parseFloat(mass), parseFloat(mass));
                }
                break;
            case 'field':
                if (this.visualizationObjects.electricField) {
                    this.visualizationObjects.electricField.rotation.x = time * 0.2;
                }
                break;
            case 'gravity':
                if (this.visualizationObjects.massSource) {
                    this.visualizationObjects.massSource.scale.set(parseFloat(mass), parseFloat(mass), parseFloat(mass));
                }
                break;
        }
    }
    
    /**
     * 清理所有可视化对象
     */
    cleanup() {
        Object.values(this.visualizationObjects).forEach(obj => {
            if (Array.isArray(obj)) {
                obj.forEach(item => {
                    this.removeObject(item);
                });
            } else {
                this.removeObject(obj);
            }
        });
        this.visualizationObjects = {};
    }
    
    /**
     * 移除单个对象
     * @param {THREE.Object3D} obj - 要移除的对象
     */
    removeObject(obj) {
        if (obj && obj.parent) {
            this.sceneManager.remove(obj);
            
            // 清理几何体和材质
            if (obj.geometry) {
                obj.geometry.dispose();
            }
            if (obj.material) {
                if (Array.isArray(obj.material)) {
                    obj.material.forEach(material => material.dispose());
                } else {
                    obj.material.dispose();
                }
            }
        }
    }
    
    /**
     * 获取当前方程
     * @returns {string} 当前方程类型
     */
    getCurrentEquation() {
        return this.currentEquation;
    }
    
    /**
     * 获取可视化对象
     * @param {string} key - 对象键名
     * @returns {THREE.Object3D|Array} 可视化对象
     */
    getObject(key) {
        return this.visualizationObjects[key];
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VisualizationManager;
    module.exports.default = VisualizationManager;
} else if (typeof window !== 'undefined') {
    window.VisualizationManager = VisualizationManager;
}