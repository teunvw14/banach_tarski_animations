from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from math import sqrt, pi, e, log
from numpy import arctan2
from random import shuffle

config.background_color = rgb_to_color([28/255, 35/255, 31/255])

def modified_arctan2(x, y):
    a = arctan2(x, y)
    if a < 0:
        return 2 * pi + a
    else:
        return a

class NonMeasurableScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": '#E0DBD1',
                "stroke_width": 2,
                "stroke_opacity": 0.2
            },
            faded_line_ratio = 3
        )
        self.add(number_plane)
        
        title = Title("Constructing a non measurable set on $S^1$")
        s = "When trying to generalize a notion of size to arbitrary sets however, we run into trouble. For some sets, it ends up being impossible to say what its 'size' is. We call these sets 'non-measurable' In this section, we will give an example of such a non-measurable set. "
        with self.voiceover(s):
            self.play(Create(title))

        circle_radius = 2.5
        circle = Circle(circle_radius, color=WHITE)
        circle_inside_color = AnnularSector(outer_radius = circle_radius, inner_radius = 0, angle = 0).set_fill(WHITE, opacity = 0.3)
        point = Dot([circle_radius, 0.0, 0.0]).set_color(RED)
        original_point_label = Tex(r"p", color = RED).next_to(point).shift(0.3 * UP)
        original_point_coordinates = MathTex(r"= (1, 0)", color=RED).next_to(original_point_label, buff = 0.2 * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
        circle_text = Tex(r"The unit circle: $S^1 = \{x \in \mathbb{R}^2: ||x|| = 1\}$").to_corner(UP + LEFT)

        s = "We will create a non-measurable subset on S1."
        with self.voiceover(text=s):
            self.play(
                Create(circle),
                FadeIn(circle_inside_color, circle_text),
                FadeOut(title)
            )

        s = "We will do this by creating equivalence classes on the points of the unit circle by taking any two points to be equivalent when there exists some rational rotation to take the first point to the second."
        with self.voiceover(s):
            self.play(
                FadeIn(original_point_label, original_point_coordinates),
                FadeIn(point)
            )
            self.wait()

        s = "Let's look at how such an equivalence class is created by looking at the point 1, 0."
        with self.voiceover(s):
            pass
        circle_inside_color.add_updater(lambda x: x.become(
            AnnularSector(outer_radius = circle_radius, inner_radius = 0, angle = modified_arctan2(point.get_y(), point.get_x())).set_fill(WHITE, opacity = 0.3)
        ))

        # add a label for the current angle
        def angle_label_with_angle(angle):
            return Tex(r"$\theta = " + f"{angle}$ rad")
        angle_label = angle_label_with_angle(0).next_to(circle).shift(UP + RIGHT)
        self.play(FadeIn(angle_label))

        # s: We define a relation ~ on S1 by letting two points p and q on S1
        # be equivalent, whenever there is a rational rotation phi such that 
        # p can be transformed into q by a rational rotation
        total_rotated = 0
        point_class_first_point = point.copy()
        self.add(point_class_first_point)
        points = VGroup(point_class_first_point)

        rotations = [
            (1, 4), (5, 3), (21, 8), (34, 7), (17, 3), (15, 11), (150, 68), (68, 19), (23, 6)
        ]
        shuffle(rotations) 
        for (num, denom) in rotations:
            a = num / denom
            a_tex = r"\frac" + "{" + f"{num}" + "}{" + f"{denom}" + "}"
            rotation_amount = a - total_rotated
            self.play(
                Transform(
                    angle_label, 
                    angle_label_with_angle(a_tex).next_to(circle).shift(UP + RIGHT)
                ),
                Rotate(point, about_point=ORIGIN, angle=rotation_amount),
                run_time = 1.5
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
            FadeOut(original_point_label, original_point_coordinates),
            FadeOut(angle_label),
            FadeIn(p_class_tex_start),
            Transform(points, p)
        )
        self.wait()

        s = "we will use the notation p in brackets to mean the equivalence class of p. Of course we didn't see all the points in the equivalence class, since there are infinitely many."
        with self.voiceover(text = s):
            self.play(
                FadeOut(points),
                Transform(p_class_tex_start, p_class_tex_end)
            )

        s = "Let's see that process for a few more points."
        with self.voiceover(s):
            self.play(FadeOut(p_class_tex_start))

        for color, coordinates, label in [
            (BLUE, [0,1,0], r"(0, 1)"),
            (GREEN_B, [-(np.sqrt(2)/2), (np.sqrt(2)/2), 0], r"(-\frac{\sqrt{2}}{2}, \frac{\sqrt{2}}{2})"),
            # (LIGHT_PINK, [1/2, -np.sqrt(3/4),0], r"(\frac{1}{2}, \frac{\sqrt{3}}{2})")
        ]:
            coordinates = np.array(circle_radius) * coordinates
            rotating_point = Dot(coordinates, color=color)
            
            circle_inside_color.add_updater(lambda x: x.become(
            AnnularSector(outer_radius = circle_radius, inner_radius = 0, angle = modified_arctan2(rotating_point.get_y(), rotating_point.get_x())).set_fill(WHITE, opacity = 0.3)
            ))
            
            point_class_first_point = rotating_point.copy()
            self.add(point_class_first_point)
            points = VGroup(point_class_first_point)

            rotating_point_coordinates = MathTex(f"{label}", color=color).next_to(rotating_point, buff = 0.2 * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)

            total_rotated = 0

            self.play(
                FadeIn(rotating_point_coordinates),
                FadeIn(angle_label)
            )

            shuffle(rotations)
            for (num, denom) in rotations:
                a = num / denom
                a_tex = r"\frac" + "{" + f"{num}" + "}{" + f"{denom}" + "}"
                rotation_amount = a - total_rotated
                self.play(
                    Transform(
                        angle_label, 
                        angle_label_with_angle(a_tex).next_to(circle).shift(UP + RIGHT)
                    ),
                    Rotate(rotating_point, about_point=ORIGIN, angle=rotation_amount),
                    run_time = 1
                )
                new_point = rotating_point.copy()
                self.add(new_point)
                points.add(new_point)
                total_rotated = a

            # add to VGroup for easy deletion
            points.add(rotating_point)
            
            class_tex = Tex(r"[\ \ ]").next_to(circle).shift(RIGHT+UP)
            self.add(class_tex)
            # p_class_tex_end = MathTex(r"{{[}} p {{]}}").next_to(circle).shift(RIGHT+UP).set_color_by_tex(r"p", color)
            p = Dot(color = color).move_to(class_tex)
            self.play(
                FadeIn(class_tex),
                FadeOut(rotating_point_coordinates),
                FadeOut(angle_label),
                Transform(points, p)
            )
            self.wait()
            self.play(
                FadeOut(points, class_tex)
            )
        
        classes_tex = MathTex(r"\text{Equivalence classes = }\{[{{p}}], [{{(0, 1)}}], [{{(-\frac{1}{2}\sqrt{2}, \frac{1}{2}\sqrt{2})}}], \dots\}").to_edge(UP)
        s = "Now, we can do this for all points of the unit circle, so that we have a collection of all equivalence classes."
        with self.voiceover(text=s):
            self.play(
                FadeOut(number_plane, circle, circle_inside_color, circle_text),
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

        m_explanation = Tex("Non-measurable set: ", font_size=40).next_to(M_tex_start, LEFT).shift(UP * .05)
        self.play(FadeIn(m_explanation))


        s = "Notice now that we can form the whole circle again by looking at all rational rotations of M"
        s_1_from_M_tex = MathTex(r"S^1 = \bigcup_{\varphi \in Q} e^{i\varphi} M").to_edge(DOWN).shift(UP)
        with self.voiceover(s):
            self.play(Write(s_1_from_M_tex))
        
        s = "Note that these rotations of M are all disjoint!" 
        self.voiceover(s)
        
        self.play(
            FadeOut(classes_tex, m_explanation, ),
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
        s = "It should be clear that neither of these options is a good choice. As a result, we say that M is non-measurable. You might be wondering why this is relevant to the Banach-Tarski paradox? It is relevant because the parts that we will divide the ball into, are going to be non-measurable. In fact, there is no other way for the paradox to make sense; if we could assign a size to each of these parts, then the Banach-Tarski paradox would imply that the volume of one unit ball is the same as the volume of two unit balls - and that obviously cannot be the case."
        with self.voiceover(s):
            self.play(
                FadeIn(cross)
            )

        self.wait(2)
