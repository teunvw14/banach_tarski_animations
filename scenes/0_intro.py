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

class Intro(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(silence_threshold=-40.0))

        s = "Welcome to this video about the Banach-Tarski paradox. My name is Teun van Wezel, and this video was made as part of my bachelor's thesis in mathematics at Utrecht University."
        
        opening_tex = Tex(r"The Banach-Tarski Paradox: \\An Animated Proof", font_size = 80).shift(UP)
        subtitle = Tex(r"By Teun van Wezel \\ Bachelor Thesis Mathematics").next_to(opening_tex, DOWN).shift(DOWN)
        subsubtitle = Tex("(Utrecht University, advised by Karma Dajani)").next_to(subtitle, DOWN)
        with self.voiceover(s):
            self.play(Write(opening_tex), Write(subtitle), Write(subsubtitle))
            
        s = "The goal of this video is to provide a visual proof that follows the same lines as my thesis, so that as many people as possible can get a grasp of how exactly one ball can be turned into two."
        with self.voiceover(s):
            pass
        s = "Because that is what the Banach-Tarski paradox says: you can take parts of the unit ball, rotate and translate those parts, without stretching or scaling anything and get two copies of the unit ball."
        with self.voiceover(s):
            pass
        s = "A fascinating result indeed, which we will get to proving very shortly. Before we do that, we will make a short stop in  the world of non-measurable sets. This is because without non-measurable sets the Banach-Tarski paradox would not be possible at all."
        with self.voiceover(s):
            pass
        
        s = "Okay, let's get into it."
        with self.voiceover(s):
            pass

        
