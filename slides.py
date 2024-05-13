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

class Flux(ThreeDScene,Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FIELDS',color=GREEN,match_underline_width_to_text=True )
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
        self.next_slide()
        self.play(FadeOut(steps1, img, fig1,fig2))

        steps2 = ItemList(Item(r"The concept of \textbf{flux} describes how much of something goes through a given area.",pw="9 cm"),
                          Item(r"You may conceptualize the Electric Flux ($\Delta \phi$) as a measure of the number of electric field lines passing through an area ",pw="9 cm"),
                          Item(r"The larger the area ($\Delta S$), the more field lines go through it and, hence, the greater the flux (i.e., $\Delta \phi\propto \Delta S$)",pw="9 cm"),
                          Item(r"Similarly, the stronger the electric field is (represented by a greater density of lines), the greater the flux. (i.e., $\Delta \phi\propto E$)",pw="9 cm"),
                          Item(r"Similarly, Larger the value of $\cos\theta$ (i.e., at $\theta = 0^\circ$), the more field lines go through it, hence, the greater the flux (i.e., $\Delta \phi\propto \cos\theta$)",pw="9 cm"),
                          Item(r"Electric Flux:", r" \quad $\Delta\phi = E \Delta S \cos\theta$",r"$=\vec{E}\cdot \Delta\vec{S}$",pw="9 cm"),
                        buff=MED_SMALL_BUFF).next_to(cur_title,DOWN,buff=0.4).to_corner(LEFT)
        
        steps3 = ItemList(Item(r"Here, $\theta$ is the angle between $\vec{E}$ and Area vector $\Delta \vec{S}$",pw="9 cm"),
                          Item(r"If $\vec{E}$ is not uniform or if $S$ is a curved surface, we divide $S$ into many small elements $\Delta S$, as the elements become smaller, they can be approximated by flat surfaces.",pw="9 cm"),
                          Item(r"Then electric flux through the area element $\Delta S$ is \\  $\Delta \phi = \vec{E}\cdot \Delta\vec{S}$",pw="9 cm"),
                          Item(r"Then the total flux through entire surface $S$ is \\   $\phi \approx \sum_{i=1}^{n}\vec{E}\cdot \Delta\vec{S}$ ",pw="9 cm"),
                          Item(r"This estimate of the total flux gets better as we decrease the size of the area elements i.e., $(\Delta S \rightarrow 0=dS)$. and the limit of the sum becomes a surface integral.",pw="9 cm"),
                          Item(r"$ \phi = \int_{S} \vec{E}\cdot d\vec{S}$ (For Open surface)", r"\qquad $ \phi = \oint_{S} \vec{E}\cdot d\vec{S}$ (For Closed surface)",pw="13 cm"),
                        buff=MED_SMALL_BUFF).next_to(cur_title,DOWN,buff=0.4).to_corner(LEFT)
        sr = SurroundingRectangle(steps2[-1][1:3].set_color(RED))
        sr2 = SurroundingRectangle(steps3[-1][0].set_color(RED))
        sr3 = SurroundingRectangle(steps3[-1][1].set_color(RED))
        
        
        
        self.set_camera_orientation(phi=0 * DEGREES)
        self.play(FadeOut(steps1, img, fig1,fig2))
        m = ValueTracker(0.5)

        def plane_func(u, v):
            return np.array([- m.get_value(),u, v])
        
        def plane_func_t(u, v):
            return np.array([-0.5*u**2,u, v])
        
        axes = ThreeDAxes(x_range=(-5, 5, 1),
                          y_range=(-5, 5, 1),
                          z_range=(-5, 5, 1),
                          x_length=10,
                          y_length=10,
                          z_length=10,
                          ).scale(0.5)
        ag =VGroup()
        for i in range(3):
            for j in range(3):
                ag.add(Arrow3D(start=1.5*LEFT+(j-1)*1.1*UP+(i-1)*1.1*OUT,end=1.5*RIGHT+(j-1)*1.1*UP+(i-1)*1.1*OUT,color=BLUE))

        surf = Surface(lambda u, v: axes.c2p(*plane_func(u, v)), 
                       u_range=[-3.1, 3.1],
                       v_range=[-3.1, 3.1],
                       fill_opacity=0.99,resolution=10,
                       checkerboard_colors = [RED, RED_E],)
        
        normal = Arrow3D(start=surf.get_center()+0.5*OUT+0.5*UP,end=surf.get_center()+2*RIGHT+0.5*OUT+0.5*UP,color=PINK)
        norlbl = Tex(r"$\Delta \vec{S}$",font_size=35,color=PINK).next_to(normal,RIGHT,buff=0.1)
        Elbl = Tex(r"$\vec{E}$",font_size=35,color=BLUE).next_to(ag[1],RIGHT)
        ag.add(normal,norlbl,Elbl,surf)
        csg =VGroup()
        for i in range(3):
            for j in range(3):
                csg.add(Arrow3D(start=1.5*LEFT+(j-1)*1.1*UP+(i-1)*1.1*OUT,end=1.5*RIGHT+(j-1)*1.1*UP+(i-1)*1.1*OUT,color=BLUE))

        surf2 = Surface(lambda u, v: axes.c2p(*plane_func_t(u, v)), 
                       u_range=[-3, 3],
                       v_range=[-3, 3],
                       fill_opacity=0.99,resolution=10,
                       checkerboard_colors = [PINK, LIGHT_PINK],)
        
        
        
        
        Elbl2 = Tex(r"$\vec{E}$",font_size=35,color=BLUE).next_to(csg[1],RIGHT)
        csg.add(Elbl2,surf2)
        img3 = ImageMobject("sflux2.png").to_corner(DR)

        self.add_fixed_orientation_mobjects(norlbl,Elbl,Elbl2)
        self.add_fixed_in_frame_mobjects(steps2,steps3,img3,sr,sr2,sr3)
        self.remove(steps2,steps3,norlbl,Elbl,img3,sr,sr2,sr3,Elbl2)
        
        VGroup(ag,axes).move_to(3*RIGHT+3*UP-1.2*IN)

        self.set_camera_orientation(phi=60*DEGREES,theta=-50*DEGREES)
        self.add(ag)
        self.wait(2)
        for item in steps2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        self.play(Write(sr))
        self.play(FadeIn(img3))
        self.next_slide()
        
        self.play(FadeOut(steps2,sr,ag,img3))
        self.set_camera_orientation(phi=60*DEGREES,theta=-5*DEGREES)
        self.add(csg.move_to(2*RIGHT+3.5*UP-1.2*IN))
        self.wait(2)
        self.next_slide()
        for item in steps3:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        self.play(Write(VGroup(sr2,sr3)))

        self.wait(2)

class Ex48(Slide):
    def construct(self):

        ex_title = Tex(r"Example 37 :", r" A rectangular surface of sides 10 cm and 15 cm is placed inside a uniform electric field of 25 N/C, such that the surface makes an angle of $30^\circ$ with the direction of electric field. Find the flux of the electric field through the rectangular surface.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) $0.1675\ Nm^2C^{-1}$ ',font_size=35),Tex(r'(b) $0.1875 \ Nm^2C^{-1}$ ',font_size=35),Tex(r'(c) Zero ',font_size=35),Tex(r'(d) $0.1075\ Nm^2C^{-1}$ ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[1]))

class Ex49(Slide):
    def construct(self):

        ex_title = Tex(r"Example 38 :", r" If an electric field is given by $10\hat{i}+3\hat{j}+4\hat{k}$, calculate the electric flux through a surface area of 10 units lying in yz plane",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) 100  units ',font_size=35),Tex(r'(b) 10  units  ',font_size=35),Tex(r'(c) 30  units  ',font_size=35),Tex(r'(d) 40  units  ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[0]))

