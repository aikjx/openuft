# -*- coding: utf-8 -*-
# 设置中文字体支持 - Windows系统通用字体
import matplotlib
matplotlib.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
matplotlib.rcParams["text.usetex"] = False  # 使用 Matplotlib 的内置渲染
matplotlib.rcParams["mathtext.fontset"] = "cm"  # 使用 CMU Serif 字体渲染数学公式
# -*- coding: utf-8 -*-
# 设置中文字体支持 - Windows系统通用字体
import matplotlib
matplotlib.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
# -*- coding: utf-8 -*-
# 设置中文字体支持 - Windows系统通用字体
import matplotlib
matplotlib.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "NSimSun"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
# -*- coding: utf-8 -*-
# 设置中文字体支持
import matplotlib
matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial Unicode MS"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
from manim import *
import numpy as np

class SpaceTimeUnification(ThreeDScene):
    def construct(self):
        # ========== 超酷炫开场 ==========
        self.camera.background_color = "#0a0a0a"
        
        # 全息网格背景
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            }
        )
        grid.set_opacity(0.2)
        self.add(grid)
        
        # ========== 表格标题 ==========
        table_header = VGroup(
            Text("1", font="Consolas", weight=BOLD, font_size=40, color="#00ff41"),
            Text("时空同一化方程", font="Noto Sans SC", weight=BOLD, font_size=40, color="#00d4ff"),
        ).arrange(RIGHT, buff=0.5)
        table_header.to_edge(UP, buff=0.3)
        
        # 霓虹边框
        header_box = SurroundingRectangle(
            table_header,
            color="#00ff41",
            buff=0.2,
            corner_radius=0.15,
            stroke_width=3
        )
        header_glow = header_box.copy().set_stroke(color="#00ff41", width=15, opacity=0.3)
        
        self.play(
            Create(header_glow),
            Create(header_box),
            Write(table_header),
            run_time=1.5
        )
        self.wait(0.3)
        
        # ========== 主方程 100% 精确还原 ==========
        main_equation = MathTex(
            r"\vec{r}(t)", r"=", r"\vec{C}", r"t", r"=", 
            r"x", r"\vec{i}", r"+", r"y", r"\vec{j}", r"+", r"z", r"\vec{k}",
            font_size=52
        )
        
        # 精确着色
        main_equation[0].set_color("#ff6b9d")  # r(t) 粉色
        main_equation[2].set_color("#ffd700")  # C 金色
        main_equation[3].set_color("#00d4ff")  # t 青色
        main_equation[5].set_color("#ff4444")  # x 红色
        main_equation[6].set_color("#ff4444")  # i 红色
        main_equation[8].set_color("#44ff44")  # y 绿色
        main_equation[9].set_color("#44ff44")  # j 绿色
        main_equation[11].set_color("#4444ff") # z 蓝色
        main_equation[12].set_color("#4444ff") # k 蓝色
        
        main_equation.next_to(table_header, DOWN, buff=0.6)
        
        # 方程发光效果
        eq_glow = main_equation.copy().set_stroke(width=8, opacity=0.5)
        
        self.play(
            FadeIn(eq_glow),
            Write(main_equation),
            run_time=1.8
        )
        self.wait(0.5)
        
        # ========== 转换到3D视图 ==========
        self.play(
            main_equation.animate.scale(0.65).to_corner(UL, buff=0.5),
            FadeOut(eq_glow),
            FadeOut(grid),
            run_time=1
        )
        
        # 设置3D相机
        self.set_camera_orientation(phi=75*DEGREES, theta=-50*DEGREES, zoom=1)
        
        # ========== 创建中心原点 ==========
        origin_sphere = Sphere(
            radius=0.15,
            color="#ffffff",
            resolution=(20, 20)
        )
        origin_sphere.set_opacity(1)
        origin_sphere.set_sheen(1, direction=UP)
        
        origin_glow = Sphere(radius=0.3, color="#ffffff", resolution=(15, 15))
        origin_glow.set_opacity(0.3)
        
        self.add(origin_sphere, origin_glow)
        self.play(
            FadeIn(origin_sphere),
            FadeIn(origin_glow),
            run_time=1
        )
        
        # ========== 时空说明文字 ==========
        spacetime_label = Text(
            "时空三维发散",
            font="Noto Sans SC",
            weight=BOLD,
            font_size=32,
            color="#00d4ff"
        )
        self.add_fixed_in_frame_mobjects(spacetime_label)
        spacetime_label.to_edge(DOWN, buff=0.8)
        self.play(Write(spacetime_label), run_time=1)
        
        # ========== 生成多个方向的发散泡沫 ==========
        np.random.seed(42)
        
        # 定义多个发散方向（球面均匀分布）
        num_directions = 20
        directions = []
        for i in range(num_directions):
            phi = np.arccos(1 - 2 * (i + 0.5) / num_directions)
            theta = PI * (1 + 5**0.5) * i
            x = np.sin(phi) * np.cos(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(phi)
            directions.append(np.array([x, y, z]))
        
        # 泡沫颜色列表
        bubble_colors = [
            "#ff6b9d", "#ffd700", "#00d4ff", "#44ff44", 
            "#ff4444", "#4444ff", "#ff44ff", "#44ffff",
            "#ffaa44", "#aa44ff", "#ff4488", "#44ff88"
        ]
        
        # 存储所有泡沫
        all_bubbles = []
        
        # ========== 第一波：初始泡沫爆发 ==========
        initial_bubbles = VGroup()
        
        for i, direction in enumerate(directions):
            color = bubble_colors[i % len(bubble_colors)]
            
            # 创建泡沫球
            bubble = Sphere(
                radius=0.08,
                color=color,
                resolution=(15, 15)
            )
            bubble.set_opacity(0.6)
            bubble.set_sheen(0.8, direction=UP)
            
            # 泡沫光环
            bubble_glow = Sphere(
                radius=0.15,
                color=color,
                resolution=(10, 10)
            )
            bubble_glow.set_opacity(0.2)
            
            bubble_group = VGroup(bubble, bubble_glow)
            initial_bubbles.add(bubble_group)
            all_bubbles.append({
                'group': bubble_group,
                'direction': direction,
                'color': color,
                'birth_time': 0
            })
        
        # 初始泡沫从中心爆发
        self.play(
            *[FadeIn(b, scale=0.1) for b in initial_bubbles],
            run_time=1
        )
        
        # ========== 持续发散动画 ==========
        t_tracker = ValueTracker(0)
        spawn_interval = 0.3  # 新泡沫生成间隔
        last_spawn = 0
        max_radius = 6
        
        def update_bubbles(mob, dt):
            t = t_tracker.get_value()
            
            # 更新所有现有泡沫
            for bubble_data in all_bubbles:
                age = t - bubble_data['birth_time']
                if age > 0:
                    # 计算当前半径
                    radius = age * 1.2  # 扩散速度
                    
                    if radius < max_radius:
                        # 更新位置
                        pos = bubble_data['direction'] * radius
                        bubble_data['group'].move_to(pos)
                        
                        # 动态调整透明度和大小
                        opacity = max(0.1, 0.8 - age * 0.15)
                        scale = 1 + age * 0.3
                        
                        bubble_data['group'][0].set_opacity(opacity * 0.6)
                        bubble_data['group'][1].set_opacity(opacity * 0.2)
                        bubble_data['group'].scale(1 + dt * 0.2)
                    else:
                        # 泡沫消失
                        bubble_data['group'].set_opacity(0)
        
        # 添加更新器
        dummy = Dot(ORIGIN)
        dummy.set_opacity(0)
        dummy.add_updater(update_bubbles)
        self.add(dummy)
        
        # 动态生成新泡沫
        for wave in range(8):  # 8波泡沫
            self.wait(0.4)
            
            # 生成新的一波泡沫
            new_wave = VGroup()
            for i in range(15):  # 每波15个泡沫
                # 随机方向
                phi = np.random.uniform(0, PI)
                theta = np.random.uniform(0, 2*PI)
                x = np.sin(phi) * np.cos(theta)
                y = np.sin(phi) * np.sin(theta)
                z = np.cos(phi)
                direction = np.array([x, y, z])
                
                color = bubble_colors[np.random.randint(0, len(bubble_colors))]
                
                # 创建新泡沫
                bubble = Sphere(
                    radius=0.08,
                    color=color,
                    resolution=(12, 12)
                )
                bubble.set_opacity(0.6)
                bubble.set_sheen(0.8, direction=UP)
                
                bubble_glow = Sphere(
                    radius=0.15,
                    color=color,
                    resolution=(8, 8)
                )
                bubble_glow.set_opacity(0.2)
                
                bubble_group = VGroup(bubble, bubble_glow)
                new_wave.add(bubble_group)
                
                all_bubbles.append({
                    'group': bubble_group,
                    'direction': direction,
                    'color': color,
                    'birth_time': t_tracker.get_value()
                })
            
            # 新泡沫爆发
            self.play(
                *[FadeIn(b, scale=0.1) for b in new_wave],
                t_tracker.animate.increment_value(0.4),
                run_time=0.4,
                rate_func=linear
            )
        
        # 继续扩散
        self.play(
            t_tracker.animate.increment_value(3),
            run_time=3,
            rate_func=linear
        )
        
        # 开始相机旋转观察
        self.begin_ambient_camera_rotation(rate=0.2)
        self.play(
            t_tracker.animate.increment_value(2),
            run_time=2,
            rate_func=linear
        )
        self.stop_ambient_camera_rotation()
        
        # ========== 显示参数方程 ==========
        param_eqs = VGroup(
            MathTex(r"x(t) = C_x \cdot t", color=RED, font_size=32),
            MathTex(r"y(t) = C_y \cdot t", color=GREEN, font_size=32),
            MathTex(r"z(t) = C_z \cdot t", color=BLUE, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        
        param_box = SurroundingRectangle(
            param_eqs,
            color="#00d4ff",
            buff=0.25,
            corner_radius=0.1,
            fill_color="#0a0a0a",
            fill_opacity=0.95,
            stroke_width=2
        )
        
        param_group = VGroup(param_box, param_eqs)
        self.add_fixed_in_frame_mobjects(param_group)
        param_group.to_corner(DR, buff=0.5)
        
        self.play(
            FadeIn(param_box),
            Write(param_eqs),
            run_time=1.5
        )
        
        # 继续扩散
        self.play(
            t_tracker.animate.increment_value(2),
            run_time=2,
            rate_func=linear
        )
        
        # ========== 核心结论 ==========
        conclusion = Text(
            "各向同性：时空均匀扩张",
            font="Noto Sans SC",
            weight=BOLD,
            font_size=36,
            color="#00ff41"
        )
        conclusion_box = SurroundingRectangle(
            conclusion,
            color="#00ff41",
            buff=0.25,
            corner_radius=0.15,
            stroke_width=4,
            fill_color="#0a0a0a",
            fill_opacity=0.95
        )
        conclusion_glow = conclusion_box.copy().set_stroke(width=20, opacity=0.3)
        conclusion_group = VGroup(conclusion_glow, conclusion_box, conclusion)
        
        self.add_fixed_in_frame_mobjects(conclusion_group)
        conclusion_group.next_to(spacetime_label, UP, buff=0.5)
        
        self.play(
            FadeOut(spacetime_label),
            FadeIn(conclusion_glow),
            Create(conclusion_box),
            Write(conclusion),
            run_time=2
        )
        
        # 最终扩散
        self.play(
            t_tracker.animate.increment_value(1.5),
            run_time=1.5,
            rate_func=linear
        )
        
        self.wait(1)
        
        # ========== 终场 ==========
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
        self.wait(0.5)

# LaTeX 公式渲染配置
plt.rcParams["text.usetex"] = False  # 使用 Matplotlib 的内置渲染
plt.rcParams["mathtext.fontset"] = "cm"  # 使用 CMU Serif 字体渲染数学公式