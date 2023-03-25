from manim import *

config.background_color = rgb_to_color([28/255, 35/255, 31/255])

class IntroScene(Scene):
    def construct(self):
        IntroText = Tex(r"\textbf{Non-measurable sets and \\ the Banach-Tarski Paradox}", font_size=70)

        self.wait()

        self.play(DrawBorderThenFill(IntroText), run_time = 2)
        self.play(IntroText.animate.shift(2 * UP))
        
        self.wait()