# Show how decomp of S^2 \ D can be made into one of S^2 using E

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

from math import sqrt

GOLDEN_RATIO = (1/2 + sqrt(5)/2)

config.background_color = rgb_to_color([28/255, 35/255, 31/255])

def get_random_point_on_sphere(radius):
    rand_x = random.uniform(-1, 1)
    rand_y = random.uniform(-sqrt(1 - rand_x**2), sqrt(1 - rand_x**2))
    rand_z = sqrt(1 - (rand_x**2 + rand_y**2)) * random.choice([-1, 1])
    return [radius * rand_x, radius * rand_y, radius * rand_z]

points_of_D_coordinates = [
    [1.705653589119117, -0.8576977742843473, 2.3141089779681403],
    [0.9283384411680031, -2.097001251668247, -1.9341079311019767],
    [-1.1434703478071881, 0.47170339618990065, 2.733124854394439],
    [-1.370287035516874, 0.3107835017307966, 2.6506088084337005],
    [2.005681072368484, 0.1257956769516082, 2.2274242711264267],
    [0.4857349665773061, 0.9075533386404354, -2.8178730418112776],
    [2.7715304818209487, -0.0906080364568918, -1.1447309605609381],
    [1.1061345705914623, -0.592104294838423, -2.725046571304119],
    [2.569263400349941, -0.3128280601590953, -1.516912714825529],
    [1.1340220797792513, -0.8198574530133578, -2.653644226212623]
]

class AddE(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        s = "Luckily we can classify exactly which points are causing this problem. These are precisely those points that are fixed by some rotation, like the one we just saw. This is the set D. A proof for this fact is not shown here; interested viewers are referred to the thesis that this video is based on."

        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=.75, run_time=1.5)
        title = Title(r"Adding $D$ into the paradoxical decomposition of $S^2 \setminus D$")
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex(r"x"))
        y_label = axes.get_y_axis_label(Tex(r"y")).shift(UP * 1.8)
        z_label = axes.get_z_axis_label(Tex(r"z")).shift(OUT*.25)

        self.wait(.5)

        sphere_radius = 3
        sphere = Sphere(radius=sphere_radius, fill_opacity=.35).set_color(BLUE)

        s = "We are now ready to dive into the next step of the proof of the Banach-Tarski paradox, which will be to add the set D back to the decomposition."
        with self.voiceover(s):
            self.play(FadeIn(axes), FadeIn(x_label, y_label, z_label), Write(sphere))

        points_of_D = VGroup()
        for coordinates in points_of_D_coordinates:
            p = Dot3D(coordinates, color=WHITE)
            points_of_D.add(p)
            
        s = "Let's see the points of D. D has infinitely many points, so we show a finite subset of D to represent all of D."
        with self.voiceover(s):
            self.play(FadeIn(points_of_D))
        s = "Let's look at these points from above, so we can better see what we are doing."
        with self.voiceover(s):
            self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=.75, run_time=1.5)
        
        
        

