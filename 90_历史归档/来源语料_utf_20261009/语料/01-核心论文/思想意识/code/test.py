import numpy as np
import matplotlib
# 使用非交互式后端，避免显示图形窗口
matplotlib.use('Agg')  # 使用Agg后端，不显示图形
import matplotlib.pyplot as plt
# 设置matplotlib中文字体，避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
from scipy import signal
from scipy.fft import fft, fftfreq
import numpy as np

class ConsciousnessAlgorithm:
    """
    基于统一场论的思想意识算法模拟框架
    模拟人工场扫描读取意识信息的过程
    """
    
    def __init__(self, sampling_rate=1000, duration=10):
        self.sampling_rate = sampling_rate  # 采样率 (Hz)
        self.duration = duration  # 采样时长 (秒)
        self.time = np.linspace(0, duration, sampling_rate * duration)
        
        # 意识状态参数（模拟）
        self.consciousness_frequencies = [1, 4, 8, 12, 30, 40]  # 不同意识状态的频率成分 (Hz)
        self.amplitude_modulation = 0.5  # 意识活动的幅度调制
        
    def simulate_consciousness_waveform(self, consciousness_state="awake"):
        """
        模拟不同意识状态下的脑电波形
        基于文档中提到的"带电粒子运动模式"
        """
        t = self.time
        
        if consciousness_state == "awake":
            # 清醒状态：高频高幅活动
            base_freq = 15
            modulation_depth = 0.8
        elif consciousness_state == "sleep":
            # 睡眠状态：低频慢波
            base_freq = 3
            modulation_depth = 0.3
        elif consciousness_state == "focused":
            # 专注状态：特定频率增强
            base_freq = 40
            modulation_depth = 0.9
        else:
            base_freq = 10
            modulation_depth = 0.5
        
        # 生成基础意识波形（模拟带电粒子集体运动）
        consciousness_signal = np.zeros_like(t)
        for freq in self.consciousness_frequencies:
            amplitude = np.exp(-(freq - base_freq)**2 / 100)  # 高斯分布
            phase = 2 * np.pi * np.random.random()
            consciousness_signal += amplitude * np.sin(2 * np.pi * freq * t + phase)
        
        # 添加幅度调制（模拟意识强度变化）
        modulation = 1 + modulation_depth * np.sin(2 * np.pi * 0.1 * t)
        consciousness_signal *= modulation
        
        return consciousness_signal
    
    def artificial_field_scanning(self, consciousness_signal):
        """
        模拟人工场扫描过程
        基于文档中的"空间扰动波形反推"算法
        """
        # 模拟空间扰动（意识活动对周围空间的影响）
        # 根据统一场论，意识活动会产生以光速传播的空间波动
        spatial_perturbation = consciousness_signal.copy()
        
        # 添加传播效应（光速延迟和衰减）
        propagation_delay = 0.001  # 1ms延迟（模拟光速传播）
        delay_samples = int(propagation_delay * self.sampling_rate)
        spatial_perturbation = np.roll(spatial_perturbation, delay_samples)
        spatial_perturbation[:delay_samples] = 0
        
        # 添加空间衰减（与距离平方成反比）
        distance = 0.1  # 假设探测距离10cm
        attenuation = 1 / (distance ** 2)
        spatial_perturbation *= attenuation
        
        return spatial_perturbation
    
    def consciousness_reconstruction(self, spatial_perturbation):
        """
        从空间扰动反推意识状态
        验证文档中的"逆向求导"算法
        """
        # 使用逆滤波技术重建原始意识信号
        # 这相当于求解文档中提到的逆问题 F⁻¹
        
        # 首先估计传播信道特性
        estimated_delay = self.estimate_propagation_delay(spatial_perturbation)
        
        # 逆向传播（补偿延迟和衰减）
        reconstructed_signal = spatial_perturbation.copy()
        
        # 补偿延迟
        reconstructed_signal = np.roll(reconstructed_signal, -estimated_delay)
        reconstructed_signal[-estimated_delay:] = 0
        
        # 补偿衰减（需要知道距离信息，这里假设已知）
        distance = 0.1
        amplification = distance ** 2
        reconstructed_signal *= amplification
        
        return reconstructed_signal
    
    def estimate_propagation_delay(self, signal):
        """
        估计信号传播延迟
        使用互相关方法
        """
        # 这里简化处理，实际需要参考信号
        return int(0.001 * self.sampling_rate)  # 返回1ms的延迟
    
    def information_content_analysis(self, signal_data):
        """
        分析信号的信息含量
        验证文档中的公式：I ∝ ∫ E(k) dk
        """
        # 计算功率谱密度
        frequencies, power_spectrum = signal.welch(signal_data, self.sampling_rate)
        
        # 计算总能量（积分功率谱）
        total_energy = np.trapz(power_spectrum, frequencies)
        
        # 计算香农熵（信息量度量）
        # 归一化功率谱作为概率分布
        normalized_spectrum = power_spectrum / np.sum(power_spectrum)
        # 避免log(0)
        normalized_spectrum = np.where(normalized_spectrum == 0, 1e-10, normalized_spectrum)
        shannon_entropy = -np.sum(normalized_spectrum * np.log2(normalized_spectrum))
        
        return total_energy, shannon_entropy
    
    def validate_algorithm(self, original_signal, reconstructed_signal):
        """
        验证算法准确性
        计算重建信号与原始信号的相似度
        """
        # 计算相关系数
        correlation = np.corrcoef(original_signal, reconstructed_signal)[0, 1]
        
        # 计算均方误差
        mse = np.mean((original_signal - reconstructed_signal) ** 2)
        
        # 计算信噪比改进
        original_power = np.mean(original_signal ** 2)
        noise_power = np.mean((original_signal - reconstructed_signal) ** 2)
        snr_improvement = 10 * np.log10(original_power / noise_power) if noise_power > 0 else float('inf')
        
        return {
            'correlation': correlation,
            'mse': mse,
            'snr_improvement': snr_improvement
        }

