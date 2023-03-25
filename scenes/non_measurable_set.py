from manim import *
from math import sqrt, pi, e, log
from numpy import arctan2

config.background_color = rgb_to_color([28/255, 35/255, 31/255])

class MeasurableScene(Scene):  
    def construct(self):

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
        line.set_stroke(color = '#49b675', width = 5)
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



class NonMeasurableScene(Scene):
    def construct(self):
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
        circle = Circle(circle_radius, color='#E0DBD1')
        circle_inside_color = AnnularSector(outer_radius = circle_radius, inner_radius = 0, angle = 0).set_fill(WHITE, opacity = 0.3)
        point = Dot().set_color(RED)
        thing = VGroup(circle, circle_inside_color, point)
        self.play(
            Create(circle),
            FadeIn(circle_inside_color)
        )
        self.wait()
        def modify_angle(a):
            if a < 0:
                return 2 * pi - a
        circle_inside_color.add_updater(lambda x: x.become(
            AnnularSector(outer_radius = circle_radius, inner_radius = 0, angle = arctan2(point.get_y(), point.get_x())).set_fill(WHITE, opacity = 0.3)
        ))
        self.play(
            MoveAlongPath(point, circle),
            run_time = 2
        )
        circle_inside_color.clear_updaters()
        self.play(
            thing.animate.shift(DOWN)
        )