class Ex50(Slide):
    def construct(self):

        ex_title = Tex(r"Example 39 :", r" If an electric field in a region is given by $a\hat{i}+b\hat{j}$, where $a$ and $b$ are constants. Find the net flux through a square area of side $l$ parallel to y-z plane.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.next_slide()
        self.play(Write(sol_label)) 

class Ex51(Slide):
    def construct(self):

        ex_title = Tex(r"Example 38 :", r" There is a uniform electric field of $8\times 10^3\ \hat{i}$ N/C. What is the net flux (in S.I. Units) of the uniform electric field throughout a cube of side 0.3 m oriented so that its faces are parallel to the coordinate plane?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) $16\times 10^3$ ',font_size=35),Tex(r'(b) $2.4\times 10^3$  ',font_size=35),Tex(r'(c) Zero  ',font_size=35),Tex(r'(d) $48\times 10^3$  ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[2]))

class Gauss(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FIELDS',color=GREEN,match_underline_width_to_text=True )
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list2[6]))
        self.play(Circumscribe(list2[6]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        cur_title = Title(" Gauss's Law ",match_underline_width_to_text=True, color=GREEN)
        self.play(ReplacementTransform(title,cur_title))
        self.next_slide()
        img1 = ImageMobject("flux_intro.png").scale(0.9).next_to(cur_title,DOWN)
        img2 = ImageMobject("flux_intro1.png").scale(0.9).next_to(cur_title,DOWN)
        img2lbl = Tex("(a) The electric flux through a closed surface due to a charge outside that surface is zero.",font_size=35).next_to(img2,DOWN)
        img3 = ImageMobject("flux_intro2.png").scale(1).next_to(cur_title,DOWN)
        img3lbl = Tex("(b) Charges are enclosed, but because the net charge included is zero, the net flux through the closed surface is also zero.",font_size=35).next_to(img3,DOWN)
        img4 = ImageMobject("flux_intro3.png").scale(1).next_to(cur_title,DOWN)
        img4lbl = Tex("(c) The shape and size of the surfaces that enclose a charge does not matter because all surfaces enclosing the same charge have the same flux.",font_size=35).next_to(img4,DOWN)
        statement_lbl =Tex("Statement of Gauss's Law : ",font_size=40, color=ORANGE).next_to(cur_title,DOWN).to_corner(LEFT)
        imp =Tex("Important Points Regarding Gauss's Law : ",font_size=40, color=ORANGE).next_to(cur_title,DOWN).to_corner(LEFT)
        statement =Item(r"According to Gauss's law, the flux $(\Phi)$ of the electric field (E) through any closed surface(S), also called a Gaussian surface, is equal to $\dfrac{1}{\epsilon_0}$ times the net charge enclosed $(q_{enc})$ by the surface.",pw="12 cm", color=BLUE,dot=False).next_to(statement_lbl,DOWN).to_corner(LEFT,buff=0.2)
        formula =Item(r" $\Phi_{\text{Closed surface}}=\oint_{s} \vec{E}\cdot d\vec{S}=\dfrac{q_{enc}}{\epsilon_0}$",pw="12 cm", color=PINK,dot=False).next_to(statement,DOWN).to_corner(LEFT,buff=2)
        sr = SurroundingRectangle(statement)
        img5 = ImageMobject("gausslaw.png").scale(0.7).next_to(sr,DOWN).to_edge(RIGHT)

        

        imppt = ItemList(Item(r"The term $q_{enc}$ in Gauss's law is just the net charge enclosed (or inside) (i.e. $q_1,\ q_2$ and $q_5$) the Gaussian surface(S)",pw="6 cm"),
                          Item(r"Charges Outside the surface (i.e., $q_3,\ q_4,\ q_6,\ ..., \ q_n $), no matter how large or how nearby it may be, is not included in the term $q_{enc}$ in Gauss law.",pw="6 cm"),
                          Item(r"The electric field $\vec{E}$ used in the Gauss's law is the total electric field at every point on the Gaussian surface, due to \textbf{all charges inside or outside} the Gaussian surface.",pw="6 cm"),
                        buff=MED_SMALL_BUFF).next_to(imp,DOWN,buff=0.4).to_corner(LEFT)
        
        imppt2 = ItemList(Item(r"Gaussian surface is any closed surface in space. ", r" That surface can coincide with the actual surface of a conductor, or it can be an imaginary geometric surface. ", r"The only requirement imposed on a Gaussian surface is that it be closed.",pw="6 cm"),
                          Item(r"The Gaussian surface should not pass through any discrete charge because the electric field due to a discrete charge at its location is not defined. ",r"However it can pass through a continuous charge distribution.",pw="6 cm"),
                        buff=MED_SMALL_BUFF).next_to(imp,DOWN,buff=0.4).to_corner(LEFT)
        
        imppt3 = ItemList(Item(r"Gauss's law is true for  any closed surface, no matter what its shape or size be.",pw="6 cm"),
                          Item(r"If $q_{enc}$ is positive, the net flux is outward. ",r"If $q_{enc}$ is negative, net flux is inward.",pw="6 cm"),
                          Item(r"If $q_{enc}=0$, then $\Phi = \oint_s \vec{E}\cdot d\vec{S}=0$,",r"But, $E$ may or may not be Zero.",pw="6 cm"),
                          Item(r"Gauss's law is commonly used for calculating electric field for symmetric charge configuration.",pw="6 cm"),
                          Item(r"Gauss's law and Coulomb's law are equivalent.",pw="13 cm"),
                        buff=MED_SMALL_BUFF).next_to(imp,DOWN,buff=0.4).to_corner(LEFT)
        self.play(FadeIn(img1))
        self.next_slide()
        self.play(FadeOut(img1))
        self.play(FadeIn(img2),Write(img2lbl))
        self.next_slide()
        self.play(FadeOut(img2,img2lbl))
        self.play(FadeIn(img3),Write(img3lbl))
        self.next_slide()
        self.play(FadeOut(img3,img3lbl))
        self.play(FadeIn(img4),Write(img4lbl))
        self.next_slide()
        self.play(FadeOut(img4,img4lbl))
        self.wait(1)
        self.play(Write(statement_lbl))
        self.next_slide()
        self.play(Write(statement[0]),Write(sr),FadeIn(img5))
        self.next_slide()
        sr2=SurroundingRectangle(formula,color=RED)
        self.play(Write(formula),Write(sr2))
        self.next_slide()
        self.play(FadeOut(statement,sr),VGroup(sr2,formula).animate.next_to(cur_title,DOWN).to_corner(RIGHT),img5.animate.scale(1.3).to_corner(DR),ReplacementTransform(statement_lbl,imp))
        self.next_slide()  
        for item in imppt:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeOut(imppt))
        self.wait(1)

        for item in imppt2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        
        img7 =  ImageMobject("nflux.png").scale(0.6).next_to(sr2,DOWN).to_edge(RIGHT)
        img6 =  ImageMobject("pflux.png").scale(0.6).next_to(img7,LEFT)
        self.play(FadeOut(img5,imppt2),FadeIn(img4.next_to(sr2,DOWN).to_edge(RIGHT)),Write(imppt3[0]))
        self.next_slide()
        self.play(FadeOut(img4),Write(imppt3[1][0]),FadeIn(img6))
        self.next_slide()
        self.play(Write(imppt3[1][1]),FadeIn(img7))
        self.next_slide()
        self.play(Write(imppt3[2][0]))
        self.next_slide()
        self.play(Write(imppt3[2][1]))
        self.next_slide()
        self.play(Write(imppt3[3]))
        self.next_slide()
        self.play(Write(imppt3[4]))
        self.next_slide()
        self.play(FadeOut(imppt3,img6, img7, sr2,formula,cur_title))
        proof_lbl =Tex("Proof of Gauss's Law  for Spherically Symmetric Surface : ",font_size=40, color=ORANGE).to_corner(UL)
        self.play(ReplacementTransform(imp,proof_lbl))
        self.next_slide()
        proof = ItemList(Item(r" Let's calculate the electric flux through a spherical surface around a positive point charge $q$",pw="13 cm"),
                          Item(r"The electric field at a point P on the surface at distance $R$ from the charge at the origin is given by:\quad",r" $\vec{E}=\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{R^2}\hat{r}$",pw="13 cm",dot=False),
                          Item(r"The total flux $(\Phi)$ passing through the spherical surface $S$ is: ",pw="6 cm"),
                          Item(r"\Phi &= \oint_{S} \vec{E}\cdot dA\ \hat{n}",r"=\oint_{S}\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{R^2}\hat{r}\cdot  \hat{n} dA\\",r"&=\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{R^2}\oint_{S} dA",r"=\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{R^2}\times 4\pi R^2\\",r"\Phi&=\dfrac{q}{\epsilon_0}",math=True,dot=False,pw="13 cm"),
                          buff=0.4).next_to(imp,DOWN,buff=0.4).to_corner(LEFT)
        sr3=SurroundingRectangle(proof[-1][-1])
        
        img8 = ImageMobject("gaussproof.png").scale(0.6).next_to(proof_lbl,DOWN).to_corner(DR)
        
        self.play(FadeIn(img8))
        self.next_slide()
        for item in proof:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        
        self.play(Write(sr3))


class Ex52(Slide):
    def construct(self):

        ex_title = Tex(r"Example 39 :", r" Calculate the electric flux through each Gaussian surface shown in Figure",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()
        img = ImageMobject("ex52.png").next_to(ex_title,DOWN)
        self.play(FadeIn(img))

class Ex53(Slide):
    def construct(self):

        ex_title = Tex(r"Example 40 :", r" A charge $q$ is situated at the centre of a cube. Electric flux through one of the faces of the cube is",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) $\dfrac{q}{\epsilon_0}$ ',font_size=35),Tex(r'(b) $\dfrac{q}{3\epsilon_0}$  ',font_size=35),Tex(r'(c) $\dfrac{q}{6\epsilon_0}$  ',font_size=35),Tex(r'(d) Zero  ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[2]))

class Ex54(Slide):
    def construct(self):

        ex_title = Tex(r"Example 41 :", r" A charge $q$ is placed at the centre of the open end of cylindrical vessel. Electric flux through the surface of the vessel is ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) $\dfrac{q}{2\epsilon_0}$ ',font_size=35),Tex(r'(b) $\dfrac{q}{\epsilon_0}$  ',font_size=35),Tex(r'(c) $\dfrac{2q}{\epsilon_0}$  ',font_size=35),Tex(r'(d) Zero  ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[0]))

class Ex55(Slide):
    def construct(self):

        ex_title = Tex(r"Example 42 :", r" A hemispherical surface of radius $R$ is kept in a uniform electric field $E$ as shown in the figure. The flux through the curved surface is ",tex_environment="{minipage}{8 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        img = ImageMobject("Ex55.png").scale(0.8).next_to(ex_title,RIGHT).align_to(ex_title,UP)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title),FadeIn(img))
        self.next_slide()

        op = VGroup(Tex(r'(a) $E\times 2\pi R^2$ ',font_size=35),Tex(r'(b) $E\times \pi R^2$ ',font_size=35),Tex(r'(c) $E\times 4\pi R^2$  ',font_size=35),Tex(r'(d) Zero  ',font_size=35) ).arrange_in_grid(2,2,buff=(2,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[1]))

class Ex56(Slide):
    def construct(self):

        ex_title = Tex(r"Example 43 :", r" A charge of 1 C is located at the centre of a sphere of radius 10 cm and a cube of side 20 cm. The ratio of outgoing flux from the sphere and cube will be ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) More than one ',font_size=35),Tex(r'(b) Less than one ',font_size=35),Tex(r'(c) one  ',font_size=35),Tex(r'(d) Nothing can be said  ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[2]))

class Ex57(Slide):
    def construct(self):

        ex_title = Tex(r"Example 44 :", r" If the number of electric lines of force emerging out of  a closed surface is 1000, then the charge enclosed by the surface is ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) $8.854\times 10^{-9}$ C ',font_size=35),Tex(r'(b) $8.854\times 10^{-4}$ C ',font_size=35),Tex(r'(c) $8.854\times 10^{-1}$ C  ',font_size=35),Tex(r'(d) $8.854$ C  ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[0]))

class Ex58(Slide):
    def construct(self):

        ex_title = Tex(r"Example 45 :", r" The electric field components in Fig. 1.27 are $E_x = \alpha x^{1/2}, E_y = E_z = 0,$ in which $\alpha = 800 NC^{-1} m^{-1/2}$. Calculate (a) the flux through the cube, and (b) the charge within the cube. Assume that $a = 0.1$ m",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()
        img = ImageMobject("Ex58.png").scale(0.7).next_to(ex_title,DOWN).to_edge(RIGHT)
        self.play(FadeIn(img))

class Ex59(Slide):
    def construct(self):

        ex_title = Tex(r"Example 46 :", r" An electric field is uniform, and in the positive $x$ direction for positive x, and uniform with the same magnitude but in the negative $x$ direction for negative $x$. It is given that $E = 200 \ \hat{i}$ N/C for $x > 0$ and $E = -200\ \hat{i}$ N/C for $x < 0$. A right circular cylinder of length 20 cm and radius 5 cm has its centre at the origin and its axis along the x-axis so that one face is at $x = +10$ cm and the other is at $x = 10$ cm (Fig.). ", r"(a) What is the net outward flux through each flat face? ", r"(b) What is the flux through the side of the cylinder? ", r"(c) What is the net outward flux through the cylinder? ", r"(d) What is the net charge inside the cylinder?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        img = ImageMobject("Ex59.png").scale(0.6).next_to(ex_title,DOWN).to_edge(RIGHT)
        for item in ex_title:
            self.play(Write(item))
            self.next_slide()
        
        self.play(FadeIn(img))

class Ex60(Slide):
    def construct(self):

        ex_title = Tex(r"Example 47 :", r" Careful measurement of the electric field at the surface of a black box indicates that the net outward flux through the surface of the box is $8.0 \times 10^3\ Nm^2/C$. (a) What is the net charge inside the box? b) If the net outward flux through the surface of the box were zero, could you conclude that there were no charges inside the box? Why or Why not?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))


class Ex61(Slide):
    def construct(self):

        ex_title = Tex(r"Example 48 :", r" A point charge $+10\ \mu$C is a distance 5 cm directly above the centre of a square of side 10 cm, as shown in Fig. 1.34. What is the magnitude of the electric flux through the square? (Hint: Think of the square as one face of a cube with edge 10 cm.)",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        img = ImageMobject("Ex61.png").scale(0.6).next_to(ex_title,DOWN).to_edge(RIGHT)
        
        self.play(FadeIn(img))

class Ex62(Slide):
    def construct(self):

        ex_title = Tex(r"Example 49 :", r" A point charge of $2.0\ \mu$C is at the centre of a cubic Gaussian surface 9.0 cm on edge. What is the net electric flux through the surface?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))

class Ex63(Slide):
    def construct(self):

        ex_title = Tex(r"Example 50 :", r" A point charge causes an electric flux of $-1.0 \times 10^3\ Nm^2/C$ to pass through a spherical Gaussian surface of 10.0 cm radius centred on the charge. (a) If the radius of the Gaussian surface were doubled, how much flux would pass through the surface? (b) What is the value of the point charge?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))

class Continuous(Slide):
    def construct(self):
        cur_title = Title(" CONTINUOUS CHARGE DISTRIBUTION ",match_underline_width_to_text=True, color=GREEN,underline_buff=SMALL_BUFF)
        self.play(Write(cur_title))
        self.next_slide() 
        content = ItemList(Item(r" The charge distributions we have seen so far have been discrete: made up of individual point particles $(q_1\ q_2,\ q_3, ....\ q_n)$",pw="13 cm"),
                          Item(r"If the region in which charges are closely spaced is said to have continuous distribution of charge. ",pw="13 cm"),
                          Item(r"For continuous distribution of charges, it is impractical to specify the charge distribution in terms of the locations of the microscopic charged constituents(electrons or protons).",pw="13 cm"),
                          Item(r"For continuous charge distribution, we can generalize the definition of the electric field. We simply divide the charge into infinitesimal pieces and treat each piece as a point charge.",
                          pw="13 cm"),
                          Item(r"Our first step is to define a charge density for a charge distribution along a line, across a surface, or within a volume",pw="13 cm"),
                          buff=0.4).next_to(cur_title,DOWN,buff=0.4).to_corner(LEFT)
        linear_title = Tex(r"Linear/Line Charge distribution",tex_environment="{minipage}{13 cm}",font_size=40, color=BLUE_C).next_to(cur_title,DOWN).to_edge(LEFT)
        linear = ItemList(Item(r" Let charge $Q$ is uniformly distributed along a line of length $L$, with \textbf{linear charge density (charge per unit length)} $\lambda$ ",pw="6 cm"),
                          Item(r"$\lambda= \dfrac{Q}{L}$\qquad ","S.I unit : C/m",pw="6 cm"),
                          Item(r"The charge $dQ$ on a small element $dl$ of the wire will be",pw="13 cm"),
                          Item(r"$dQ= \lambda\times dl$\qquad",r"(We can consider this element as a point charge.)",pw="13 cm"),
                          buff=0.4).next_to(linear_title,DOWN,buff=0.4).to_corner(LEFT)
        
        img1 = ImageMobject("linear.png").scale(0.75).next_to(linear[0],RIGHT)
        for item in content:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(content),Write(linear_title),FadeIn(img1))
        for item in linear:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
