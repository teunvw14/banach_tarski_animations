from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

config.background_color = rgb_to_color([28/255, 35/255, 31/255])


class Conclusion(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))
        title = Title("Conclusion")
        self.add(title)

        end_tex = Tex("Thank you for watching this video!")

        s = "So, we have now come to the end of this video. Hopefully you now have a decent grasp of the Banach-Tarski paradox."
        with self.voiceover(s):
            self.play(FadeIn(end_tex))

        summary_tex = Tex(r"\begin{itemize}\item Non-measurable set \item Paradoxical decomposition of $F_2$ \item Transfer to $S^2 \setminus D$ \item Added D back \item Finally: paradoxical decomposition of $B^3$\end{itemize}").shift(DOWN)
        summary_word = Tex("Summary").next_to(summary_tex, UP)


        s = "To shortly summarize what we have seen in the past chapters: we saw a construction of a 'non-measurable set'; explored the concept of 'paradoxical decompositions'; dove into 'the free group $F_2$' and saw its paradoxical decomposition. "
        with self.voiceover(s):
            self.play(FadeOut(end_tex), Write(summary_word))
            self.play(Write(summary_tex))
        s = "We then proved the 'Banach-Tarski paradox': we passed on the paradoxical decomposition from the free group to the sphere $S^2$ - except a countable set of fixed points $D$. "
        with self.voiceover(s):
            pass
        s= "Then we found a way to add that set $D$ back into the paradoxical decomposition, after which we found a way to expand the decomposition from the sphere to the ball."
        with self.voiceover(s):
            pass
        s= " We finally added the origin to the decomposition to finish the paradoxical decomposition of the unit ball $B^3$. "
        with self.voiceover(s):
            pass

        interestedinmore = Tex(r"Interested in more details, or the general result?\\ Read the full thesis!")
        s = "It is also possible to generalize this result, which is shown in the thesis. "
        with self.voiceover(s):
            self.play(
                FadeOut(summary_tex, summary_word),
                Write(interestedinmore)
            )
        s = "This general result shows that you can transform any bounded set with interior points into any other such set with finite Euclidean transformations. "
        with self.voiceover(s):
            pass
        
        s = "If that sounds interesting, make sure to read the thesis."
        with self.voiceover(s):
            pass