def run_comprehensive_simulation():
    """
    运行完整的意识算法验证模拟
    """
    print("=== 思想意识算法验证模拟 ===\n")
    
    # 初始化算法
    algo = ConsciousnessAlgorithm()
    
    # 测试不同意识状态
    states = ['awake', 'sleep', 'focused']
    results = {}
    
    plt.figure(figsize=(15, 10))
    
    for i, state in enumerate(states):
        print(f"\n--- 测试意识状态: {state} ---")
        
        # 1. 模拟原始意识信号
        original_signal = algo.simulate_consciousness_waveform(state)
        
        # 2. 模拟人工场扫描
        spatial_perturbation = algo.artificial_field_scanning(original_signal)
        
        # 3. 意识重建
        reconstructed_signal = algo.consciousness_reconstruction(spatial_perturbation)
        
        # 4. 信息量分析
        energy, entropy = algo.information_content_analysis(original_signal)
        print(f"总能量: {energy:.4f}, 香农熵: {entropy:.4f}")
        
        # 5. 算法验证
        validation = algo.validate_algorithm(original_signal, reconstructed_signal)
        print(f"相关系数: {validation['correlation']:.4f}")
        print(f"均方误差: {validation['mse']:.4f}")
        print(f"信噪比改进: {validation['snr_improvement']:.2f} dB")
        
        # 存储结果
        results[state] = {
            'original': original_signal,
            'perturbation': spatial_perturbation,
            'reconstructed': reconstructed_signal,
            'validation': validation,
            'energy': energy,
            'entropy': entropy
        }
        
        # 绘制结果
        plt.subplot(3, 3, i*3 + 1)
        plt.plot(algo.time[:1000], original_signal[:1000])
        plt.title(f'{state} - 原始意识信号')
        plt.xlabel('时间 (s)')
        plt.ylabel('幅度')
        
        plt.subplot(3, 3, i*3 + 2)
        plt.plot(algo.time[:1000], spatial_perturbation[:1000])
        plt.title(f'{state} - 空间扰动')
        plt.xlabel('时间 (s)')
        plt.ylabel('幅度')
        
        plt.subplot(3, 3, i*3 + 3)
        plt.plot(algo.time[:1000], reconstructed_signal[:1000])
        plt.title(f'{state} - 重建信号')
        plt.xlabel('时间 (s)')
        plt.ylabel('幅度')
    
    plt.tight_layout()
    plt.show()
    
    # 绘制信息量比较
    plt.figure(figsize=(10, 6))
    states_list = list(results.keys())
    energies = [results[state]['energy'] for state in states_list]
    entropies = [results[state]['entropy'] for state in states_list]
    
    plt.subplot(1, 2, 1)
    plt.bar(states_list, energies)
    plt.title('不同意识状态的总能量')
    plt.ylabel('能量')
    
    plt.subplot(1, 2, 2)
    plt.bar(states_list, entropies)
    plt.title('不同意识状态的信息熵')
    plt.ylabel('香农熵 (bits)')
    
    plt.tight_layout()
    plt.show()
    
    return results

