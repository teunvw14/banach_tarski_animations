from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from math import sqrt, pi, e, log
from numpy import arctan2


config.background_color = rgb_to_color([28/255, 35/255, 31/255])

class MeasurableScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        top_text = Tex(r"\textbf{Measures and measurable sets}", font_size=70)

        self.play(Write(top_text), run_time = 2)
        self.play(top_text.animate.shift(3 * UP))
        top_text.add_background_rectangle(color=BLACK, opacity=1, buff = MED_SMALL_BUFF)

        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": '#E0DBD1',
                "stroke_width": 2,
                "stroke_opacity": 0.2
            },
            faded_line_ratio = 2
        ).set_stroke(opacity=.5)
        self.add(number_plane)

        line = Line([-1, 0, 0], [1, 0, 0])
        line.set_stroke(color = RED, width = 5)
        line_brace = BraceBetweenPoints(line.get_start(), line.get_end())
        line_width_label = DecimalNumber(2).next_to(line_brace, DOWN)
        line_width_indicator = Group(line_brace, line_width_label)

        # line_width_label.add_updater(lambda x: x.next_to(line_brace, DOWN))
        self.play(
            Create(line), FadeIn(line_brace), Write(line_width_label)
        )

        # text_one_dim = Tex(r"\textbf{Size in $\mathbb{R}$}", font_size=70).move_to(top_text.get_center())
        # self.play(UnWrite(top_text, ))

        line_brace.add_updater(lambda x: x.become(BraceBetweenPoints(line.get_start(), line.get_end())))
        line_width_label.add_updater(lambda x: x.set_value(line.get_length()))
        for length in [4, 8, 128, 2 * pi, e, 2]:
            self.play(line.animate.stretch_to_fit_width(length))
            self.wait(0.5)

        # We won't need these updaters after this point
        line_brace.clear_updaters()
        line_width_label.clear_updaters()

        # Make two squares, one that overlaps with the line exactly, so that we
        # can transform it into `square`
        square_as_line = Polygon([1, 0, 0], [1, 0, 0], [-1, 0, 0], [-1, 0, 0]).shift([0, -1, 0])
        square = Polygon([1, 1, 0], [1, -1, 0], [-1, -1, 0], [-1, 1, 0]).set_fill(opacity = .5)

        self.play(line.animate.shift(DOWN), line_width_indicator.animate.shift(DOWN))

        # New brace for height
        square_height_brace = BraceBetweenPoints(square.points[3], square.points[0])
        square_height_brace.add_updater(lambda x: x.become(BraceBetweenPoints(square_as_line.points[3], square_as_line.points[0])).next_to(square_as_line, RIGHT))
        # Label for the height
        square_height_label = DecimalNumber(2).next_to(square_height_brace, RIGHT)
        square_height_label.add_updater(lambda x: x.set_value(abs(square_as_line.points[3][1] - square_as_line.points[0][1])).next_to(square_height_brace, RIGHT))
        # Reuse brace used for the line, change updater
        line_brace.add_updater(lambda x: x.become(BraceBetweenPoints(square_as_line.points[7], square_as_line.points[3])).next_to(square_as_line, DOWN))
        # Label (reused) for width
        line_width_label.add_updater(lambda x: x.set_value(abs(square_as_line.points[7][0] - square_as_line.points[3][0])).next_to(line_brace, DOWN))
        
        self.add(square_height_brace, square_height_label)
        # Transform the line into a square
        self.play(
            Transform(square_as_line, square),
            FadeIn(square_height_brace, square_height_label)
        )
        
        self.remove(line)

        square_sizes = [
            (4, 3), 
            (8, log(2)),
            (sqrt(2), 4.5),
            (2, 2)
        ]
        for (w, h) in square_sizes:
            self.play(
                square_as_line.animate.stretch_to_fit_width(w)
                .stretch_to_fit_height(h)
            )
            self.wait(0.5)

        self.wait()
        self.play(Transform(square_as_line, square))

def modified_arctan2(x, y):
    a = arctan2(x, y)
    if a < 0:
        return 2 * pi + a
    else:
        return a

class NonMeasurableScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": '#E0DBD1',
                "stroke_width": 2,
                "stroke_opacity": 0.2
            },
            faded_line_ratio = 3
        )
        self.add(number_plane)
        
        circle_radius = 2.5
        circle = Circle(circle_radius)
        circle_inside_color = AnnularSector(outer_radius = circle_radius, inner_radius = 0, angle = 0).set_fill(WHITE, opacity = 0.3)
        point = Dot([circle_radius, 0.0, 0.0]).set_color(RED)
        original_point_label = Tex(r"p", color = RED).next_to(point).shift(0.3 * UP)
        circle_text = Tex(r"The unit circle: $S^1 = \{x \in \mathbb{R}^2: ||x|| = 1\}$").to_corner(UP + LEFT)

        s = "We will create a non-measurable subset on S1"
        with self.voiceover(text=s):
            self.play(
                Create(circle),
                FadeIn(circle_inside_color, circle_text)
            )
            self.wait()
            self.play(
                FadeIn(original_point_label),
                FadeIn(point)
            )
            self.wait()
            
        circle_inside_color.add_updater(lambda x: x.become(
            AnnularSector(outer_radius = circle_radius, inner_radius = 0, angle = modified_arctan2(point.get_y(), point.get_x())).set_fill(WHITE, opacity = 0.3)
        ))
        # add a label for the current angle
        def angle_label_with_angle(angle):
            return Tex(r"$\theta = " + f"{angle}$ rad")
        angle_label = angle_label_with_angle(0).next_to(circle).shift(UP + RIGHT)
        self.play(FadeIn(angle_label))

        # create a 
        # p_class_tex_end = Tex(r"}")
        # p_class_tex_start = Tex(r"[p] = {p")
        # p_class_tex = VGroup(p_class_tex_start, p_class_tex_end)
        # def add_p_class_point():
        #     p_class_tex.remove(p_class_tex_end)
        #     p_class_tex.add(
        #         Tex(r",\ ")
        #     )
        #     p_class_tex.add(p_class_tex_end)

        # s: We define a relation ~ on S1 by letting two points p and q on S1
        # be equivalent, whenever there is a rational rotation phi such that 
        # p can be transformed into q by a rational rotation
        total_rotated = 0
        point_class_first_point = point.copy()
        self.add(point_class_first_point)
        points = VGroup(point_class_first_point)
        for (num, denom) in ((1, 4), (5, 3), (21, 8), (34, 7), (17, 3)):
            a = num / denom
            a_tex = r"\frac" + "{" + f"{num}" + "}{" + f"{denom}" + "}"
            rotation_amount = a - total_rotated
            self.play(
                Transform(
                    angle_label, 
                    angle_label_with_angle(a_tex).next_to(circle).shift(UP + RIGHT)
                ),
                Rotate(point, about_point=ORIGIN, angle=rotation_amount),
                run_time = 1.75
            )
            new_point = point.copy()
            self.add(new_point)
            points.add(new_point)
            total_rotated = a

        points.add(point)
        
        p_class_tex_start = Tex(r"[\ \ ]").next_to(circle).shift(RIGHT+UP)
        p_class_tex_end = MathTex(r"{{[}} p {{]}}").next_to(circle).shift(RIGHT+UP).set_color_by_tex(r"p", RED)
        p = Dot(color = RED).move_to(p_class_tex_start)
        self.play(
            FadeOut(original_point_label),
            FadeOut(angle_label),
            FadeIn(p_class_tex_start),
            Transform(points, p)
        )
        self.wait()
        # original_point_label.generate_target()
        # original_point_label.target.move_to(p_class_tex_start)

        s = "we will use the notation p in brackets to mean the equivalence class of p"
        with self.voiceover(text = s) as voiceover:
            self.play(
                FadeOut(points),
                Transform(p_class_tex_start, p_class_tex_end)
            )

        classes_tex = MathTex(r"\text{Equivalence classes = }\{[{{p}}], [{{(0, 1)}}], [{{(-\frac{1}{2}\sqrt{2}, \frac{1}{2}\sqrt{2})}}], \dots\}").to_edge(UP)
        s = "Now, we can do this for all points, so that we have a collection of all equivalence classes."
        with self.voiceover(text=s):
            self.play(
                FadeOut(number_plane, circle, circle_inside_color, p_class_tex_start, circle_text),
                FadeIn(classes_tex)
            )
        
        M_tex_start = MathTex(r"M = \{").next_to(classes_tex, DOWN).shift(2*LEFT+ .5 * DOWN)
        M_group = VGroup(M_tex_start)
        s = "Using the Axiom of Choice, we can pick exactly one point from each of these equivalence classes. This will be our non-measurable set M."
        with self.voiceover(text=s):
            self.play(
                Write(M_tex_start)
            )
            for i, point in enumerate((
                classes_tex.submobjects[1],
                classes_tex.submobjects[3],
                classes_tex.submobjects[5])):
                new_point = point.copy()
                if i > 0:
                    self.play(
                        new_point.animate.next_to(M_group[2*i], RIGHT).shift(UP*.15)
                    )
                else:
                    self.play(
                        new_point.animate.next_to(M_group[2*i], RIGHT)
                    )
                comma = MathTex(r",").next_to(new_point, RIGHT).shift(DOWN * 0.15)
                self.play(
                    Write(comma), run_time = .1
                )
                M_group.add(new_point, comma)

            M_tex_end = MathTex(r"\ \dots\}").next_to(M_group[-1], RIGHT).shift(UP * .15)
            M_group.add(M_tex_end)
            self.play(Write(M_tex_end))

        s = "Notice now that we can form the whole circle again by looking at all rational rotations of M"
        s_1_from_M_tex = MathTex(r"S^1 = \bigcup_{\varphi \in Q} e^{i\varphi} M").to_edge(DOWN).shift(UP)
        with self.voiceover(s):
            self.play(Write(s_1_from_M_tex))
        
        s = "Note that these rotations of M are all disjoint!" 
        self.voiceover(s)
        
        self.play(
            FadeOut(classes_tex),
            M_group.animate.to_edge(UP).shift(DOWN * .5 + 3 * LEFT),
            s_1_from_M_tex.animate.to_corner(RIGHT + UP).shift(DOWN * .5)
        )

        sigma_intro_text = Tex(r"Then by $\sigma$-additivity and rotation invariance:").shift(UP)
        sigma_additivity_M_tex = MathTex(r"\mu(S^1) = \sum_{\varphi \in \mathbb{Q}} \mu(e^{i\varphi} M) = \sum_{\varphi \in \mathbb{Q}} \mu(M).").next_to(sigma_intro_text, DOWN).shift(DOWN)

        s = "By sigma additivity and rotation invariance, we then get the following"
        with self.voiceover(s):
            self.play(
                FadeIn(sigma_intro_text),
                Write(sigma_additivity_M_tex)
            )
        self.wait(3)

        what_is_mu_m_text = Tex(r"So then what is $\mu(M)$?").to_edge(DOWN).shift(UP*.25)
        s = "So then, what is mu of M?"
        with self.voiceover(s):
            self.play(Write(what_is_mu_m_text))

        self.play(
            sigma_additivity_M_tex.animate.to_edge(UP),
            FadeOut(what_is_mu_m_text, sigma_intro_text, M_group, s_1_from_M_tex)
        )
        
        opt_1_tex = MathTex(r"\mu(M) = 0 \Rightarrow  \mu(S^1) = \sum_{\varphi \in \mathbb{Q}} 0 = 0").next_to(sigma_additivity_M_tex, DOWN).shift(DOWN)
        opt_2_tex = MathTex(r"\mu(M) = m > 0 \Rightarrow  \mu(S^1) = \sum_{\varphi \in \mathbb{Q}} m = +\infty").next_to(opt_1_tex, DOWN).shift(DOWN)

        s = "If we take mu of M is zero, then the measure of the unit circle must also be zero."
        with self.voiceover(s):
            self.play(Write(opt_1_tex))

        s = "But if we take mu of M to be nonzero, then the measure of the unit circle must be infinite!"
        with self.voiceover(s):
            self.play(Write(opt_2_tex))


        cross = Cross(VGroup(opt_1_tex, opt_2_tex))
        s = "It should be clear that neither of these options is a good choice."
        with self.voiceover(s):
            self.play(
                FadeIn(cross)
            )

        self.wait(2)



class SphereRotation(ThreeDScene):
    def construct(self):
        # Create 3D axes
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)

        # Create a 3D sphere
        sphere = Sphere(radius=2, resolution=(30, 30))
        self.play(Create(sphere))

        # Create a point
        point = Dot(color=RED)

        # Calculate the initial position of the point on the sphere
        radius = sphere.radius
        theta = 0.3  # Angle of rotation along the latitude
        phi = 0.5  # Angle of rotation along the longitude
        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)
        point.move_to(np.array([x, y, z]))

        self.add(point)

        # Animate the rotation
        # self.play(
            # Rotating(point, about_point=sphere.get_center(), axis=OUT, radians=2 * PI, run_time=5),§
        self.move_camera(phi=75 * DEGREES, theta=360 * DEGREES, run_time=5)

        self.wait(2)
