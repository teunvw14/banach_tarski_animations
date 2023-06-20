# Show that some points might be fixed - and remove those points from sphere 
# (don't show proof that only possible overlap is caused by fixed points) 

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim.utils.color import Colors

import random
from math import sqrt, acos
import numpy as np

config.background_color = rgb_to_color([28/255, 35/255, 31/255])
random.seed(14)

SIGMA = 0
TAU = 1
SIGMA_I = 2
TAU_I = 3

class ShowFixedPointProblem(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        title = Title("Paradoxical decomposition: why D?")
        self.add(title)

        s2_decomp_explanation = Tex(r"We have the paradoxical decomposition :").shift(UP*2)
        s2_decomp_tex = MathTex(r"\tau^{-1}{{W(\tau)}} {{M}} \cup {{W(\tau^{-1})}} {{M}} = S^2 \setminus D = \sigma^{-1}{{W(\sigma)}} {{M}} \cup {{W(\sigma^{-1})}} {{M}}").next_to(s2_decomp_explanation, DOWN)

        s2_question = Tex(r"But why \textbf{not} for the enitre sphere?")
        s2_wrong_decomp_tex = MathTex(r"\tau^{-1}{{W(\tau)}} {{M}} \cup {{W(\tau^{-1})}} {{M}} = S^2 = \sigma^{-1}{{W(\sigma)}} {{M}} \cup {{W(\sigma^{-1})}} {{M}}").next_to(s2_question, DOWN)

        s = "So why does this paradoxical decomposition we found not work for all of the unit sphere S2?"
        with self.voiceover(s):
            self.play(FadeIn(s2_decomp_explanation, s2_decomp_tex))
            self.wait(2)
            self.play(FadeIn(s2_question, s2_wrong_decomp_tex))
        
        s = "Although this equation is true; it does not qualify as a paradoxical decomposition." 
        with self.voiceover(s):
            self.play(Circumscribe(s2_wrong_decomp_tex), run_time=2)

        s = "That's because in the transfer of the paradoxical decomposition of the free group to the sphere, the disjointness is lost, which is necessary to speak of a paradoxical decomposition. The highlighted equation shows the partition we want - but it's not a partition because the sets are not necessarily disjoint."
        problem_explanation = Tex(r"Ex: $(1, 0, 0) \in M$, $(1, 0, 0) \in W(\sigma)M$").to_edge(DOWN)
        problem_1 = MathTex(r"M \cup {{W(\tau)}} {{M}} \cup {{W(\tau^{-1})}} {{M}} \cup {{W(\sigma)}} {{M}} \cup {{W(\sigma^{-1})}} {{M}}\\ \text{ is not necessarily a disjoint partition of } S^2.").next_to(problem_explanation, UP)
        box = SurroundingRectangle(problem_1, color=YELLOW)

        with self.voiceover(s):
            self.play(FadeIn(problem_1, box))
        s = "For example, the point (1, 0, 0) is unaffected by the rotation sigma, which means that we cannot be sure that it isn't contained in both M and W(sigma)M."
        with self.voiceover(s):
            self.play(FadeIn(problem_explanation))
        
        self.wait(2)


class ShowFixedPointProblemThreeD(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=.75, run_time=1.5)
        self.begin_ambient_camera_rotation(rate=0.4)
        title = Title(r"Applying $\sigma$ to $(0, 0, 1)$ does nothing")
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex(r"x"))
        y_label = axes.get_y_axis_label(Tex(r"y")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex(r"z")).shift(OUT*.25)

        s = " Let's see this visually."
        with self.voiceover(s):
            self.play(FadeIn(axes), FadeIn(x_label, y_label, z_label))

        sphere_radius = 3
        sphere = Sphere(radius=sphere_radius, fill_opacity=.35).set_color(BLUE)
        point = Dot3D([sphere_radius*1.02, 0 , 0], color=RED, radius=0.2)

        start = 0
        end = start+np.arccos(1/3)
        eps = 0.05
        sphere_radius_expanded = sphere_radius + 0.25
        arrow_curve = ParametricFunction(
                    lambda t: np.array([
                        0,
                        sphere_radius_expanded*np.cos(t),
                        sphere_radius_expanded*np.sin(t)
                    ]), color=PINK, t_range=[start, end],
                ).set_shade_in_3d(True)
        arrow_curve.stroke_width = 5
        arrow_cone = Cone(show_base=True, base_radius=0.15, height=0.5, direction=[0, -np.sin(end+eps), np.cos(end+eps)]).shift([0, sphere_radius_expanded*np.cos(end+eps), sphere_radius_expanded*np.sin(end+eps)]).set_color(PINK)

        
        self.play(
            Write(sphere), FadeIn(point, arrow_curve, arrow_cone)
        )

        explanation = Tex(r"Possibly: $(1, 0, 0) \in M$ \textit{and} $(1, 0, 0) \in W(\sigma)M$").to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(explanation)


        s = "Applying sigma to the whole sphere looks like this. The red dot is the point (1, 0, 0), and as you can see, it is entirely unaffected by the rotation"
        with self.voiceover(s):
            for _ in range(5):
                self.play(Rotate(sphere, angle=np.arccos(1/3), axis = RIGHT), run_time=2)
                sphere.rotate(angle=-np.arccos(1/3), axis=RIGHT)
        
        self.play(FadeIn(explanation))

        self.wait(2)

        
