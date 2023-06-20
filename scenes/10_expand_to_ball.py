# Show how the paradoxical decomposition on the sphere can be expanded to 

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

import random
from math import sqrt

config.background_color = rgb_to_color([28/255, 35/255, 31/255])


def get_random_point_on_sphere(radius):
    rand_x = random.uniform(-1, 1)
    rand_y = random.uniform(-sqrt(1 - rand_x**2), sqrt(1 - rand_x**2))
    rand_z = sqrt(1 - (rand_x**2 + rand_y**2)) * random.choice([-1, 1])
    return [radius * rand_x, radius * rand_y, radius * rand_z]


class ExpandToBall(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        
        title = Title("From $S^2$ to (almost) $B^3$")

        self.add(title)

        full_decomp = MathTex(r"S^2 &= \tau^{-1}T_1 \cup T_2 \cup \varphi^{-1}\tau^{-1}T_3 \cup \varphi^{-1}T_4 \\ &= \sigma^{-1}\Sigma_1 \cup \Sigma_2 \cup \varphi^{-1}\sigma^{-1}\Sigma_3 \cup \varphi^{-1}\Sigma_4").shift(UP)
        full_decomp_toelichting = Tex("Paradoxical decomposition of $S^2$:").next_to(full_decomp, UP)

        b3_decomp_start = Tex("Paradoxical decomposition of $B^3$").shift(DOWN*2.5)
        arrow = Arrow(start = UP, end=DOWN).shift(DOWN)

        s = "Alright. Now that we have a paradoxical decomposition on the sphere, there is only one thing left to do for us to finish the proof of the Banach-Tarski paradox: to expand the paradoxical decomposition of the sphere onto all of the unit ball. "
        with self.voiceover(s):
            self.play(FadeIn(full_decomp, full_decomp_toelichting))
            self.wait(2)
            self.play(FadeIn(arrow, b3_decomp_start))

        b3o_explanation = Tex("Paradoxical decomposition of $B^3 \setminus 0$:").to_edge(UP).shift(DOWN*1.5)
        solution = Tex(r"Identify every point {{$p$}} with {{the line from the origin to $p$}}.").set_color_by_tex("$p$", RED).set_color_by_tex("the line from the origin to $p$", BLUE)
        solution_symbolic = MathTex(r"{{p}} \leftrightarrow {{ \{x \in B^3 \setminus 0: \exists r \in (0, 1], x = rp\} }}").next_to(solution, DOWN).set_color_by_tex("p", RED).set_color_by_tex(r"\{x \in B^3 \setminus 0: \exists r \in (0, 1], x = rp\}", BLUE)

        s = "The first step here is actually quite simple. We can expand the decomposition to the ball with the origin removed by simply identifying each point p of the sphere with the points between p and the origin"
        with self.voiceover(s):
            self.play(FadeOut(full_decomp, full_decomp_toelichting, arrow, b3_decomp_start))
            self.wait(0.5)
            self.play(FadeIn(b3o_explanation, solution, solution_symbolic))

        s = "This works because when we rotate points on a sphere, this rotations works the exact same way on that line as it does on the point of the sphere. "
        with self.voiceover(s):
            pass
        s = "Let's see this in 3D"
        with self.voiceover(s):
            self.play(solution_symbolic.animate.to_edge(DOWN))



class ExpandToBallThreeD(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        
        title = Title("From $S^2$ to (almost) $B^3$")
        self.add_fixed_in_frame_mobjects(title)

        solution_symbolic = MathTex(r"{{p}} \leftrightarrow {{ \{x \in B^3 \setminus 0: \exists r \in (0, 1], x = rp\} }}").to_edge(DOWN).set_color_by_tex("p", RED).set_color_by_tex(r"\{x \in B^3 \setminus 0: \exists r \in (0, 1], x = rp\}", BLUE)
        self.add_fixed_in_frame_mobjects(solution_symbolic)

        self.set_camera_orientation(phi=65 * DEGREES, theta=225 * DEGREES, zoom=.75, run_time=1.5)
        self.begin_ambient_camera_rotation(rate=0.4)

        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex(r"x"))
        y_label = axes.get_y_axis_label(Tex(r"y")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex(r"z"), rotation=-PI/2).shift(OUT*.25)

        sphere_radius = 2.5
        sphere = Sphere(radius=sphere_radius, fill_opacity=.5).set_color(BLUE)

        self.add(title, sphere, axes, x_label, y_label, z_label)

        dots_lines_pairs = VGroup()
        lines = VGroup()
        dots = VGroup()
        for color in (PINK, YELLOW, GREEN, ORANGE):
            dot = Dot3D(get_random_point_on_sphere(radius=sphere_radius), color=color)
            dots.add(dot)
            line = Line3D(start=ORIGIN, end=dot, color=color)
            lines.add(line)
            pair = VGroup(dot, line)
            dots_lines_pairs.add(pair)
            
        s = "Here are a few points on the unit sphere"
        with self.voiceover(s):
            self.play(FadeIn(dots))
        
        s = "Let's remove the sphere so we can see the next part more clearly"
        with self.voiceover(s):
            self.play(FadeOut(sphere))

        s = "Now, let's see the lines from the origin to the points."
        with self.voiceover(s):
            self.play(FadeIn(lines))
        
        s = "When we rotate all these objects, you should see that rotating just the points is very similar to rotating the lines to them. It is as if the points on the line represent the same point but for all balls with radius smaller than 1. Well actually, it's exactly like that. "
        with self.voiceover(s):
            for ax in (UP, LEFT, OUT, DOWN, IN):
                for line, dot in dots_lines_pairs:
                    self.play(
                            line.animate.rotate(angle=sqrt(2), axis=ax, about_point=ORIGIN),
                            dot.animate.rotate(angle=sqrt(2), axis=ax, about_point=ORIGIN),
                        run_time=1
                    )

        s = "Note that these lines don't include the origin, because otherwise it would be identified with all points on the sphere."
        with self.voiceover(s):
            pass


        self.wait(2)

class ExpandToBallConclusion(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        title = Title("From $S^2$ to (almost) $B^3$")

        self.add(title)

        full_decomp = MathTex(r"S^2 &= \tau^{-1}T_1 \cup T_2 \cup \varphi^{-1}\tau^{-1}T_3 \cup \varphi^{-1}T_4 \\ &= \sigma^{-1}\Sigma_1 \cup \Sigma_2 \cup \varphi^{-1}\sigma^{-1}\Sigma_3 \cup \varphi^{-1}\Sigma_4").shift(UP)
        full_decomp_toelichting = Tex("Original decomposition of $S^2$:").next_to(full_decomp, UP)
        box_1 = SurroundingRectangle(VGroup(full_decomp, full_decomp_toelichting), color=BLUE)

        new_sets = MathTex(r"T_i' &= \{x \in B^3 \setminus 0: \exists p \in T_i, r \in (0, 1], x = rp\}, \\ \Sigma_i' &= \{x \in B^3 \setminus 0: \exists p \in \Sigma_i, r \in (0, 1], x = rp\}.").shift(DOWN*0.85)
        expanded_decomp = MathTex(r"B^3 \setminus 0 &= \tau^{-1}T_1' \cup T_2' \cup \varphi^{-1}\tau^{-1}T_3' \cup \varphi^{-1}T_4' \\  &= \sigma^{-1}\Sigma_1' \cup \Sigma_2' \cup \varphi^{-1}\sigma^{-1}\Sigma_3' \cup \varphi^{-1}\Sigma_4'. ").to_edge(DOWN)
        box = SurroundingRectangle(expanded_decomp, color=YELLOW)

        s = "So, because our argument depended only on applying rotations to points, we can expand the paradoxical decomposition as follows."
        with self.voiceover(s):
            self.play(Write(full_decomp), FadeIn(full_decomp_toelichting, box_1))

        s = "The sets T i and Sigma i, which are defined on the sphere, can be altered by identifying the points in them with the lines to the points. We call these sets T i prime and Sigma i prime."
        with self.voiceover(s):
            self.play(Write(new_sets))
        
        s = "This then gives rise to the following paradoxical decomposition of the unit ball B3 without the origin."
        with self.voiceover(s):
            self.play(Write(expanded_decomp), FadeIn(box))