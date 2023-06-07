from manim import *

config.background_color = rgb_to_color([28/255, 35/255, 31/255])


class BackgroundSquare(Scene):
    def construct(self):
        circle = Circle(2)
        box = SurroundingRectangle(circle, color=YELLOW, buff=MED_LARGE_BUFF)
        objects = VGroup(circle, box)
        self.play(Create(circle), FadeIn(box))
        self.wait()
        self.play(FadeOut(objects))

class Rotation(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES, zoom=.75, run_time=1.5)
        title = Tex(r"Rotation $\tau$ (along the $y$-axis)").to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex(r"x"))
        y_label = axes.get_y_axis_label(Tex(r"y")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex(r"z"), rotation=-PI/2).shift(OUT*.25)

        sphere_radius = 2.5
        sphere = Sphere(radius=sphere_radius, fill_opacity=.5, resolution=(64, 64)).set_color(BLUE)

        start = 0
        end = start+np.arccos(1/3)
        eps = 0.05
        sphere_radius_expanded = sphere_radius + 0.25
        arrow_curve = ParametricFunction(
                    lambda t: np.array([
                        sphere_radius_expanded*np.cos(t),
                        0,
                        sphere_radius_expanded*np.sin(t)
                    ]), color=PINK, t_range=[start, end],
                ).set_shade_in_3d(True)
        arrow_curve.stroke_width = 5
        arrow_cone = Cone(show_base=True, base_radius=0.15, height=0.5, direction=[-np.sin(end+eps), 0, np.cos(end+eps)]).shift([sphere_radius_expanded*np.cos(end+eps), 0, sphere_radius_expanded*np.sin(end+eps)]).set_color(PINK)


        self.add(title, sphere, axes, x_label, y_label, z_label, arrow_curve, arrow_cone)
