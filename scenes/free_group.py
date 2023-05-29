from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from math import sqrt, pi, e, log

config.background_color = rgb_to_color([28/255, 35/255, 31/255])

class FreeGroupScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        title_card_tex = Tex(r"The free group $F_2$", font_size = 60)
        
        s = "One of the essential constructions in the proof of the Banach-Tarski paradox is the use of the free group to “duplicate” the ball. We will see that the free group generated by two elements can be easily divided into parts, such that they can be shifted to create two copies of itself. This is in essence what we wil eventually be doing with the unit sphere. So what is it?"

        with self.voiceover(s):
            self.play(Write(title_card_tex))

        s = "Let's look at a definition. The free group f two generated by two elements sigma and tau is the group consisting of all finite products of sigma, tau and their inverses. The identity in this group is the empty product."
        f2_definition_tex = Tex(r"\textbf{Definition (Free Group $F_2$)}. The free group $F_2$ generated by two elements $\sigma, \tau$ is the group consisting of all finite products of $\sigma, \tau$ and their inverses $\sigma^{-1}, \tau^{-1}$. The identity in this group is the empty product (denoted $e$).").scale(.75)

        with self.voiceover(s):
            self.play(
                title_card_tex.animate.to_edge(UP)
            )
            self.play(FadeIn(f2_definition_tex))

        s = "These are some examples of elements."
        example_elements_tex = Tex(r"Ex.: $\sigma\tau$, $\tau^2\sigma^{-1}$, $\sigma\tau\sigma\tau^{-2}\sigma$, etc.").next_to(f2_definition_tex, DOWN).shift(DOWN * .75)

        with self.voiceover(s):
            self.play(
                Write(example_elements_tex)
            )


        root = MathTex(r"e")
        leaves_1 = []
        branches_1 = []
        for i, label in enumerate((r"\sigma", r"\tau", r"\sigma^{-1}", r"\tau^{-1}")):
            leaf = MathTex(label).shift(1.5*DOWN + i * RIGHT*2 - 3 * RIGHT)
            leaf_branch = Arrow(start = root, end = leaf)
            # leaf_branch_label = MathTex(label).next_to(leaf_branch, LEFT)#.shift(LEFT * .5)
            leaves_1.append(leaf)
            branches_1.append(leaf_branch)

        tree = VGroup(root, *leaves_1, *branches_1).to_edge(UP)

        leaves_2 = []
        branches_2 = []
        for i, label in enumerate((r"\sigma^2", r"\sigma\tau", r"\sigma\tau^{-1}")):
            leaf = MathTex(label).shift(i * RIGHT*2 - 3 * RIGHT)
            leaf_branch = Arrow(start = leaves_1[0], end = leaf)
            # leaf_branch_label = MathTex(label).next_to(leaf_branch, LEFT)#.shift(LEFT * .5)
            leaves_2.append(leaf)
            branches_2.append(leaf_branch)
        tree.add(*leaves_2, *branches_2)
        
        leaves_3 = []
        branches_3 = []
        for i, label in enumerate(
                (r"\sigma\tau\sigma", r"\sigma\tau^2", r"\sigma\tau\sigma^{-1}")
            ):
            leaf = MathTex(label).shift(2 * DOWN + i * RIGHT*2 - 3 * RIGHT)
            leaf_branch = Arrow(start = leaves_2[1], end = leaf)
            # leaf_branch_label = MathTex(label).next_to(leaf_branch, LEFT)#.shift(LEFT * .5)
            leaves_3.append(leaf)
            branches_3.append(leaf_branch)
        tree.add(*leaves_3, *branches_3)
        
        
        tree_text = Tex(r"$F_2$ as a tree").to_corner(UP + LEFT)

        s = "One way to look at this group is to consider it as a directed tree. At the root of the tree, we have the identity element e. We can then go further down the tree by multiplying with sigma, sigma inverse, tau or tau inverse."
        with self.voiceover(s):
            self.play(
                    FadeOut(title_card_tex, f2_definition_tex, example_elements_tex),
                    Create(tree),
                    FadeIn(tree_text),
                    run_time = 2.5           
                )
            
        s = "Each step down the tree is a multiplication by some element of F2. Note that we only looked at the progression of the tree for words starting with sigma, then starting with sigma tau. You should imagine the tree continuing infinitely for all the other branches as well. "

        sigma_tree = VGroup(leaves_1[0], *leaves_2, *leaves_3, *branches_2, *branches_3) 
        sigma_tree_leaves = VGroup(leaves_1[0], *leaves_2, *leaves_3)
        self.play(
            LaggedStartMap(Indicate, sigma_tree_leaves, run_time = 2)
        )

        s = "Now notice the following: if we multiply the branch that begins with sigma, that is "

        self.wait(2)