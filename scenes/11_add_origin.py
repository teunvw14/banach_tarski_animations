# Add the origin to the paradoxical decomposition to finish the proof

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

from math import sqrt

GOLDEN_RATIO = (1/2 + sqrt(5)/2)
config.background_color = rgb_to_color([28/255, 35/255, 31/255])



class ExpandToBall(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        
        title = Title("Adding $0$ into the paradoxical decomposition")
        self.add(title)

        circle_radius = 2.5
        circle = Circle(color=BLUE, fill_opacity=0.35, radius=circle_radius)

        phi_no_overlap = Tex(r"We need $\theta$ such that $\theta^n(0) \neq 0\ \forall n$").to_edge(DOWN)

        s = "The final step now is to add the origin to the paradoxical decomposition. Luckily, this is easy to fix using the same trick that we used for adding the set D to our paradoxical decomposition of S2 minus D. Let's look at the ball from above again"
        with self.voiceover(s):    
            self.play(FadeIn(circle, phi_no_overlap))

        origin_dot = Dot(color=WHITE, radius = 0.04 )
        s = "The white dot is the origin."
        with self.voiceover(s):
            self.play(FadeIn(origin_dot))

        rotation_counter = MathTex(r"{{ D }}").set_color(RED).to_edge(LEFT).shift(RIGHT)
        rotation_point = Dot([circle_radius/3, 0, 0], radius = 0.04, color=GREEN)
        rotation_point_label = MathTex(r"(\frac{1}{3}, 0, 0)",color=GREEN).next_to(rotation_point, RIGHT)
        s = "This time, we will be looking at a rotation around a line through the point one third, 0, 0. The choice of this point is arbitrary, the only important thing is that when we rotate 0 around this line, it stays inside the ball."
        with self.voiceover(s):
            self.play(FadeIn(rotation_point, rotation_point_label))

        s = "Now, again we look at the rotations. "
        initial_number_of_d_rotations = 8
        zero_dupes_groups = VGroup()
        with self.voiceover(s):
            self.play(origin_dot.animate.set_color(RED),
                      FadeOut(rotation_point_label))
            self.play(Create(rotation_counter))
            for i in range(1, initial_number_of_d_rotations + 1):
                rotation_counter_new = MathTex(r"\theta^{" + f"{i}" + r"}({{ 0 }})").set_color_by_tex("0", RED).shift(rotation_counter.get_center())
                zero_copy = origin_dot.copy().set_color(WHITE)
                self.play(
                    Rotate(zero_copy, angle=GOLDEN_RATIO*i, axis=OUT, about_point=[circle_radius/3, 0, 0]),
                    Transform(rotation_counter, rotation_counter_new),
                    run_time = 0.75
                )
                self.wait(.2)
                self.remove(rotation_counter)
                rotation_counter = rotation_counter_new
                zero_dupes_groups.add(zero_copy)
        
        e_definition = MathTex(r"K = \bigcup_{n=0}^\infty \theta^n(0)").to_edge(RIGHT)
        total_number_of_d_rotations = 20
        s = "Again, we will define a set K similarly. K is the union of 0 with all the repeated rotations theta n of 0."
        with self.voiceover(s):
            self.play(FadeOut(phi_no_overlap))
            self.play(Write(e_definition))
            for i in range(initial_number_of_d_rotations, total_number_of_d_rotations + 1):
                rotation_counter_new = MathTex(r"\theta^{" + f"{i}" + r"}({{ D }})").set_color_by_tex("D", RED).shift(rotation_counter.get_center())
                zero_copy = origin_dot.copy().set_color(WHITE)
                self.play(
                    Rotate(zero_copy, angle=GOLDEN_RATIO*i, axis=OUT, about_point=[circle_radius/3, 0, 0]),
                    Transform(rotation_counter, rotation_counter_new),
                    run_time = 0.75
                )
                self.wait(.2)
                self.remove(rotation_counter)
                rotation_counter = rotation_counter_new
                zero_dupes_groups.add(zero_copy)
        
        e_rotated = MathTex(r"\theta^{-1}(E \setminus D) = \theta^{-1}(\bigcup_{n=1}^\infty \theta^n(D)) = \bigcup_{n=0}^\infty \theta^n(D) = E").to_edge(DOWN).shift(DOWN * 0.25)
        D_dupes_groups_blue = zero_dupes_groups.copy().set_color(YELLOW)

        s = "Now we do the same trick again: if we rotate this set K minus 0 by theta inverse, we get all of K again. The symbolic representation of this is at the bottom of the screen."
        with self.voiceover(s):
            self.play(Write(e_rotated))

        s = "Let's now see how we can use this to create a paradoxical decomposition of the whole ball."
        with self.voiceover(s):
            self.play(FadeOut(*self.mobjects))

        self.wait(2)

class ExpandToBallConclusion(VoiceoverScene):
    def construct(self):
        

        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        title = Title(r"Finally: a paradoxical decomposition of $B^3$")
        self.add(title)

        b3_partition = MathTex(r"B^3 = \Big((B \setminus 0) \cap (B^3 \setminus K)\Big) \cup \theta^{-1}\Big((B \setminus 0) \cap K\Big)").shift(UP)
        s = "Now, for the exact same reasons as before, we can partition B3 as follows"
        with self.voiceover(s):
            self.play(Write(b3_partition))


        b3o_decomp = MathTex(r"B^3 \setminus 0 &= \tau^{-1}T_1' \cup T_2' \cup \varphi^{-1}\tau^{-1}T_3' \cup \varphi^{-1}T_4' \\  &= \sigma^{-1}\Sigma_1' \cup \Sigma_2' \cup \varphi^{-1}\sigma^{-1}\Sigma_3' \cup \varphi^{-1}\Sigma_4'. ").shift(DOWN*2)
        final_eq_toelichting = Tex(r"Using the paradoxical decomposition of $B^3 \setminus 0$:").next_to(b3o_decomp, UP)

        s = "combining this, in the same way as before, with the paradoxical decomposition of the ball without the origin."
        with self.voiceover(s):
            self.play(Write(b3o_decomp), FadeIn(final_eq_toelichting))


        ball_decomp = MathTex(r"B^3 &= \tau^{-1}A_1 \cup A_2 \cup \varphi^{-1}\tau^{-1}A_3 \cup \varphi^{-1}A_4 \\  &\cup \theta^{-1}\tau^{-1}A_5 \cup \theta^{-1}A_6 \cup \theta^{-1}\varphi^{-1}\tau^{-1}A_7 \cup \theta^{-1}\varphi^{-1}A_8 \\   &= \sigma^{-1}B_1 \cup B_2 \cup \varphi^{-1}\sigma^{-1}B_3 \cup \varphi^{-1}B_4 \\ &\cup \theta^{-1}\sigma^{-1}B_5 \cup \theta^{-1}B_6 \cup \theta^{-1}\varphi^{-1}\sigma^{-1}B_7 \cup \theta^{-1}\varphi^{-1}B_8")
        s = "Gives us the final paradoxical decomposition of the ball, completing the Banach-Tarski paradox! Finally we have arrived at the result that we were working towards for the entirety of this video."
        with self.voiceover(s):
            self.play(
                FadeOut(b3o_decomp, b3_partition, final_eq_toelichting),
            )
            self.wait(1)
            self.play(Write(ball_decomp))


        s = "Again, a lot of new terms are used to make sure everything fits on screen, and we skipped over quite a few details to speed things up. For an exact treatment and definition of things, refer to the thesis."
        with self.voiceover(s):
            pass


        self.wait(2)