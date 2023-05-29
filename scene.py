from manim import *
from manim_voiceover import VoiceoverScene

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()

class FloatNumberAnimation(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        super().__init__(number, **kwargs)
        self.start = start
        self.end = end
    
    def interpolate_mobject(self, alpha: float) -> None:
        value = self.start + (self.end - self.start) * alpha
        self.mobject.set_value(value)

class NumberGoingUp(Scene):
    def construct(self):
        num = DecimalNumber(-100).set_color(GREEN).scale(5)
        num.add_updater(lambda number: number.move_to(ORIGIN))
        
        self.add(num)

        self.wait()
        
        self.play(FloatNumberAnimation(num, -100, 100), run_time=4)

        self.wait()