class ConstructingE(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        ax = Axes()
        self.add(ax)

        circle_radius = 2.5
        circle = Circle(color=BLUE, fill_opacity=0.35, radius=circle_radius)
        self.add(circle)

        points_of_D_twod = VGroup()
        for coordinates in points_of_D_coordinates:
            coordinates_2d = np.array([coordinates[0], coordinates[1], 0]) * circle_radius/3
            p = Dot(coordinates_2d, color=WHITE, radius=0.04)
            points_of_D_twod.add(p)

        self.add(points_of_D_twod)

        phi_no_overlap = Tex(r"We have $\varphi$ such that $\varphi^n(D) \cap D = \emptyset\ \forall n$").to_edge(DOWN)

        s = "We know that there exists a rotation phi such that applying it to D repeatedly always gives unique points. For a proof, refer to the thesis. "
        with self.voiceover(s):    
            self.play(FadeIn(phi_no_overlap))

        origin_dot = Dot(color=BLACK, radius = 0.02 )
        s = "Let's remove the axes to keep things tidy. We will add a small black dot in the center to keep track of the origin."
        with self.voiceover(s):
            self.play(FadeOut(ax), FadeIn(origin_dot))

        rotation_counter = MathTex(r"{{ D }}").set_color(RED).to_edge(LEFT).shift(RIGHT)
        s = "We will be using this rotation phi to fix the gap of D. You're now seeing these rotations of phi being generated."
        initial_number_of_d_rotations = 16
        D_dupes_groups = VGroup()
        with self.voiceover(s):
            self.play(points_of_D_twod.animate.set_color(RED))
            self.play(Create(rotation_counter))
            for i in range(1, initial_number_of_d_rotations + 1):
                rotation_counter_new = MathTex(r"\varphi^{" + f"{i}" + r"}({{ D }})").set_color_by_tex("D", RED).shift(rotation_counter.get_center())
                dupe_group = points_of_D_twod.copy().set_color(WHITE)
                self.play(
                    *[Rotate(p, angle=GOLDEN_RATIO*i, axis=OUT, about_point=ORIGIN)for p in dupe_group],
                    Transform(rotation_counter, rotation_counter_new),
                    run_time = 0.75
                )
                self.wait(.2)
                self.remove(rotation_counter)
                rotation_counter = rotation_counter_new
                D_dupes_groups.add(dupe_group)
        
        e_definition = MathTex(r"E = \bigcup_{n=0}^\infty \varphi^n(D)").to_corner(UP+RIGHT)
        total_number_of_d_rotations = 100
        s = "We will define the set E as the union of D with all these repeated rotations phi n of D. Again, we can't show the infinite number of rotations of D, so we will just show a lot of them - also because it is quite mesmerizing to look at."
        with self.voiceover(s):
            self.play(FadeOut(phi_no_overlap))
            self.play(Write(e_definition))
            for i in range(initial_number_of_d_rotations, total_number_of_d_rotations + 1):
                rotation_counter_new = MathTex(r"\varphi^{" + f"{i}" + r"}({{ D }})").set_color_by_tex("D", RED).shift(rotation_counter.get_center())
                dupe_group = points_of_D_twod.copy().set_color(WHITE)
                self.play(
                    *[Rotate(p, angle=GOLDEN_RATIO*i, axis=OUT, about_point=ORIGIN)for p in dupe_group],
                    Transform(rotation_counter, rotation_counter_new),
                    run_time = 0.1
                )
                self.wait(.2)
                self.remove(rotation_counter)
                rotation_counter = rotation_counter_new
                D_dupes_groups.add(dupe_group)
        
        e_rotated = MathTex(r"\varphi^{-1}(E \setminus D) = \varphi^{-1}(\bigcup_{n=1}^\infty \varphi^n(D)) = \bigcup_{n=0}^\infty \varphi^n(D) = E").to_edge(DOWN).shift(DOWN * 0.25)
        D_dupes_groups_blue = D_dupes_groups.copy().set_color(YELLOW)

        s = "Alright, let's continue with the proof."
        with self.voiceover(s):
            pass

        s = "Notice now that we can play a smart trick: if we rotate this newly defined set E, minus the set D by phi inverse, we get all of E again. We can represent this visually as follows."
        with self.voiceover(s):
            self.play(Write(e_rotated))

        s = "We take a yellow copy of all these rotations of D, that is, E minus D, and rotate it to see where all these points end up."
        with self.voiceover(s):
            self.play(FadeIn(D_dupes_groups_blue))
            
        s = " What you see is that all of E gets covered."
        with self.voiceover(s):
            self.play(Rotate(D_dupes_groups_blue, angle=-GOLDEN_RATIO, axis=OUT, about_point=ORIGIN), run_time = 5)
            self.play(FadeOut(points_of_D_twod))


        last_rotation_of_D = points_of_D_twod.copy().set_color(WHITE).rotate(angle=GOLDEN_RATIO*total_number_of_d_rotations, axis=OUT, about_point=ORIGIN)
        s = "Well, all of E except the last rotation of D. But this is only the case because we are showing finitely many rotations of D."
        with self.voiceover(s):
            for _ in range(3):
                self.play(
                    Indicate(last_rotation_of_D, color = PINK)
                ) 

        infinite_demonstration_parts = VGroup(
            MathTex("D"), MathTex(r"\varphi(D)"), *[MathTex(r"\varphi^" + f"{i}(D)") for i in range(1, 3)]
        )
        infinite_demonstration = VGroup()
        for obj in infinite_demonstration_parts:
            infinite_demonstration.add(obj)
            infinite_demonstration.add(Arrow(start=UP, end=DOWN).scale(0.5))
        infinite_demonstration.add(MathTex(r"\vdots"))
        infinite_demonstration.arrange(UP)
        for obj in infinite_demonstration:
            if type(obj) == Arrow:
                infinite_demonstration.add(MathTex(r"\varphi^{-1}").next_to(obj, RIGHT).shift(UP*0.1))
        infinite_demonstration.to_edge(LEFT)

        s = "In the infinite case, this doesn't happen, because for every rotation of D, where phi is applied n times to D, the copy of D rotated by phi n+1 times will cover it up. This is shown schematically on the left of the screen."
        with self.voiceover(s):
            self.play(FadeOut(e_rotated))
            self.play(FadeIn(infinite_demonstration))

        s = "Let's now see how we can use this to create a paradoxical decomposition of the whole sphere."

        self.wait(2)

class EConclusionScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        title = Title(r"Coming to a paradoxical decomposition of $S^2$")
        self.add(title)

        thing_1 = MathTex(r"(1)\ S^2 \setminus E = (S^2 \setminus D) \cap (S^2 \setminus E)").shift(UP*2)
        thing_2 = MathTex(r"(2)\ E = \varphi^{-1}(E \setminus D) = \varphi^{-1}((S^2 \setminus D) \cap E)").next_to(thing_1, DOWN)

        s = "Note the following to things about E first. The first follows from the fact that D is a subset of E, and the second is derived from the fact that E is contained in S2. Feel free to pause the video here to check for yourself."
        with self.voiceover(s):
            self.play(Write(thing_1), Write(thing_2))

        s2_partition = MathTex(r"S^2 = (S^2 \setminus E) \cup E")
        s = "Now, since we can partition S2 as follows"
        with self.voiceover(s):
            self.play(Write(s2_partition))

        final_eq = MathTex(r"S^2 = \Big((S^2 \setminus D) \cap (S^2 \setminus E) \Big)\cup \varphi^{-1}\Big((S^2 \setminus D) \cap E\Big)").shift(2*DOWN)
        box = SurroundingRectangle(final_eq, color=YELLOW)
        final_eq_toelichting = Tex(r"Combining these gives:").next_to(final_eq, UP)
        s = "we can combine all of these to get THIS equation."
        with self.voiceover(s):
            self.play(Write(final_eq), FadeIn(final_eq_toelichting, box))

        self.wait(4)

        s2d_decomp = MathTex(r"S^2 \setminus D &= \sigma^{-1}{{W(\sigma)}}M \cup {{W(\sigma^{-1})}}M \\ &= \tau^{-1}{{W(\tau)}}M \cup {{W(\tau^{-1})}}M").shift(DOWN*2)

        s = "Now remember our paradoxical decomposition of S2 minus D"
        with self.voiceover(s):
            self.play(
                FadeOut(thing_1, thing_2, s2_partition, final_eq_toelichting, box),
                final_eq.animate.to_edge(UP).shift(DOWN*2)
            )
            self.wait(1)
            self.play(Write(s2d_decomp))


        s = "We can then finally get a paradoxical decomposition of S2 by first substituting the expression with sigma for S2 minus D, and then the expression with tau. It is quite tedious to work out, so we won't show it exactly here."
        with self.voiceover(s):
            pass

        full_decomp = MathTex(r"S^2 &= \tau^{-1}T_1 \cup T_2 \cup \varphi^{-1}\tau^{-1}T_3 \cup \varphi^{-1}T_4 \\ &= \sigma^{-1}\Sigma_1 \cup \Sigma_2 \cup \varphi^{-1}\sigma^{-1}\Sigma_3 \cup \varphi^{-1}\Sigma_4")

        s = "The result however is this: a paradoxical decomposition of S2. If we wanted to write the decomposition in full, it would unfortunately not fit on the screen, which is why there are some new terms used here. These terms are defined precisely in the thesis. "
        with self.voiceover(s):
            self.play(
                Write(full_decomp),
                FadeOut(s2d_decomp, final_eq)
            )
        


        self.wait(2)