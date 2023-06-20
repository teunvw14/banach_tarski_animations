# Show reconstructing the whole sphere from M
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

class SphereFromM(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=.75, run_time=1.5)
        title = Tex(r"Creating M for reasons. (Paradoxical decomposition of $S^2 \setminus D$)").to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex(r"x"))
        y_label = axes.get_y_axis_label(Tex(r"y")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex(r"z")).shift(OUT*.25)

        self.play(FadeIn(axes), FadeIn(x_label, y_label, z_label))
        self.wait(.5)

        sphere_radius = 3
        sphere = Sphere(radius=sphere_radius, fill_opacity=.35).set_color(BLUE)
        self.begin_ambient_camera_rotation(rate=0.15)

        self.play(Write(sphere), FadeOut(title))

        s = "We will now define a set M that contains exactly one point from each equivalent class. This will look something like this."
        dots = VGroup()
        colors = random.sample(list(Colors.__members__.values()), 20) 
        for color in colors:
            random_coordinates = get_random_point_on_sphere(sphere_radius)
            dot = Dot3D(random_coordinates, color=color.value, radius=0.04)
            dots.add(dot)
        self.play(ShowIncreasingSubsets(dots), run_time=3)
        s = "Then of course, we can cover the whole of S2 by taking all rotations in G(tau, sigma) and applying them to M."
        # rotated_point_groups = []
        for rotation, label in generate_random_rotations_with_labels(3):
            rotation_tex = Tex(f"Rotating tex by ${label}$").to_edge(DOWN)
            new_point_group = dots.copy()
            self.add_fixed_in_frame_mobjects(rotation_tex)
            for component in rotation:
                axis_of_rotation, rotation_angle = axis_angle_from_rotation_component(component)
                self.play(Rotate(new_point_group, rotation_angle, about_point=ORIGIN, axis=axis_of_rotation), run_time=1)
            self.remove(rotation_tex)
        s = "Of course, we can't possibly show all these rotations of M, but hopefully it is clear how S2 can be covered by taking the union of all these rotations of M."
        s = "This is because, for every element of S2, there is some equivalent point in M. So if we rotate by all possible rotations in G tau sigma, then we will be sure to cover it eventually"
        self.wait(2)