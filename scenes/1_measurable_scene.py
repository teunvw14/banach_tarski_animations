from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from math import sqrt, pi, e, log
from numpy import arctan2

def modified_arctan2(x, y):
    a = arctan2(x, y)
    if a < 0:
        return 2 * pi + a
    else:
        return a

config.background_color = rgb_to_color([28/255, 35/255, 31/255])

class MeasurableScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        top_text = Tex(r"\textbf{(Non-)measurable sets}", font_size=70)

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
        
        s = "When we talk about size, we have an intuitive idea of what it means:"
        with self.voiceover(s):
            pass
        s = "the interval from -1 to 1 has has “length” two, and we know it for every interval."
        with self.voiceover(s):
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
        
        # add in area label
        square_area_label = DecimalNumber(2)
        square_area_label.add_updater(lambda x: x.set_value(line_width_label.get_value() * square_height_label.get_value()))
        
        self.add(square_height_brace, square_height_label)
        # Transform the line into a square
        self.play(
            Transform(square_as_line, square),
            FadeIn(square_height_brace, square_height_label, square_area_label)
        )
        
        self.remove(line)

        square_sizes = [
            (4, 3), 
            (8, log(2)),
            (sqrt(2), 4.5),
            (2, 2)
        ]
        s = "Similarly, we can expand that notion to two dimensions: rectangle sizes are the length of the width multiplied by the height"
        with self.voiceover(s):
            for (w, h) in square_sizes:
                self.play(
                    square_as_line.animate.stretch_to_fit_width(w)
                    .stretch_to_fit_height(h)
                )
                self.wait(0.5)

        s = "Of course, this notion can be generalized to any higher dimension if you'd like."
        with self.voiceover(s):
            pass
 
        self.wait()
        self.play(Transform(square_as_line, square))
