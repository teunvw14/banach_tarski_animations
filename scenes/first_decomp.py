from manim import *
from manim_voiceover import VoiceoverScene
from manim.utils.color import Colors
import random
from math import sqrt, acos

config.background_color = rgb_to_color([28/255, 35/255, 31/255])
random.seed(14)

SIGMA = 0
TAU = 1
SIGMA_I = 2
TAU_I = 3


def get_random_point_on_sphere(radius):
    rand_x = random.uniform(-1, 1)
    rand_y = random.uniform(-sqrt(1 - rand_x**2), sqrt(1 - rand_x**2))
    rand_z = sqrt(1 - (rand_x**2 + rand_y**2)) * random.choice([-1, 1])
    return [radius * rand_x, radius * rand_y, radius * rand_z]

def get_point_string(point):
    x, y, z = point.get_center()
    return f"({x:.2f}, {y:.2f}, {z:.2f})"

def axis_angle_from_rotation_component(component):
    axis_of_rotation = RIGHT
    rotation_angle = 0
    if component == SIGMA:
        axis_of_rotation = RIGHT
        rotation_angle = acos(1/3)
    elif component == SIGMA_I:
        axis_of_rotation = RIGHT
        rotation_angle = -acos(1/3)
    elif component == TAU:
        axis_of_rotation = UP
        rotation_angle = acos(1/3)
    elif component == TAU_I:
        axis_of_rotation = UP
        rotation_angle = -acos(1/3)
    return axis_of_rotation, rotation_angle

rotation_translation_dict = {
    SIGMA: r"\sigma",
    SIGMA_I: r"\sigma^{-1}",
    TAU: r"\tau",
    TAU_I: r"\tau^{-1}", 
}


def generate_random_rotations_with_labels(n):
    rotations = []
    for i in range (n):
        rotation_components = []
        rotation_label = ""
        number_of_components = random.randint(2, 7)
        for i in range(number_of_components): # generate components
            rotation = random.randint(0,3)
            if i >= 1:
                last_rotation = rotation_components[-1]
                # keep generating a new rotation component until it doesn't reduce the rotation
                while (
                    (rotation == SIGMA and last_rotation == SIGMA_I)
                    or (rotation == SIGMA_I and last_rotation == SIGMA)
                    or (rotation == TAU and last_rotation == TAU_I)
                    or (rotation == TAU_I and last_rotation == TAU)
                ):
                    rotation = random.randint(0,3)
            rotation_components.append(rotation)
            rotation_label += rotation_translation_dict[rotation]
        rotations.append((rotation_components, rotation_label))
    return rotations

# sigma along x-axis
# tau along y-axis

def generate_rotation_arrow(start_point, sphere_radius, rotation_comp, color=BLACK, eps=0):
    start_point_location = start_point.get_center()
    start = 0
    end = 0
    if rotation_comp in (SIGMA, TAU):
        end = np.cos(1/3)
    elif rotation_comp in (SIGMA_I, TAU_I):
        start = -np.cos(1/3)

    sigma_lambda = lambda t: start_point_location + sphere_radius * np.array([0, np.cos(t), np.sin(t)])
    tau_lambda = lambda t: start_point_location + sphere_radius * np.array([np.cos(t), 0, np.sin(t)])

    result = VGroup()

    # create arrow curve
    if rotation_comp in (SIGMA, SIGMA_I):
        arrow_curve = ParametricFunction(
            sigma_lambda, color=color, t_range=[start, end],
        ).set_shade_in_3d(True)
        arrow_curve.stroke_width = 5
        result.add(arrow_curve)
    elif rotation_comp in (TAU, TAU_I):
        arrow_curve = ParametricFunction(
            tau_lambda, color=color, t_range=[start, end],
        ).set_shade_in_3d(True)
        arrow_curve.stroke_width = 5
        result.add(arrow_curve)

    # create arrow cone
    sigma_direction_lambda = lambda t: np.array([0, -np.sin(t), np.cos(t)])
    tau_direction_lambda = lambda t: np.array([-np.sin(t), 0, np.cos(t)])
    direction = np.array([0,0,0])
    end_point = np.array([0,0,0])
    if rotation_comp == SIGMA:
        direction = sigma_direction_lambda(np.cos(1/3))
        end_point = start_point_location + sigma_lambda(np.cos(1/3) + eps)
    elif rotation_comp == SIGMA_I:
        direction = sigma_direction_lambda(-np.cos(1/3))
        end_point = start_point_location + sigma_lambda(-np.cos(1/3) + eps)
    elif rotation_comp == TAU:
        direction = tau_direction_lambda(np.cos(1/3))
        end_point = start_point_location + tau_lambda(np.cos(1/3) + eps)
    elif rotation_comp == TAU_I:
        direction = tau_direction_lambda(-np.cos(1/3))
        end_point = start_point_location + tau_lambda(-np.cos(1/3) + eps)
    arrow_cone = Cone(show_base=True, base_radius=0.15, height=0.5, direction=direction).shift(end_point).set_color(color)
    result.add(arrow_cone)

    return result


