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

class SpaceTimeUnification(Scene):
    def construct(self):
        # 标题
        title = Text("时空同一化方程", font="Noto Sans SC", font_size=48)
        title.to_edge(UP)
        
        # 主方程
        main_eq = MathTex(
            r"\vec{r}(t) = \vec{C}t = x\vec{i} + y\vec{j} + z\vec{k}",
            font_size=42
        )
        main_eq.next_to(title, DOWN, buff=0.8)
        
        # 分解展示
        decomp_title = Text("分量展示：", font="Noto Sans SC", font_size=32)
        decomp_title.next_to(main_eq, DOWN, buff=1)
        
        x_comp = MathTex(r"x(t) = C_x t", color=RED, font_size=36)
        y_comp = MathTex(r"y(t) = C_y t", color=GREEN, font_size=36)
        z_comp = MathTex(r"z(t) = C_z t", color=BLUE, font_size=36)
        
        components = VGroup(x_comp, y_comp, z_comp).arrange(DOWN, buff=0.4)
        components.next_to(decomp_title, DOWN, buff=0.5)
        
        # 3D 坐标系和轨迹
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            z_length=5
        )
        axes.scale(0.6)
        axes.to_edge(RIGHT, buff=0.5)
        
        # 轨迹参数
        C = np.array([1, 0.8, 0.6])
        
        # 创建轨迹
        def trajectory(t):
            return axes.c2p(C[0]*t, C[1]*t, C[2]*t)
        
        path = ParametricFunction(
            trajectory,
            t_range=[0, 2],
            color=YELLOW,
            stroke_width=4
        )
        
        # 运动点
        dot = Dot3D(point=trajectory(0), color=YELLOW, radius=0.12)
        
        # 速度矢量
        velocity_arrow = Arrow3D(
            start=ORIGIN,
            end=axes.c2p(C[0], C[1], C[2]),
            color=ORANGE,
            thickness=0.02
        )
        velocity_label = MathTex(r"\vec{C}", color=ORANGE, font_size=32)
        velocity_label.next_to(axes, UP)
        
        # 动画序列
        self.play(Write(title))
        self.wait(0.5)
        
        self.play(Write(main_eq))
        self.wait(1)
        
        self.play(
            FadeIn(decomp_title),
            Write(x_comp),
            run_time=1
        )
        self.wait(0.3)
        
        self.play(Write(y_comp))
        self.wait(0.3)
        
        self.play(Write(z_comp))
        self.wait(1)
        
        # 转换到3D视图
        self.play(
            FadeOut(decomp_title),
            FadeOut(components),
            main_eq.animate.scale(0.7).to_edge(LEFT).shift(UP*2),
        )
        
        self.play(Create(axes))
        self.play(
            FadeIn(velocity_arrow),
            Write(velocity_label)
        )
        self.wait(0.5)
        
        # 绘制轨迹
        self.add(dot)
        self.play(
            MoveAlongPath(dot, path),
            Create(path),
            run_time=3,
            rate_func=linear
        )
        self.wait(1)
        
        # 高亮显示线性关系
        highlight_box = SurroundingRectangle(
            main_eq,
            color=YELLOW,
            buff=0.15,
            corner_radius=0.1
        )
        
        note = Text(
            "线性时空关系：位置正比于时间",
            font="Noto Sans SC",
            font_size=28,
            color=YELLOW
        )
        note.next_to(main_eq, DOWN, buff=0.5)
        
        self.play(Create(highlight_box))
        self.play(FadeIn(note))
        self.wait(2)
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait(0.5)

main = SpaceTimeUnification()
main.render()


# LaTeX 公式渲染配置
plt.rcParams["text.usetex"] = False  # 使用 Matplotlib 的内置渲染
plt.rcParams["mathtext.fontset"] = "cm"  # 使用 CMU Serif 字体渲染数学公式