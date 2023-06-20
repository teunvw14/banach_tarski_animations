from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
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

def dot_radial_line(dot, color):
    result = Line3D(ORIGIN, dot.get_center(), color=color)
    result.add_updater(lambda x: x.set_start_and_end_attrs(ORIGIN, dot))
    return result

class CreatingMIntro(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        
        title = Title(r"Creating a paradoxical decomposition of $S^2 \setminus D$")
        self.play(Write(title))
        
        s2_decomp_tex = MathTex(r"\tau^{-1}{{W(\tau)}} {{M}} \cup {{W(\tau^{-1})}} {{M}} = S^2 \setminus D = \sigma^{-1}{{W(\sigma)}} {{M}} \cup {{W(\sigma^{-1})}} {{M}}").shift(UP)
        s = "Let's look at that paradoxical decomposition again. "
        with self.voiceover(s):
            self.play(FadeIn(s2_decomp_tex))
        
        s = "We want to take the sphere apart in the same way we did to the free group. To do so, we will need to apply the rotations to the points on the sphere. But applying a rotation to the whole sphere, just gives the whole sphere."

        with self.voiceover(s):
            pass

        s = "So, we will need to choose a subset M of the sphere, such that every rotation of that set is unique. Actually, this set M and all its rotation will be non-measurable - that is why we talked about non-measurable sets before."
        with self.voiceover(s):
            self.play(
                s2_decomp_tex.animate.set_color_by_tex("M", BLUE)
            )

        m_explanation_tex = Tex(r"M is what we get when we `divide' $S^2$ by $G(\sigma, \tau)$").shift(DOWN)
        box = SurroundingRectangle(m_explanation_tex, color=YELLOW, buff=MED_LARGE_BUFF)
        s  = "We will do this by dividing the sphere based on the group of rotations. We will see how exactly we do that right now."
        with self.voiceover(s):
            self.play(FadeIn(m_explanation_tex, box))


class CreatingM(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=.75, run_time=1.5)
        title = Title(r"Creating $M$ using $ G(\sigma, \tau)$")
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex(r"x"))
        y_label = axes.get_y_axis_label(Tex(r"y")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex(r"z")).shift(OUT*.25)

        s = "Let's see how we can create the set M by dividing the sphere by the group of rotations. We will make points equivalent whenever they can be transformed into each other using rotations from G(sigma, tau)"
        with self.voiceover(s): 
            self.play(FadeIn(axes), FadeIn(x_label, y_label, z_label))
        self.wait(.5)

        sphere_radius = 3
        sphere = Sphere(radius=sphere_radius, fill_opacity=.35).set_color(BLUE)

        s = "Similarly to the construction of the non-measurable set, we will look at equivalence classes over rotations. The only differences are that we are now looking at three-dimensional rotations instead of two, and that we are not looking at rational rotations, but at rotations from the group generated by sigma and tau."
        with self.voiceover(s):
            pass

        self.play(Write(sphere), FadeOut(title))

        s = "Let's once again look at how the equivalence classes are formed; we apply rotations from G(sigma, tau) to it. Each color here represents a unique equivalence class. Of course, as was the case with the non-measurable set and the tree of the free group, this is an infinite process of which we can only show a finite part. This is because, to get the equivalence class of any particular point, we would need to apply ALL rotations from the group G(tau, sigma) to it; hopefully these finite examples do illustrate how that would be done. The lines from the origin to the points are there to make it easier to see how the points are rotating."
        with self.voiceover(s):
                
            # show creating equivalence classes for four different points
            for i, color in enumerate((RED, BLUE, GREEN, YELLOW)):
                random_sphere_coordinates = get_random_point_on_sphere(sphere_radius)
                origin_dot = Dot3D(random_sphere_coordinates, color=color, radius=.1)
                origin_line = dot_radial_line(origin_dot, color)
                point_string = get_point_string(origin_dot)
                point_tex = Tex(r"Equivalence class of {{$" + point_string + r"$}}").to_edge(UP).set_color_by_tex(point_string, color)
                rotation_tex_old = Tex(r"Applying rotation: {{$e$}}").to_edge(DOWN)
                self.add_fixed_in_frame_mobjects(point_tex)
                self.add_fixed_in_frame_mobjects(rotation_tex_old)
                self.play(FadeIn(origin_dot, origin_line), Write(point_tex))
                for rotation, label in generate_random_rotations_with_labels(3):
                    rotation_dot = origin_dot.copy()
                    rotation_dot_line = dot_radial_line(rotation_dot, color)

                    # rotation_arrows = VGroup()

                    rotation_tex_new = Tex(r"Rotation is: {{$" + label + r"$}}").to_edge(DOWN)
                    self.add_fixed_in_frame_mobjects(rotation_tex_new)
                    # set up animation
                    self.play(TransformMatchingTex(rotation_tex_old, rotation_tex_new), run_time = .5)
                    self.wait(.15)
                    # animate all the components of the rotation:
                    for component in rotation:
                        axis_of_rotation, rotation_angle = axis_angle_from_rotation_component(component)
                        # component_arrow = generate_rotation_arrow(rotation_dot, sphere_radius, component)
                        # rotation_arrows.add(component_arrow)
                        dot_line_group = VGroup(rotation_dot, rotation_dot_line)
                        self.play(
                            Rotate(dot_line_group, rotation_angle, about_point=ORIGIN, axis=axis_of_rotation),
                            # Rotate(rotation_dot_line, rotation_angle, about_point=ORIGIN, axis=axis_of_rotation), 
                            # FadeIn(component_arrow),
                            run_time=1
                        )
                    self.remove(rotation_tex_old)
                    # self.play(FadeOut(rotation_arrows))
                    rotation_tex_old = rotation_tex_new
                self.play(Unwrite(point_tex, rotation_tex_old, rotation_tex_new))
                self.remove(rotation_tex_new)

        # Overview:
        # Goal: show paradoxical decomposition of S^2 - D
        # - show ball, creating M by choosing random point on ball and rotating them by 
        #   arbitrary rotations
        # - Show (non-disjoint) "almost" paradoxical decomp
        # - Explain why not disjoint;
        #   - (give example)
        #   - "overlap is caused by fixed points. It can be shown that it's caused
        #     only by these points (refer to thesis)"
        #   - show altered decomposition
        self.wait(2)

