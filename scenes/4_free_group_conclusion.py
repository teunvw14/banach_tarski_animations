from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from math import sqrt, pi, e, log

config.background_color = rgb_to_color([28/255, 35/255, 31/255])

class FreeGroupConclusionScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        title = Title(r"The paradoxical decomposition of $F_2$", font_size = 1.5 * DEFAULT_FONT_SIZE).to_edge(UP)
        self.add(title)

        s = "So what we can conclude from all the trees is the following."
        with self.voiceover(s): pass
        s = "If we multiply all elements in F2 starting with sigma by sigma inverse on the left, we get all of the free group, except the elements starting with sigma inverse."
        decomp_tex = MathTex(r"\sigma^{-1}W(\sigma) = F_2 \setminus W(\sigma^{-1})").shift(UP)
        with self.voiceover(s):
            self.play(Write(decomp_tex))

        decomp_tex_2 = MathTex(r"F_2 = \sigma^{-1}{{W(\sigma)}} \cup {{W(\sigma^{-1})}}").next_to(decomp_tex, DOWN, buff=3*DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
        s = "This is of course equivalent to saying that F2 is the union of sigma inverse W sigma and W sigma inverse"
        with self.voiceover(s):
            self.play(Write(decomp_tex_2))
        self.wait(1)
        decomp_tex_3 = MathTex(r"F_2 = \tau^{-1}{{W(\tau)}} \cup {{W(\tau^{-1})}}").next_to(decomp_tex_2, DOWN)
        s = "But the choice for sigma was arbitrary, we could just as well have chosen to looked at the subtree of elements starting with tau."
        with self.voiceover(s): pass
        s = "So we also have that F2 is the union of tau inverse W tau and W tau inverse"
        with self.voiceover(s):
            self.play(Write(decomp_tex_3))
        

        f2_decomp_tex = MathTex(r"F_2 = {{ \{e\} }} \cup {{W(\sigma)}} \cup {{W(\sigma^{-1})}} \cup {{W(\tau)}} \cup {{W(\tau^{-1})}}").next_to(decomp_tex_3, DOWN, buff = 1)
        s = "Let's look at the original partition of F2 that we made."
        with self.voiceover(s):
            self.play(Write(f2_decomp_tex))
        
        s = "Notice that the parts in the original partition are now disjointly used in the two new partitions that we have found."
        with self.voiceover(s):    
            for obj, tex_element, color in [
                (decomp_tex_2, r"W(\sigma)", RED),
                (decomp_tex_2, r"W(\sigma^{-1})", BLUE),
                (decomp_tex_3, r"W(\tau)", ORANGE),
                (decomp_tex_3, r"W(\tau^{-1})", PINK),
            ]:
                self.play(
                    obj.animate.set_color_by_tex(tex_element, color),
                    f2_decomp_tex.animate.set_color_by_tex(tex_element, color)
                )

        conclusion_tex = Tex(r"We found a \textit{paradoxical decomposition} of $F_2$").next_to(f2_decomp_tex, DOWN)
        s = "So what we have now is called a paradoxical decomposition. We have split the free group F2 into five parts, took four of them and sort of shifted two of those parts to create two copies of F2. This is called a paradoxical decomposition"
        with self.voiceover(s):
            self.play(FadeIn(conclusion_tex))

        self.wait(2)