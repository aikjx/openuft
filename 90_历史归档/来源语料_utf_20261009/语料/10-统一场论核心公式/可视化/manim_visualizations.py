from manim import *
import numpy as np

class SpacetimeUnification(ThreeDScene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("统一场论核心公式 - 时空同一化方程", font_size=40, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 方程
        equation = MathTex(
            r"\vec{r}(t) = \vec{C}t = x\vec{i} + y\vec{j} + z\vec{k}",
            font_size=48,
            color=YELLOW
        )
        equation.to_corner(UP, buff=1.5)
        self.play(Write(equation))
        self.wait(2)
        
        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "tip_length": 0.2,
                "tip_width": 0.1
            }
        )
        
        # 添加坐标轴标签
        x_label = axes.get_x_axis_label("x", color=RED)
        y_label = axes.get_y_axis_label("y", color=GREEN)
        z_label = axes.get_z_axis_label("z", color=BLUE)
        
        # 设置相机角度
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))
        self.wait(2)
        
        # 创建轨迹点
        trajectory_points = VGroup()
        t_values = np.linspace(0, 2, 30)
        C = np.array([1, 0.8, 0.6])  # 速度矢量
        
        for t in t_values:
            point = Dot3D(
                point=axes.c2p(*C * t),
                color=BLUE,
                radius=0.07
            )
            trajectory_points.add(point)
        
        # 显示轨迹
        trajectory = VMobject()
        trajectory.set_points_as_corners([dot.get_center() for dot in trajectory_points])
        trajectory.set_stroke(BLUE, width=6)
        
        self.play(Create(trajectory_points, lag_ratio=0.1), run_time=2)
        self.wait()
        self.play(Create(trajectory), run_time=2)
        self.wait(2)
        
        # 添加移动的点
        moving_dot = Dot3D(
            point=axes.c2p(0, 0, 0),
            color=RED,
            radius=0.15
        )
        
        self.play(Create(moving_dot))
        self.wait()
        
        # 动画移动点
        def update_dot(dot, alpha):
            t = alpha * 2
            new_position = axes.c2p(*C * t)
            dot.move_to(new_position)
            return dot
        
        self.play(
            UpdateFromAlphaFunc(moving_dot, update_dot),
            run_time=5,
            rate_func=linear
        )
        self.wait(2)
        
        # 添加速度矢量
        vector = Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(*C * 2),
            color=YELLOW,
            thickness=0.02,
            base_radius=0.05,
            tip_length=0.3,
            tip_radius=0.1
        )
        vector_label = MathTex(r"\vec{C}", color=YELLOW, font_size=36)
        vector_label.next_to(vector.get_end(), UP, buff=0.2)
        
        self.play(Create(vector), run_time=2)
        self.play(Write(vector_label))
        self.wait(3)
        
        # 旋转视角展示
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(6)
        self.stop_ambient_camera_rotation()
        self.wait(2)
        
        # 总结
        summary = Text(
            "时空同一化方程表明空间和时间是统一的，\n时间是空间运动的描述。",
            font_size=28,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        summary.to_edge(DOWN, buff=0.5)
        
        self.play(Write(summary))
        self.wait(3)

class SpiralMotionVisualization(ThreeDScene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("三维螺旋时空方程", font_size=40, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 方程
        equation = MathTex(
            r"\vec{r}(\theta) = a\theta\cos(\theta)\vec{i} + a\theta\sin(\theta)\vec{j} + b\theta\vec{k}",
            font_size=36,
            color=YELLOW
        )
        equation.to_corner(UP, buff=1.5)
        self.play(Write(equation))
        self.wait(2)
        
        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[0, 10, 2],
            x_length=8,
            y_length=8,
            z_length=8,
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "tip_length": 0.2,
                "tip_width": 0.1
            }
        )
        
        # 添加坐标轴标签
        x_label = axes.get_x_axis_label("x", color=RED)
        y_label = axes.get_y_axis_label("y", color=GREEN)
        z_label = axes.get_z_axis_label("z", color=BLUE)
        
        # 设置相机角度
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))
        self.wait(2)
        
        # 创建螺旋线
        a = 0.5
        b = 0.3
        
        spiral = ParametricFunction(
            lambda t: axes.c2p(
                a * t * np.cos(t),
                a * t * np.sin(t),
                b * t
            ),
            t_range=[0, 8*PI],
            color=BLUE
        )
        
        spiral.set_stroke(width=6)
        self.play(Create(spiral), run_time=4)
        self.wait(2)
        
        # 添加移动点
        moving_dot = Dot3D(color=RED, radius=0.15)
        
        def update_moving_dot(dot, alpha):
            t = alpha * 8 * PI
            x = a * t * np.cos(t)
            y = a * t * np.sin(t)
            z = b * t
            dot.move_to(axes.c2p(x, y, z))
            return dot
        
        self.play(Create(moving_dot))
        self.wait()
        
        self.play(
            UpdateFromAlphaFunc(moving_dot, update_moving_dot),
            run_time=6,
            rate_func=linear
        )
        self.wait(2)
        
        # 旋转视角展示
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(2)
        
        # 添加说明文字
        explanation = Text(
            "三维螺旋时空方程描述了空间的螺旋结构，\n揭示了时空的几何本质。",
            font_size=28,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.wait(3)

class UnifiedForceEquation(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("宇宙大统一方程", font_size=40, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 方程
        equation = MathTex(
            r"\vec{F} = \frac{d\vec{P}}{dt} = \vec{C}\frac{dm}{dt} - \vec{V}\frac{dm}{dt} + m\frac{d\vec{C}}{dt} - m\frac{d\vec{V}}{dt}",
            font_size=30,
            color=YELLOW
        )
        equation.to_corner(UP, buff=1.5)
        self.play(Write(equation))
        self.wait(2)
        
        # 分解方程
        terms = VGroup(
            MathTex(r"\vec{F}_1 = \vec{C}\frac{dm}{dt}", color=RED, font_size=36),
            MathTex(r"\vec{F}_2 = -\vec{V}\frac{dm}{dt}", color=GREEN, font_size=36),
            MathTex(r"\vec{F}_3 = m\frac{d\vec{C}}{dt}", color=BLUE, font_size=36),
            MathTex(r"\vec{F}_4 = -m\frac{d\vec{V}}{dt}", color=ORANGE, font_size=36)
        )
        
        terms.arrange(DOWN, buff=0.8)
        terms.to_edge(LEFT, buff=1)
        
        for i, term in enumerate(terms):
            self.play(Write(term), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        
        # 总力
        total_force = MathTex(
            r"\vec{F} = \vec{F}_1 + \vec{F}_2 + \vec{F}_3 + \vec{F}_4",
            font_size=36,
            color=WHITE
        )
        total_force.to_edge(RIGHT, buff=1)
        self.play(Write(total_force))
        self.wait(2)
        
        # 力的可视化
        # 创建力矢量
        force_vectors = VGroup()
        colors = [RED, GREEN, BLUE, ORANGE]
        labels = [r"\vec{F}_1", r"\vec{F}_2", r"\vec{F}_3", r"\vec{F}_4"]
        directions = [UP, DOWN, LEFT, RIGHT]
        
        origin = ORIGIN
        
        for i in range(4):
            vector = Arrow(
                start=origin,
                end=origin + 2.5 * directions[i],
                color=colors[i],
                buff=0,
                max_tip_length_to_length_ratio=0.15
            )
            label = MathTex(labels[i], color=colors[i], font_size=28)
            label.next_to(vector.get_end(), directions[i], buff=0.15)
            force_vectors.add(VGroup(vector, label))
        
        self.play(LaggedStart(*[Create(v[0]) for v in force_vectors], lag_ratio=0.3), run_time=2)
        self.play(LaggedStart(*[Write(v[1]) for v in force_vectors], lag_ratio=0.3), run_time=2)
        self.wait(2)
        
        # 合成总力
        resultant = Arrow(
            start=origin,
            end=origin + 0.5*UP + 0.3*DOWN + 0.2*LEFT + 0.4*RIGHT,  # 不完全抵消
            color=WHITE,
            buff=0,
            max_tip_length_to_length_ratio=0.2
        )
        resultant_label = MathTex(r"\vec{F}", color=WHITE, font_size=36)
        resultant_label.next_to(resultant.get_end(), UP, buff=0.2)
        
        self.play(Create(resultant), Write(resultant_label))
        self.wait(3)
        
        # 物理意义说明
        explanation = Text(
            "宇宙大统一方程将所有力统一描述为动量变化率，\n揭示了自然界四种基本力的内在统一性。",
            font_size=28,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.wait(3)

class WaveEquationVisualization(ThreeDScene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("三维空间波动方程", font_size=40, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 方程
        equation = MathTex(
            r"\nabla^2 L = \frac{1}{c^2} \frac{\partial^2 L}{\partial t^2}",
            font_size=48,
            color=YELLOW
        )
        equation.to_corner(UP, buff=1.5)
        self.play(Write(equation))
        self.wait(2)
        
        # 设置相机角度
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 创建波动表面
        def wave_function(x, y, t):
            return np.sin(np.sqrt(x**2 + y**2) - 0.5*t)
        
        # 创建波动表面
        surface = Surface(
            lambda u, v: np.array([
                u,
                v,
                wave_function(u, v, 0)
            ]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30)
        )
        
        # 设置表面颜色
        surface.set_fill_by_value(
            axes=ThreeDAxes(),
            colors=[(RED, -0.5), (YELLOW, 0), (BLUE, 0.5)],
            axis=2
        )
        surface.set_stroke(color=WHITE, width=0.5, opacity=0.5)
        
        self.play(Create(surface), run_time=3)
        self.wait(2)
        
        # 动画波动
        def update_surface(surf, alpha):
            t = alpha * 4 * PI
            new_points = []
            for u in np.linspace(-3, 3, 30):
                row = []
                for v in np.linspace(-3, 3, 30):
                    x, y = u, v
                    z = wave_function(x, y, t)
                    row.append([x, y, z])
                new_points.append(row)
            surf.set_points(np.array(new_points))
            return surf
        
        self.play(
            UpdateFromAlphaFunc(surface, update_surface),
            run_time=8,
            rate_func=linear
        )
        self.wait(2)
        
        # 添加波动传播说明
        explanation = Text(
            "波动方程描述了空间本身的波动性质，\n这为理解引力波和电磁波提供了统一框架。",
            font_size=28,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.wait(3)

# 统一场论公式集合
class UnifiedFieldTheoryOverview(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("统一场论核心公式一览", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 公式列表
        formulas = VGroup(
            MathTex(r"\text{1. 时空同一化方程: } \vec{r}(t) = \vec{C}t", font_size=36, color=RED),
            MathTex(r"\text{2. 螺旋时空方程: } \vec{r}(\theta) = a\theta\cos(\theta)\vec{i} + a\theta\sin(\theta)\vec{j} + b\theta\vec{k}", font_size=36, color=GREEN),
            MathTex(r"\text{3. 质量定义方程: } m = \frac{E}{c^2}", font_size=36, color=BLUE),
            MathTex(r"\text{4. 动量方程: } \vec{P} = m(\vec{C} - \vec{V})", font_size=36, color=YELLOW),
            MathTex(r"\text{5. 大统一方程: } \vec{F} = \frac{d\vec{P}}{dt}", font_size=36, color=ORANGE),
            MathTex(r"\text{6. 波动方程: } \nabla^2 L = \frac{1}{c^2} \frac{\partial^2 L}{\partial t^2}", font_size=36, color=PURPLE)
        )
        
        formulas.arrange(DOWN, buff=0.6)
        formulas.scale(0.8)
        
        # 逐个显示公式
        for formula in formulas:
            self.play(Write(formula), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        
        # 高亮大统一方程
        unified_formula = formulas[4]
        self.play(
            unified_formula.animate.set_color(WHITE).scale(1.3),
            run_time=2
        )
        self.wait()
        
        # 添加说明
        conclusion = Text(
            "这些公式共同构成了统一场论的数学基础，\n揭示了宇宙万物的本质统一性。",
            font_size=32,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        conclusion.to_edge(DOWN, buff=0.5)
        
        self.play(Write(conclusion))
        self.wait(3)
        
        # 结束动画
        self.play(
            FadeOut(formulas),
            FadeOut(conclusion),
            run_time=2
        )
        
        final_text = Text(
            "统一场论 - 探索宇宙的终极理论",
            font_size=48,
            color=GOLD
        )
        self.play(Write(final_text))
        self.wait(3)

class MassDefinitionEquation(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("质量定义方程", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 方程
        equation = MathTex(
            r"m = \frac{E}{c^2}",
            font_size=70,
            color=YELLOW
        )
        self.play(Write(equation))
        self.wait(2)
        
        # 变换形式
        equation2 = MathTex(
            r"E = mc^2",
            font_size=70,
            color=RED
        )
        self.play(Transform(equation, equation2))
        self.wait(2)
        
        # 图形解释
        # 创建能量和质量的图形表示
        energy = Circle(radius=1.8, color=RED, fill_opacity=0.7)
        energy_label = Text("能量 E", font_size=30, color=RED)
        energy_label.next_to(energy, UP)
        
        mass = Square(side_length=1.8, color=BLUE, fill_opacity=0.7)
        mass_label = Text("质量 m", font_size=30, color=BLUE)
        mass_label.next_to(mass, UP)
        
        # 光速标签
        c_squared = MathTex(r"c^2", font_size=42, color=GREEN)
        
        # 排列元素
        energy_group = VGroup(energy, energy_label).shift(LEFT*4)
        mass_group = VGroup(mass, mass_label).shift(RIGHT*4)
        c_squared.next_to(
            (energy_group.get_right() + mass_group.get_left()) / 2, 
            UP, buff=0.7
        )
        
        self.play(
            FadeOut(equation),
            Create(energy_group),
            Create(mass_group),
            Write(c_squared),
            run_time=2
        )
        self.wait(2)
        
        # 添加箭头表示关系
        arrow1 = Arrow(start=mass_group.get_top(), end=energy_group.get_top(), color=WHITE, buff=0.2)
        arrow2 = Arrow(start=energy_group.get_bottom(), end=mass_group.get_bottom(), color=WHITE, buff=0.2)
        
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), run_time=2)
        self.wait(2)
        
        # 解释文本
        explanation = Text(
            "质量与能量的等价关系：\n质量可以转化为能量，能量也可以转化为质量",
            font_size=32,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        explanation.to_edge(DOWN, buff=1)
        
        self.play(Write(explanation))
        self.wait(3)

class MomentumEquation(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("动量方程", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 静止动量方程
        rest_momentum = MathTex(
            r"\vec{P_0} = m\vec{C}",
            font_size=55,
            color=RED
        )
        rest_label = Text("静止动量", font_size=30, color=RED)
        rest_group = VGroup(rest_momentum, rest_label).arrange(DOWN, buff=0.4)
        rest_group.to_edge(LEFT, buff=1)
        
        # 运动动量方程
        motion_momentum = MathTex(
            r"\vec{P} = m(\vec{C} - \vec{V})",
            font_size=55,
            color=BLUE
        )
        motion_label = Text("运动动量", font_size=30, color=BLUE)
        motion_group = VGroup(motion_momentum, motion_label).arrange(DOWN, buff=0.4)
        motion_group.to_edge(RIGHT, buff=1)
        
        self.play(Write(rest_group), Write(motion_group), run_time=2)
        self.wait(2)
        
        # 解释各符号
        symbol_explanations = VGroup(
            MathTex(r"m", r"&: \text{物体的质量}", font_size=32, color=WHITE),
            MathTex(r"\vec{C}", r"&: \text{空间运动速度矢量}", font_size=32, color=YELLOW),
            MathTex(r"\vec{V}", r"&: \text{物体相对于观察者的运动速度}", font_size=32, color=GREEN),
            MathTex(r"\vec{P_0}", r"&: \text{物体静止时的动量}", font_size=32, color=RED),
            MathTex(r"\vec{P}", r"&: \text{物体运动时的动量}", font_size=32, color=BLUE)
        )
        
        for i, explanation in enumerate(symbol_explanations):
            explanation.to_edge(LEFT, buff=1).shift(UP * (2 - i * 1.3))
        
        self.play(LaggedStart(*[Write(expl) for expl in symbol_explanations], lag_ratio=0.3), run_time=3)
        self.wait(3)
        
        # 动画演示
        # 创建坐标系
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 3, 1],
            axis_config={"include_tip": True, "color": WHITE}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # 创建物体点
        object_dot = Dot(axes.c2p(1, 1), color=RED, radius=0.15)
        object_label = Text("物体", font_size=24, color=RED)
        object_label.next_to(object_dot, UP, buff=0.1)
        
        # 空间运动矢量C
        vector_C = Arrow(
            start=axes.c2p(1, 1),
            end=axes.c2p(4, 2),
            color=YELLOW,
            buff=0,
            max_tip_length_to_length_ratio=0.1
        )
        label_C = MathTex(r"\vec{C}", color=YELLOW, font_size=30)
        label_C.next_to(vector_C.get_end(), RIGHT, buff=0.2)
        
        # 物体运动矢量V
        vector_V = Arrow(
            start=axes.c2p(1, 1),
            end=axes.c2p(2, 2.5),
            color=GREEN,
            buff=0,
            max_tip_length_to_length_ratio=0.1
        )
        label_V = MathTex(r"\vec{V}", color=GREEN, font_size=30)
        label_V.next_to(vector_V.get_end(), UP, buff=0.2)
        
        # 动量矢量P
        vector_P = Arrow(
            start=axes.c2p(1, 1),
            end=axes.c2p(3, 0.5),  # C - V
            color=BLUE,
            buff=0,
            max_tip_length_to_length_ratio=0.1
        )
        label_P = MathTex(r"\vec{P} = m(\vec{C} - \vec{V})", color=BLUE, font_size=30)
        label_P.next_to(vector_P.get_end(), DOWN, buff=0.2)
        
        self.play(
            FadeOut(symbol_explanations),
            FadeOut(rest_group),
            FadeOut(motion_group),
            Create(axes),
            Create(axes_labels),
            Create(object_dot),
            Write(object_label),
            run_time=2
        )
        self.wait()
        
        self.play(Create(vector_C), Write(label_C), run_time=1.5)
        self.wait()
        self.play(Create(vector_V), Write(label_V), run_time=1.5)
        self.wait()
        self.play(Create(vector_P), Write(label_P), run_time=1.5)
        self.wait(3)
        
        # 解释文本
        explanation = Text(
            "动量方程揭示了统一场论中动量的新定义：\n物体的动量取决于空间运动和物体运动的相对关系",
            font_size=30,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.wait(3)

class ElectromagneticFieldEquations(ThreeDScene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("电磁场方程", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 电场定义方程
        electric_field = MathTex(
            r"\vec{E} = \frac{\vec{F_e}}{q}",
            font_size=55,
            color=RED
        )
        e_label = Text("电场强度定义", font_size=30, color=RED)
        e_group = VGroup(electric_field, e_label).arrange(DOWN)
        e_group.to_edge(LEFT, buff=1)
        
        # 磁场定义方程
        magnetic_field = MathTex(
            r"\vec{B} = \frac{\vec{F_m}}{qv}",
            font_size=55,
            color=BLUE
        )
        b_label = Text("磁场强度定义", font_size=30, color=BLUE)
        b_group = VGroup(magnetic_field, b_label).arrange(DOWN)
        b_group.to_edge(RIGHT, buff=1)
        
        self.play(Write(e_group), Write(b_group), run_time=2)
        self.wait(2)
        
        # 电磁场能量方程
        energy_equation = MathTex(
            r"u = \frac{1}{2}(\epsilon_0 E^2 + \frac{B^2}{\mu_0})",
            font_size=55,
            color=YELLOW
        )
        energy_label = Text("电磁场能量密度", font_size=30, color=YELLOW)
        energy_group = VGroup(energy_equation, energy_label).arrange(DOWN)
        energy_group.to_edge(DOWN, buff=2)
        
        self.play(Write(energy_group))
        self.wait(2)
        
        # 3D可视化电磁场
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "tip_length": 0.2,
                "tip_width": 0.1
            }
        )
        
        # 电场线（从正电荷发出）
        e_field_lines = VGroup()
        for i in range(12):
            angle = i * 2*PI / 12
            line = Arrow3D(
                start=ORIGIN,
                end=2.5 * np.array([np.cos(angle), np.sin(angle), 0]),
                color=RED,
                thickness=0.015,
                base_radius=0.05,
                tip_length=0.2
            )
            e_field_lines.add(line)
        
        # 磁场线（环绕电流）
        b_field_lines = VGroup()
        for i in range(12):
            angle = i * 2*PI / 12
            start_point = 1.8 * np.array([np.cos(angle), np.sin(angle), 0])
            mid_point = 1.8 * np.array([np.cos(angle + PI/6), np.sin(angle + PI/6), 0.5])
            end_point = 1.8 * np.array([np.cos(angle + PI/3), np.sin(angle + PI/3), 0])
            
            # 创建弯曲的磁场线
            curve_points = [
                start_point,
                mid_point,
                end_point
            ]
            
            b_line = VGroup()
            for j in range(len(curve_points) - 1):
                segment = Arrow3D(
                    start=curve_points[j],
                    end=curve_points[j+1],
                    color=BLUE,
                    thickness=0.015,
                    base_radius=0.05,
                    tip_length=0.2
                )
                b_line.add(segment)
            
            b_field_lines.add(b_line)
        
        self.play(
            FadeOut(e_group),
            FadeOut(b_group),
            FadeOut(energy_group),
            Create(axes),
            run_time=2
        )
        self.wait()
        
        self.play(Create(e_field_lines), run_time=3)
        self.wait()
        self.play(Create(b_field_lines), run_time=3)
        self.wait(2)
        
        # 旋转视角展示
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(2)
        
        # 解释文本
        explanation = Text(
            "在统一场论框架下，电场和磁场是空间不同运动状态的表现：\n电场对应空间的直线运动，磁场对应空间的旋转运动",
            font_size=28,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.wait(3)

class TimeNatureEquation(ThreeDScene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("时间的本质方程", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 时间定义方程
        time_equation = MathTex(
            r"t = \frac{s}{v}",
            font_size=70,
            color=YELLOW
        )
        self.play(Write(time_equation))
        self.wait(2)
        
        # 统一场论时间解释
        unified_time = MathTex(
            r"t = \frac{\text{空间运动路程}}{\text{空间运动速度}}",
            font_size=45,
            color=RED
        )
        self.play(Transform(time_equation, unified_time))
        self.wait(2)
        
        # 3D可视化时间概念
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-1, 7, 1],
            x_length=7,
            y_length=7,
            z_length=7,
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "tip_length": 0.2,
                "tip_width": 0.1
            }
        )
        
        # 创建螺旋轨迹表示时间流逝
        spiral = ParametricFunction(
            lambda t: np.array([
                np.cos(t),
                np.sin(t),
                t/2.5
            ]),
            t_range=[0, 5*PI],
            color=BLUE
        )
        
        self.play(
            FadeOut(time_equation),
            Create(axes),
            Create(spiral),
            run_time=2
        )
        self.wait()
        
        # 添加移动点表示现在
        moving_dot = Dot3D(color=RED, radius=0.15)
        
        def update_dot(dot, alpha):
            t = alpha * 5 * PI
            x = np.cos(t)
            y = np.sin(t)
            z = t/2.5
            dot.move_to(np.array([x, y, z]))
            return dot
        
        self.play(Create(moving_dot))
        self.play(
            UpdateFromAlphaFunc(moving_dot, update_dot),
            run_time=6,
            rate_func=linear
        )
        self.wait(2)
        
        # 解释文本
        explanation = Text(
            "在统一场论中，时间不是独立存在的，\n而是观察者对空间运动的描述。",
            font_size=32,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        explanation.to_edge(DOWN, buff=1)
        
        self.play(Write(explanation))
        self.wait(3)

class ChargeDefinitionEquation(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("电荷定义方程", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 电荷定义方程
        charge_equation = MathTex(
            r"q = \frac{F \cdot r^2}{k \cdot Q}",
            font_size=55,
            color=YELLOW
        )
        self.play(Write(charge_equation))
        self.wait(2)
        
        # 库仑定律形式
        coulomb_law = MathTex(
            r"F = k \frac{qQ}{r^2}",
            font_size=55,
            color=RED
        )
        self.play(Transform(charge_equation, coulomb_law))
        self.wait(2)
        
        # 统一场论解释
        unified_charge = MathTex(
            r"q = \text{空间运动的某种属性}",
            font_size=45,
            color=BLUE
        )
        self.play(Transform(charge_equation, unified_charge))
        self.wait(2)
        
        # 可视化电荷
        # 正电荷
        positive_charge = Circle(radius=1.5, color=RED, fill_opacity=0.7)
        plus_sign = Text("+", font_size=60, color=RED)
        positive_group = VGroup(positive_charge, plus_sign)
        positive_label = Text("正电荷", font_size=30, color=RED)
        positive_full = VGroup(positive_group, positive_label).arrange(DOWN)
        positive_full.shift(LEFT*4)
        
        # 负电荷
        negative_charge = Circle(radius=1.5, color=BLUE, fill_opacity=0.7)
        minus_sign = Text("-", font_size=60, color=BLUE)
        negative_group = VGroup(negative_charge, minus_sign)
        negative_label = Text("负电荷", font_size=30, color=BLUE)
        negative_full = VGroup(negative_group, negative_label).arrange(DOWN)
        negative_full.shift(RIGHT*4)
        
        self.play(
            FadeOut(charge_equation),
            Create(positive_full),
            Create(negative_full),
            run_time=2
        )
        self.wait()
        
        # 电场线
        field_lines = VGroup()
        for i in range(12):
            angle = i * 2*PI / 12
            # 从正电荷出发到负电荷
            line = Arrow(
                start=positive_group.get_center() + 0.8 * np.array([np.cos(angle), np.sin(angle), 0]),
                end=negative_group.get_center() + 0.8 * np.array([np.cos(angle + PI), np.sin(angle + PI), 0]),
                color=YELLOW,
                buff=0.3,
                max_tip_length_to_length_ratio=0.1
            )
            field_lines.add(line)
        
        self.play(Create(field_lines), run_time=3)
        self.wait(2)
        
        # 解释文本
        explanation = Text(
            "在统一场论中，电荷是空间运动的一种属性表现：\n正负电荷对应空间运动的两种不同状态",
            font_size=30,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        explanation.to_edge(DOWN, buff=1)
        
        self.play(Write(explanation))
        self.wait(3)

class AllEquationsShowcase(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a1a"
        
        # 标题
        title = Title("统一场论核心公式完整展示", font_size=45, color=BLUE)
        self.play(Write(title))
        self.wait()
        
        # 所有公式
        equations = VGroup(
            MathTex(r"1. \vec{r}(t) = \vec{C}t", font_size=36, color=RED),  # 时空同一化
            MathTex(r"2. \vec{r}(\theta) = a\theta\cos(\theta)\vec{i} + a\theta\sin(\theta)\vec{j} + b\theta\vec{k}", font_size=36, color=ORANGE),  # 螺旋时空
            MathTex(r"3. m = \frac{E}{c^2}", font_size=36, color=YELLOW),  # 质量定义
            MathTex(r"4. \vec{P_0} = m\vec{C}", font_size=36, color=GREEN),  # 静止动量
            MathTex(r"5. \vec{P} = m(\vec{C} - \vec{V}) ", font_size=36, color=BLUE),  # 运动动量
            MathTex(r"6. \vec{F} = \frac{d\vec{P}}{dt}", font_size=36, color=PURPLE),  # 大统一方程
            MathTex(r"7. \nabla^2 L = \frac{1}{c^2} \frac{\partial^2 L}{\partial t^2}", font_size=36, color=PINK),  # 波动方程
            MathTex(r"8. \vec{E} = \frac{\vec{F_e}}{q}", font_size=36, color=LIGHT_RED),  # 电场定义
            MathTex(r"9. \vec{B} = \frac{\vec{F_m}}{qv}", font_size=36, color=LIGHT_BLUE),  # 磁场定义
            MathTex(r"10. u = \frac{1}{2}(\epsilon_0 E^2 + \frac{B^2}{\mu_0})", font_size=36, color=LIGHT_GREEN),  # 电磁能量
            MathTex(r"11. t = \frac{s}{v}", font_size=36, color=GOLD),  # 时间本质
            MathTex(r"12. q = \frac{F \cdot r^2}{k \cdot Q}", font_size=36, color=TEAL)  # 电荷定义
        )
        
        # 排列公式
        equations.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        equations.scale(0.9)
        
        # 创建出现效果
        self.play(FadeIn(equations[0]), run_time=0.8)
        for i in range(1, len(equations)):
            self.play(FadeIn(equations[i]), run_time=0.8)
        
        self.wait(2)
        
        # 滚动查看所有公式
        self.play(equations.animate.shift(UP*10), run_time=6)
        self.wait()
        
        # 总结
        conclusion = Text(
            "统一场论通过这些核心公式，\n构建了一个描述宇宙万物的完整理论框架。",
            font_size=36,
            line_spacing=1.5,
            color=LIGHT_PINK
        )
        conclusion.to_edge(DOWN, buff=1)
        
        self.play(Write(conclusion))
        self.wait(3)