class ActualDecomp(VoiceoverScene):
    def construct(self):
        s = "What we've seen in the previous scene can be expressed symbolically as follows"
        scene_title = Tex("The decomposition (symbolically)", font_size=70).to_edge(UP)
        self.add(scene_title)
        decomp_1_tex = MathTex(r"S^2 \setminus D = M \cup W(\sigma) M \cup W(\sigma^{-1}) M \cup W(\tau) M \cup W(\tau^{-1}) M").next_to(scene_title, DOWN).shift(DOWN)
        self.play(Create(decomp_1_tex))
        self.wait(0.5)
        s = "Notice now how similar this is to the decomposition of the free group that we did. In fact we can decompose in the exact same way"
        decomp_2_tex = Tex(r"The paradoxical decomposition of $S^2 \setminus D$ is then:").next_to(decomp_1_tex, DOWN).shift(DOWN)
        decomp_3_tex = MathTex(r"S^2 \setminus D &= \sigma^{-1} W(\sigma) M \cup W(\sigma^{-1}) M \\ &= \tau^{-1} W(\tau) M \cup W(\tau^{-1}) M").next_to(decomp_2_tex, DOWN)
        self.play(Write(decomp_2_tex))
        self.play(Write(decomp_3_tex))
        
        self.wait(2)

class ArrowTest(ThreeDScene):
    def construct(self):
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=.75, run_time=1.5)
        self.begin_ambient_camera_rotation()
        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex(r"x"))
        y_label = axes.get_y_axis_label(Tex(r"y")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex(r"z")).shift(OUT*.25)

        self.play(FadeIn(axes), FadeIn(x_label, y_label, z_label))
        self.wait(.5)

        sphere_radius = 3
        sphere = Sphere(radius=sphere_radius, fill_opacity=.35).set_color(BLUE)

        dot = Dot3D(np.array([3, 0, 0]))
        arrow = generate_rotation_arrow(dot, sphere_radius, SIGMA)
        self.play(Write(sphere))
        self.play(FadeIn(arrow))
        self.wait(1)

if __name__ == "__main__":
    get_random_point_on_sphere(3)


class MatchingEquationParts(Scene):
    def construct(self):

        point_tex = Tex(r"Equivalence class of {{$(0, 0, 0)$}}")
        point_tex_end = Tex(r"Equivalence class of {{$(1, 1, 1)$}}")
        replacement = MathTex(r"(1, 1, 1)")

        eq1 = MathTex("{{x}}^2", "+", "{{y}}^2", "=", "{{z}}^2")
        eq2 = MathTex("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2")
        eq3 = MathTex("{{a}}^2", "=", "{{c}}^2", "-", "{{b}}^2")

        # self.add(eq1)
        self.wait(0.5)
        self.play(TransformMatchingTex(point_tex, point_tex_end))
        self.wait(0.5)
        # self.play(TransformMatchingTex(eq2, eq3))
        # self.wait(0.5)