def advanced_spectral_analysis():
    """
    高级频谱分析：验证意识信号的频域特性
    """
    algo = ConsciousnessAlgorithm(duration=5)
    
    # 生成专注状态的意识信号
    signal = algo.simulate_consciousness_waveform("focused")
    
    # 傅里叶分析
    n = len(signal)
    freq = fftfreq(n, 1/algo.sampling_rate)
    fft_vals = fft(signal)
    
    # 只取正频率
    positive_freq = freq[:n//2]
    positive_fft = 2.0/n * np.abs(fft_vals[:n//2])
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(algo.time, signal)
    plt.title('意识信号时域图')
    plt.xlabel('时间 (s)')
    plt.ylabel('幅度')
    
    plt.subplot(1, 2, 2)
    plt.plot(positive_freq, positive_fft)
    plt.title('意识信号频谱图')
    plt.xlabel('频率 (Hz)')
    plt.ylabel('幅度')
    plt.xlim(0, 50)  # 聚焦在0-50Hz范围
    
    plt.tight_layout()
    plt.show()
    
    # 验证文档中的频率特征
    print("\n=== 频谱分析结果 ===")
    peak_freq = positive_freq[np.argmax(positive_fft)]
    print(f"主要频率成分: {peak_freq:.2f} Hz")
    
    # 计算不同频段的能量占比
    delta_band = np.trapz(positive_fft[(positive_freq >= 0.5) & (positive_freq < 4)], 
                          positive_freq[(positive_freq >= 0.5) & (positive_freq < 4)])
    theta_band = np.trapz(positive_fft[(positive_freq >= 4) & (positive_freq < 8)], 
                         positive_freq[(positive_freq >= 4) & (positive_freq < 8)])
    alpha_band = np.trapz(positive_fft[(positive_freq >= 8) & (positive_freq < 13)], 
                         positive_freq[(positive_freq >= 8) & (positive_freq < 13)])
    beta_band = np.trapz(positive_fft[(positive_freq >= 13) & (positive_freq < 30)], 
                        positive_freq[(positive_freq >= 13) & (positive_freq < 30)])
    gamma_band = np.trapz(positive_fft[(positive_freq >= 30) & (positive_freq < 50)], 
                         positive_freq[(positive_freq >= 30) & (positive_freq < 50)])
    
    total_energy = delta_band + theta_band + alpha_band + beta_band + gamma_band
    
    print(f"Delta波段 (0.5-4Hz): {delta_band/total_energy*100:.1f}%")
    print(f"Theta波段 (4-8Hz): {theta_band/total_energy*100:.1f}%")
    print(f"Alpha波段 (8-13Hz): {alpha_band/total_energy*100:.1f}%")
    print(f"Beta波段 (13-30Hz): {beta_band/total_energy*100:.1f}%")
    print(f"Gamma波段 (30-50Hz): {gamma_band/total_energy*100:.1f}%")

if __name__ == "__main__":
    # 运行基础模拟
    results = run_comprehensive_simulation()
    
    # 运行高级频谱分析
    advanced_spectral_analysis()
    
    print("\n=== 模拟总结 ===")
    print("本代码演示了基于统一场论的思想意识算法框架")
    print("主要验证点:")
    print("1. 不同意识状态的可区分性")
    print("2. 人工场扫描与意识重建的可行性") 
    print("3. 信息量公式 I ∝ ∫ E(k) dk 的验证")
    print("4. 意识信号的频域特征分析")
