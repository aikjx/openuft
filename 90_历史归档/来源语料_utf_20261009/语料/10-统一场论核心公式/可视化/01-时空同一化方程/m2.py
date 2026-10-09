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
        self.wait(0.5)
        
        # ========== 主方程 100% 精确还原 ==========
        main_equation = MathTex(
            r"\vec{r}(t)", r"=", r"\vec{C}", r"t", r"=", 
            r"x", r"\vec{i}", r"+", r"y", r"\vec{j}", r"+", r"z", r"\vec{k}",
            font_size=56
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
        
        main_equation.next_to(table_header, DOWN, buff=0.8)
        
        # 方程发光效果
        eq_glow = main_equation.copy().set_stroke(width=8, opacity=0.5)
        
        self.play(
            FadeIn(eq_glow),
            Write(main_equation),
            run_time=2
        )
        self.wait(1)
        
        # ========== 矢量分解动画 ==========
        arrow_r = Arrow(ORIGIN, [2, 1.5, 0], buff=0, color="#ff6b9d", stroke_width=8)
        arrow_c = Arrow(ORIGIN, [1.5, 1.2, 0], buff=0, color="#ffd700", stroke_width=8)
        label_r = MathTex(r"\vec{r}(t)", color="#ff6b9d", font_size=40).next_to(arrow_r, UP)
        label_c = MathTex(r"\vec{C}", color="#ffd700", font_size=40).next_to(arrow_c, DOWN)
        
        vectors = VGroup(arrow_r, arrow_c, label_r, label_c).scale(0.8)
        vectors.to_edge(LEFT, buff=1.5).shift(DOWN*0.5)
        
        self.play(
            Create(arrow_r),
            Write(label_r),
            run_time=1
        )
        self.play(
            Create(arrow_c),
            Write(label_c),
            run_time=1
        )
        
        # ========== 3D 时空轨迹 ==========
        self.play(
            FadeOut(vectors),
            main_equation.animate.scale(0.75).to_corner(UL, buff=0.8),
            FadeOut(eq_glow),
            run_time=1
        )
        
        # 设置3D相机
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES, zoom=0.8)
        
        # 3D坐标系
        axes_3d = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "include_tip": True,
                "tip_length": 0.2,
            }
        )
        
        # 坐标轴标签
        x_label = MathTex(r"x", color=RED, font_size=36).next_to(axes_3d.x_axis, RIGHT)
        y_label = MathTex(r"y", color=GREEN, font_size=36).next_to(axes_3d.y_axis, UP)
        z_label = MathTex(r"z", color=BLUE, font_size=36).next_to(axes_3d.z_axis, OUT)
        x_label.rotate(90*DEGREES, axis=RIGHT)
        y_label.rotate(90*DEGREES, axis=RIGHT)
        
        self.play(Create(axes_3d), run_time=2)
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        self.play(Write(x_label), Write(y_label), Write(z_label))
        
        # ========== 轨迹参数（精确的线性关系）==========
        C_vec = np.array([1.2, 0.9, 1.5])  # 速度矢量
        t_max = 1.5
        
        def space_curve(t):
            return axes_3d.c2p(C_vec[0]*t, C_vec[1]*t, C_vec[2]*t)
        
        # 主轨迹线（发光效果）
        trajectory = ParametricFunction(
            space_curve,
            t_range=[0, t_max],
            color="#00ffff",
            stroke_width=6
        )
        trajectory_glow = ParametricFunction(
            space_curve,
            t_range=[0, t_max],
            color="#00ffff",
            stroke_width=20,
            stroke_opacity=0.3
        )
        
        # 运动粒子
        particle = Sphere(
            radius=0.12,
            color="#ff6b9d",
            resolution=(20, 20)
        ).move_to(space_curve(0))
        particle.set_sheen(0.8, direction=UP)
        
        # 粒子光环
        glow_sphere = Sphere(radius=0.25, color="#ff6b9d", resolution=(15, 15))
        glow_sphere.set_opacity(0.2)
        glow_sphere.move_to(particle.get_center())
        
        # 速度矢量箭头
        velocity_arrow = Arrow3D(
            start=space_curve(0),
            end=axes_3d.c2p(C_vec[0]*0.5, C_vec[1]*0.5, C_vec[2]*0.5),
            color="#ffd700",
            thickness=0.03,
            height=0.3,
            base_radius=0.03
        )
        v_label = MathTex(r"\vec{C}", color="#ffd700", font_size=40)
        v_label.rotate(90*DEGREES, axis=RIGHT)
        v_label.next_to(velocity_arrow, OUT)
        
        self.play(
            Create(trajectory_glow),
            Create(trajectory),
            run_time=2
        )
        
        self.add_fixed_in_frame_mobjects(v_label)
        self.play(
            FadeIn(particle),
            FadeIn(glow_sphere),
            FadeIn(velocity_arrow),
            Write(v_label),
            run_time=1.5
        )
        
        # ========== 粒子运动动画 ==========
        t_tracker = ValueTracker(0)
        
        def update_particle(mob):
            t = t_tracker.get_value()
            mob.move_to(space_curve(t))
        
        def update_glow(mob):
            mob.move_to(particle.get_center())
        
        def update_arrow(mob):
            t = t_tracker.get_value()
            pos = space_curve(t)
            mob.become(
                Arrow3D(
                    start=pos,
                    end=pos + axes_3d.c2p(C_vec[0]*0.5, C_vec[1]*0.5, C_vec[2]*0.5) - axes_3d.c2p(0,0,0),
                    color="#ffd700",
                    thickness=0.03,
                    height=0.3,
                    base_radius=0.03
                )
            )
        
        particle.add_updater(update_particle)
        glow_sphere.add_updater(update_glow)
        velocity_arrow.add_updater(update_arrow)
        
        # 运动轨迹
        self.play(
            t_tracker.animate.set_value(t_max),
            run_time=4,
            rate_func=linear
        )
        
        particle.clear_updaters()
        glow_sphere.clear_updaters()
        velocity_arrow.clear_updaters()
        
        # ========== 投影演示 ==========
        # XY平面投影
        proj_xy = DashedLine(
            start=space_curve(t_max),
            end=axes_3d.c2p(C_vec[0]*t_max, C_vec[1]*t_max, 0),
            color=YELLOW,
            dash_length=0.1,
            stroke_width=2
        )
        proj_dot_xy = Dot3D(
            point=axes_3d.c2p(C_vec[0]*t_max, C_vec[1]*t_max, 0),
            color=YELLOW,
            radius=0.08
        )
        
        self.play(
            Create(proj_xy),
            FadeIn(proj_dot_xy),
            run_time=1
        )
        
        # 相机旋转
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # ========== 参数方程展示 ==========
        self.move_camera(phi=70*DEGREES, theta=-45*DEGREES, run_time=1.5)
        
        param_eqs = VGroup(
            MathTex(r"x(t) = C_x \cdot t", color=RED, font_size=36),
            MathTex(r"y(t) = C_y \cdot t", color=GREEN, font_size=36),
            MathTex(r"z(t) = C_z \cdot t", color=BLUE, font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        param_box = SurroundingRectangle(
            param_eqs,
            color="#00d4ff",
            buff=0.3,
            corner_radius=0.1,
            fill_color="#0a0a0a",
            fill_opacity=0.9,
            stroke_width=2
        )
        
        param_group = VGroup(param_box, param_eqs)
        self.add_fixed_in_frame_mobjects(param_group)
        param_group.to_corner(DR, buff=0.5)
        
        self.play(
            FadeIn(param_box),
            Write(param_eqs),
            run_time=2
        )
        self.wait(2)
        
        # ========== 高亮核心结论 ==========
        conclusion = Text(
            "线性时空统一：位置 ∝ 时间",
            font="Noto Sans SC",
            weight=BOLD,
            font_size=38,
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
        conclusion_group.move_to(DOWN*2.5)
        
        self.play(
            FadeIn(conclusion_glow),
            Create(conclusion_box),
            Write(conclusion),
            run_time=2
        )
        self.wait(3)
        
        # ========== 终场 ==========
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
        self.wait(1)

# LaTeX 公式渲染配置
plt.rcParams["text.usetex"] = False  # 使用 Matplotlib 的内置渲染
plt.rcParams["mathtext.fontset"] = "cm"  # 使用 CMU Serif 字体渲染数学公式