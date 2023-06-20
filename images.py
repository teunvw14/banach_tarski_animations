from manim import *
from math import sqrt, pi, e, log

config.background_color = rgb_to_color([28/255, 35/255, 31/255])

class FreeGroupImage(Scene):
    def construct(self):

        title_card_tex = Title(r"De Vrije Groep $F_2$")
        f2_definition_tex = Tex(r"\textbf{Definitie (Vrije Groep $F_2$)}. De vrije groep $F_2$ voortgebracht door twee elementen $\sigma, \tau$, is de groep die bestaat uit alle eindige producten van $\sigma, \tau$ en diens inverses. De identiteit in deze groep is het 'lege product' (geschreven $e$).").scale(.75)
        example_elements_tex = Tex(r"Elementen: $\sigma\tau$, $\tau^2\sigma^{-1}$, $\sigma\tau\sigma\tau^{-2}\sigma$, etc.").next_to(f2_definition_tex, DOWN).shift(DOWN * .75)
        self.add(title_card_tex, f2_definition_tex, example_elements_tex)

class ParadoxicalDecomposition(Scene):
    def construct(self):
        paradoxical_decomposition_definition = Tex(r"\textbf{Definitie (Paradoxale decompositie)}. Zij $G$ een groep die werkt op een verzameling $X$. Dan is een paradoxale decompositie van $S \subset X$ ten aanzien van $G$ een collectie elementen $g_1, g_2, \dots, g_n, h_1, h_2, \dots, h_m \in G$ samen met een collectie paarwijs disjuncte deelverzamelingen $A_1, A_2, \dots, A_n, B_1, B_2, \dots, B_m \subset S$ met de eigenschap dat:").scale(.75)
        eq = MathTex(r"\bigcup_{i=1}^n g_i A_i = S = \bigcup_{i=1}^m h_i B_i").next_to(paradoxical_decomposition_definition, DOWN)

        self.add(paradoxical_decomposition_definition, eq)

class EDScene(Scene):
    def construct(self):
        #(RED, BLUE, GREEN)
        square = Square(4, color=RED, fill_opacity=0.5)

        two_triangles_coordinates = [
            [2*sqrt(2), 2*sqrt(2), 0],
            [-2*sqrt(2), -2*sqrt(2), 0],
            [2*sqrt(2), -2*sqrt(2), 0],
            [-2*sqrt(2), 2*sqrt(2), 0]
        ]
        two_triangles = Polygon(
            *two_triangles_coordinates,
            color=BLUE,
            fill_opacity=0.5
        )

        final_polygon = VGroup(
            Polygon(
                *[np.array(p)* (1/2) for p in two_triangles_coordinates],
                color = GREEN,
                fill_opacity=0.5
            ),
            Polygon(
                [2*sqrt(2), 2*sqrt(2), 0],
                [2*sqrt(2), -2*sqrt(2), 0],
                [sqrt(2), -sqrt(2), 0],
                [sqrt(2), sqrt(2), 0],
                color = GREEN,
                fill_opacity=0.5
            ).shift(RIGHT),
            Polygon(
                [-sqrt(2), sqrt(2), 0],
                [-sqrt(2), -sqrt(2), 0],
                [-2*sqrt(2), -2*sqrt(2), 0],
                [-2*sqrt(2), 2*sqrt(2), 0],
                color = GREEN,
                fill_opacity=0.5
            ).shift(LEFT)
        )

        polys = VGroup(square, two_triangles, final_polygon)

        arrow_1 = Arrow(start=LEFT, end=RIGHT)
        arrow_2 = arrow_1.copy()
        
        objects = VGroup(square, arrow_1, two_triangles, arrow_2, final_polygon).scale(0.55).arrange(RIGHT)

        A_label = MathTex("A").set_color(RED).shift(square.get_center()).shift(2.25*UP)
        B_label = MathTex("B").set_color(BLUE).shift(two_triangles.get_center()).shift(2.25*UP)
        C_label = MathTex("C").set_color(GREEN).shift(final_polygon.get_center()).shift(2.25*UP)
        labels = VGroup(A_label, B_label, C_label)
        self.add(labels)

        self.add(objects)
        # add title
        explanation = MathTex(r"{{A}} \sim {{B}} \sim {{C}}").to_edge(DOWN)
        for part, color in [
            ("A", RED),
            ("B", BLUE),
            ("C", GREEN)
        ]:
            explanation.set_color_by_tex(part, color)

        self.add(explanation)