class CreatingMConclusion(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        title = Title("Finishing the construction of $M$")
        self.add(title)

        s = "Now that we've seen how we can create equivalence classes over the group of rotations G(sigma, tau), we can create the set $M$ identically to how we did it before."
        with self.voiceover(s):
            pass

        s = "We look at all the equivalence classes."
        classes_note = Tex("Equivalence classes").shift(UP)
        classes_tex = MathTex(r"\{[{{(0, 0, 1)}}], [{{(0, \frac{\sqrt{2} }{2}, \frac{\sqrt{2} }{2})}}], [{{(-\frac{\sqrt{3} }{3}, -\frac{\sqrt{3} }{3}, \frac{\sqrt{3} }{3})}}], \dots\}").next_to(classes_note, DOWN)
        with self.voiceover(s):
            self.play(
                FadeIn(classes_tex, classes_note)
            )
        
        M_tex_start = MathTex(r"M = \{").next_to(classes_tex, DOWN).shift(5*LEFT + DOWN)
        M_group = VGroup(M_tex_start)
        s = "Now, again by the Axiom of Choice, we can pick exactly one point from each of the equivalence classes to form our set M."
        with self.voiceover(text=s):
            self.play(
                Write(M_tex_start)
            )
            for i, point in enumerate((
                classes_tex.submobjects[1],
                classes_tex.submobjects[3],
                classes_tex.submobjects[5])):
                new_point = point.copy()
                if i > 0:
                    self.play(
                        new_point.animate.next_to(M_group[2*i], RIGHT).shift(UP*.15)
                    )
                else:
                    self.play(
                        new_point.animate.next_to(M_group[2*i], RIGHT)
                    )
                comma = MathTex(r",").next_to(new_point, RIGHT).shift(DOWN * 0.15)
                self.play(
                    Write(comma), run_time = .1
                )
                M_group.add(new_point, comma)

            M_tex_end = MathTex(r"\ \dots\}").next_to(M_group[-1], RIGHT).shift(UP * .15)
            M_group.add(M_tex_end)
            self.play(Write(M_tex_end))


        M_property_explanation = Tex("$M$ has the desired properties")
        s2_decomp_again = MathTex(r"\tau^{-1}{{W(\tau)}} {{M}} \cup {{W(\tau^{-1})}} {{M}} = S^2 \setminus D = \sigma^{-1}{{W(\sigma)}} {{M}} \cup {{W(\sigma^{-1})}} {{M}}").next_to(M_property_explanation, DOWN)
        s = "Now, two different rotations applied to M have no overlap, and similarly to before, applying all of the rotations from G(sigma, tau) gives the whole sphere. This results in the paradoxical decomposition of S2 minus D that we saw."
        with self.voiceover(s):
            self.play(
                FadeOut(M_group, classes_note, classes_tex),
                FadeIn(M_property_explanation, s2_decomp_again)
            )
