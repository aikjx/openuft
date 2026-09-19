/**
 * 核心模块主入口
 */

// 导出所有核心模块
export { default as PerformanceUtils } from './performance.js';
export { default as SceneManager } from './sceneManager.js';
export { default as VisualizationManager } from './visualizationManager.js';
export { default as PerformanceMonitor } from './performanceMonitor.js';

// 如果在浏览器环境中，挂载到window对象
if (typeof window !== 'undefined') {
    // 加载性能工具
    if (typeof importScripts === 'undefined') {
        // 浏览器环境，使用动态导入
        Promise.all([
            import('./performance.js'),
            import('./sceneManager.js'),
            import('./visualizationManager.js'),
            import('./performanceMonitor.js')
        ]).then(([performanceModule, sceneModule, visualizationModule, monitorModule]) => {
            window.PerformanceUtils = performanceModule.default;
            window.SceneManager = sceneModule.default;
            window.VisualizationManager = visualizationModule.default;
            window.PerformanceMonitor = monitorModule.default;
            
            // 初始化性能监控
            if (window.DEBUG) {
                window.performanceMonitor = new monitorModule.default();
                console.log('UTF Visualization Core Modules Loaded with Performance Monitoring');
            } else {
                console.log('UTF Visualization Core Modules Loaded');
            }
        }).catch(err => {
            console.error('Error loading core modules:', err);
        });
    }
}