from manim import *

class BackgroundSquare(Scene):
    def construct(self):
        circle = Circle(2)
        box = SurroundingRectangle(circle, color=YELLOW, buff=MED_LARGE_BUFF)
        objects = VGroup(circle, box)
        self.play(Create(circle), FadeIn(box))
        self.wait()
        self.play(FadeOut(objects))