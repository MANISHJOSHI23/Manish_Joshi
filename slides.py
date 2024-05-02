from manim import *  # or: from manimlib import *

from manim_slides import Slide

def Item(*str,dot = True,font_size = 35,math=False,pw="8cm",color=WHITE):
    if math:
        tex = MathTex(*str,font_size=font_size,color=color)
    else:
        tex = Tex(*str,font_size=font_size,color=color,tex_environment=f"{{minipage}}{{{pw}}}")
    if dot:
        dot = MathTex("\\cdot").scale(2)
        dot.next_to(tex[0][0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    else:
        dot = MathTex("\\cdot",color=BLACK).scale(2)
        dot.next_to(tex[0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    g2 = VGroup()
    for item in tex:
        g2.add(item)

    return(g2)


def ItemList(*item,buff=MED_SMALL_BUFF):
    list = VGroup(*item).arrange(DOWN, aligned_edge=LEFT,buff=buff)
    return(list)

def Ray(start,end,ext:float=0,eext:float = 0,pos:float=0.5,color=BLUE):
    dir_lin = Line(start=start,end=end)
    dir = dir_lin.get_length()*ext*dir_lin.get_unit_vector()
    edir = dir_lin.get_length()*eext*dir_lin.get_unit_vector()
    lin = Line(start=start-edir,end=end+dir,color=color)
    arrow_start = lin.get_start()+pos*lin.get_length()*lin.get_unit_vector()
    arrow = Arrow(start=arrow_start-0.1*lin.get_unit_vector(),end=arrow_start+0.1*lin.get_unit_vector(),tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(lin,arrow)
    return ray

def CurvedRay(start,end,ext:float=0,radius=2,color=RED,rev = False):
    arc = ArcBetweenPoints(start=start,end=end,radius=radius,color=color)
    n = int(len(arc.get_all_points())/2)
    pt = arc.get_all_points()[n]
    pt2 = arc.get_all_points()[n+1]
    if rev:
        arrow = Arrow(start=pt2,end=pt,tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    else:
        arrow = Arrow(start=pt,end=pt2,tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(arc,arrow)
    return ray

def MyLabeledDot(label_in:Tex| None = None,label_out:Tex| None = None,pos:Vector = DOWN,shift=[0,0,0], point=ORIGIN,radius: float = DEFAULT_DOT_RADIUS,color = WHITE):
        if isinstance(label_in, Tex):
            radius = 0.02 + max(label_in.width, label_in.height) / 2
        
        dot = Dot(point=point,radius=radius,color=color)
        g1 = VGroup(dot)
        if isinstance(label_in, Tex):
            label_in.move_to(dot.get_center())
            g1.add(label_in)
        if isinstance(label_out, Tex):
            label_out.next_to(dot,pos)
            label_out.shift(shift)
            g1.add(label_out)

        return g1


class MyDashLabeledLine(DashedLine):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True  , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)

        if pos is None:
            mask  = Line(label.get_center()-0.6*label.width*self.get_unit_vector(),label.get_center()+0.6*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        self.add(label)

class MyLabeledLine(Line):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        if pos is None:
            if rot:
                mask  = Line(label.get_center()-0.65*label.width*self.get_unit_vector(),label.get_center()+0.65*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            else:
                mask  = Line(label.get_center()-0.65*label.height*self.get_unit_vector(),label.get_center()+0.65*label.height*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)
        self.add(label)


class MyLabeledArrow(MyLabeledLine, Arrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)

class MyDoubLabArrow(MyLabeledLine, DoubleArrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)





def ir(a,b): # inclusive range, useful for TransformByGlyphMap
    return list(range(a,b+1))


class LatexItems(Tex):
    def __init__(self, *args, page_width="15em", itemize="itemize",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{itemize}}}YourTextHere\end{{{itemize}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args, tex_template=template, tex_environment=None,font_size=font_size, **kwargs)


class AlignTex(Tex):
    def __init__(self, *args, page_width="15em",align="align*",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{cancel}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{align}}}YourTextHere\end{{{align}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args,font_size=font_size, tex_template=template, tex_environment=None, **kwargs)


class TransformByGlyphMap(AnimationGroup):
    def __init__(self, mobA, mobB, *glyph_map, replace=True, from_copy=True, show_indices=False, **kwargs):
		# replace=False does not work properly
        if from_copy:
            self.mobA = mobA.copy()
            self.replace = True
        else:
            self.mobA = mobA
            self.replace = replace
        self.mobB = mobB
        self.glyph_map = glyph_map
        self.show_indices = show_indices

        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []
        for from_indices, to_indices in self.glyph_map:
            print(from_indices, to_indices)
            if len(from_indices) == 0 and len(to_indices) == 0:
                self.show_indices = True
                continue
            elif len(to_indices) == 0:
                animations.append(FadeOut(
                    VGroup(*[self.mobA[0][i] for i in from_indices]),
                    shift = self.mobB.get_center()-self.mobA.get_center()
                ))
            elif len(from_indices) == 0:
                animations.append(FadeIn(
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    shift = self.mobB.get_center() - self.mobA.get_center()
                ))
            else:
                animations.append(Transform(
                    VGroup(*[self.mobA[0][i].copy() if i in mentioned_from_indices else self.mobA[0][i] for i in from_indices]),
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    replace_mobject_with_target_in_scene=self.replace
                ))
            mentioned_from_indices.extend(from_indices)
            mentioned_to_indices.extend(to_indices)

        print(mentioned_from_indices, mentioned_to_indices)
        remaining_from_indices = list(set(range(len(self.mobA[0]))) - set(mentioned_from_indices))
        remaining_from_indices.sort()
        remaining_to_indices = list(set(range(len(self.mobB[0]))) - set(mentioned_to_indices))
        remaining_to_indices.sort()
        print(remaining_from_indices, remaining_to_indices)
        if len(remaining_from_indices) == len(remaining_to_indices) and not self.show_indices:
            for from_index, to_index in zip(remaining_from_indices, remaining_to_indices):
                animations.append(Transform(
                    self.mobA[0][from_index],
                    self.mobB[0][to_index],
                    replace_mobject_with_target_in_scene=self.replace
                ))
            super().__init__(*animations, **kwargs)
        else:
            print(f"From indices: {len(remaining_from_indices)}    To indices: {len(remaining_to_indices)}")
            print("Showing indices...")
            super().__init__(
                Create(index_labels(self.mobA[0], color=PINK)),
                FadeIn(self.mobB.next_to(self.mobA, DOWN), shift=DOWN),
                Create(index_labels(self.mobB[0], color=PINK)),
                Wait(5),
                lag_ratio=0.5
                )

class Ex47(Slide):
    def construct(self):

        ex_title = Tex(r"Example 36 :", r" An electric dipole is placed at an angle $60^\circ$ with an electric field of strength $4\times 10^5$ N/C. It experiences a torque equal to $8\sqrt{3}$ Nm. Calculate the charge on the dipole, if dipole is of length 4 cm.",tex_environment="{minipage} {13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) $10^{-1}$ C',font_size=35),Tex(r'(b) $10^{-2}$ C',font_size=35),Tex(r'(c) $10^{-3}$ C',font_size=35),Tex(r'(d) $10^{-4}$ C',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op)) 

class Flux(ThreeDScene,Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN,match_underline_width_to_text=True )
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list2[5]))
        self.play(Circumscribe(list2[5]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        cur_title = Title(" Electric Flux ",match_underline_width_to_text=True, color=GREEN)
        self.play(ReplacementTransform(title,cur_title))
        self.next_slide()
        steps1 = ItemList(Item(r"Sometimes it is useful to treat  \textbf{area} as a vector. It has magnitude and direction.",pw="7 cm"),
                          Item(r"Magnitude is equal to area $ds$",pw="7 cm"),
                          Item(r"Direction is along the normal to the surface $(\hat{n})$; that is, perpendicular to the surface.",pw="7 cm"),
                          Item(r"Since $\hat{n}$ is a unit normal to a surface, ", r"it has two possible directions at every point on that surface. ", r" For an open surface, we can use either direction, as long as we are consistent over the entire surface.",pw="7 cm"),
                          Item(r"On a closed surface, $\hat{n}$ is chosen to be the outward normal at every point",pw="7 cm"),
                        buff=MED_SMALL_BUFF).next_to(cur_title,DOWN,buff=0.4).to_corner(LEFT)
        
        
        plane = Rectangle(height=2,width=2,color=GREEN,fill_opacity=0.4)
        nv = Arrow3D(start=plane.get_center(),end = plane.get_center()+OUT)
        nvlbl = Tex(r"$\hat{n}$",font_size=35).next_to(nv,RIGHT)
        albl  = Tex(r"$ds$",font_size=35).move_to(plane.get_center()+0.5*LEFT+0.1*IN)
        avlbl  = Tex(r"$d\vec{s}=ds\ \hat{n}$",font_size=35,color=PINK).next_to(plane,DOWN).shift(0.3*IN)
        plane2 = plane.copy()
        nv2 = Arrow3D(start=plane2.get_center(),end = plane2.get_center()+IN)
        albl2  = Tex(r"$ds$",font_size=35).move_to(plane2.get_center()+0.5*LEFT+0.1*IN)
        nvlbl2 = Tex(r"$\hat{n}$",font_size=35).next_to(nv2,RIGHT+2*DOWN)
        g1 = VGroup(steps1)
        fig1 = VGroup(plane,nv,nvlbl,albl,avlbl).next_to(steps1,RIGHT).align_to(steps1,UP).shift(2*OUT)
        fig2 = VGroup(plane2,nv2,albl2,nvlbl2).next_to(plane,RIGHT,buff=0.4)
        img = ImageMobject("csurf.png").to_corner(DR).scale(0.9)
        self.add_fixed_in_frame_mobjects(g1,cur_title,img)
        self.add_fixed_orientation_mobjects(nvlbl,albl,avlbl,nvlbl2,albl2)
        self.play(FadeOut(g1,img,nvlbl,albl,avlbl,nvlbl2,albl2),run_time=0)
        self.set_camera_orientation(phi=70 * DEGREES)


        
        self.play(Write(steps1[0]),Create(plane))
        self.next_slide()
        self.play(Write(steps1[1]),Write(albl))
        self.next_slide()
        self.play(Write(steps1[2]),Create(nv),Write(nvlbl),Write(avlbl))
        self.next_slide()
        self.play(Write(steps1[3][0]))
        self.next_slide()
        self.play(Write(steps1[3][1]),Create(plane2),Create(nv2),Write(albl2),Write(nvlbl2))
        self.next_slide()
        self.play(Write(steps1[3][2]))
        self.next_slide()
        self.play(Write(steps1[4]),FadeIn(img))

        
