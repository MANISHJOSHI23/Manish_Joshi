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
        surface_title = Tex(r"Surface Charge distribution",tex_environment="{minipage}{13 cm}",font_size=40, color=BLUE_C).next_to(cur_title,DOWN).to_edge(LEFT)
        volume_title = Tex(r"Volume Charge distribution",tex_environment="{minipage}{13 cm}",font_size=40, color=BLUE_C).next_to(cur_title,DOWN).to_edge(LEFT)
        linear = ItemList(Item(r" Let charge $Q$ is uniformly distributed along a line of length $L$, with \textbf{linear charge density (charge per unit length)} $\lambda$ ",pw="6 cm"),
                          Item(r"$\lambda= \dfrac{Q}{L}$\qquad ","S.I unit : C/m",pw="6 cm"),
                          Item(r"The charge $dQ$ on a small element $dl$ of the wire will be",pw="13 cm"),
                          Item(r"$dQ= \lambda\times dl$\qquad",r"(We can consider this element as a point charge.)",pw="13 cm"),
                          Item(r"Electric field due to small element at any point is\quad ",r"$dE=\dfrac{1}{4\pi\epsilon_0}\dfrac{dq}{r^2}$",r"$=\dfrac{1}{4\pi\epsilon_0}\dfrac{\lambda dl}{r^2}$",pw="13 cm"),
                          buff=0.4).next_to(linear_title,DOWN,buff=0.4).to_corner(LEFT)
                        
        surface = ItemList(Item(r" Let charge $Q$ is uniformly distributed uniformly on a surface $A$, with \textbf{surface charge density (charge per unit area)} $\sigma$ ",pw="6 cm"),
                          Item(r"$\sigma= \dfrac{Q}{A}$\qquad ","S.I unit : C/m$^2$",pw="6 cm"),
                          Item(r"The charge $dQ$ on a small area element $dA$  will be",pw="6 cm"),
                          Item(r"$dQ= \sigma\times dA$\qquad",r"(We can consider this element as a point charge.)",pw="10 cm"),
                          Item(r"Electric field due to small element at any point is\quad ",r"$dE=\dfrac{1}{4\pi\epsilon_0}\dfrac{dq}{r^2}$",r"$=\dfrac{1}{4\pi\epsilon_0}\dfrac{\sigma dA}{r^2}$",pw="13 cm"),
                          buff=0.4).next_to(linear_title,DOWN,buff=0.4).to_corner(LEFT)
        
        volume = ItemList(Item(r" If some charge $Q$ is uniformly distributed uniformly om a volume $V$, with \textbf{volume charge density (charge per unit volume)} $\rho$ ",pw="6 cm"),
                          Item(r"$\rho= \dfrac{Q}{V}$\qquad ","S.I unit : C/m$^3$",pw="6 cm"),
                          Item(r"The charge $dQ$ on a small volume element $dV$  will be",pw="13 cm"),
                          Item(r"$dQ= \sigma\times dV$\qquad",r"(We can consider this element as a point charge.)",pw="13 cm"),
                          Item(r"Electric field due to small element at any point is\quad ",r"$dE=\dfrac{1}{4\pi\epsilon_0}\dfrac{dq}{r^2}$",r"$=\dfrac{1}{4\pi\epsilon_0}\dfrac{\rho dV}{r^2}$",pw="13 cm"),
                          buff=0.4).next_to(linear_title,DOWN,buff=0.4).to_corner(LEFT)
    
        img1 = ImageMobject("linear.png").scale(0.75).next_to(linear[0],RIGHT)
        img2 = ImageMobject("surface.png").scale(0.75).next_to(surface[0],RIGHT).align_to(surface_title,UP)
        img3 = ImageMobject("volume.png").scale(0.75).next_to(volume[0],RIGHT)
        for item in content:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(content),Write(linear_title),FadeIn(img1))
        for item in linear:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(FadeOut(linear,linear_title,img1),Write(surface_title),FadeIn(img2))
        for item in surface:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(FadeOut(surface,img2,surface_title),Write(volume_title),FadeIn(img3))
        for item in volume:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()


class LineCharge(ThreeDScene,Slide):
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
        self.play(FocusOn(list2[7]))
        self.play(Circumscribe(list2[7]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        cur_title = Title(" Applications of Gauss's Law ",match_underline_width_to_text=True, color=GREEN,underline_buff=SMALL_BUFF)
        self.play(ReplacementTransform(title,cur_title))
        line_title = Tex("(1) Electric Filed Due to Infinite Long Uniformly Charged Straight Wire:",font_size=35,color=GOLD).next_to(cur_title,DOWN).to_edge(LEFT)
        self.add_fixed_in_frame_mobjects(line_title,cur_title)
        self.play(FadeOut(line_title),run_time=0)
        self.next_slide()
        self.play(Write(line_title))
        self.next_slide()
        line = Cylinder(0.05,5,Y_AXIS,fill_opacity=1,checkerboard_colors = [GREEN, GREEN]).set_stroke(GREEN,opacity=1,width=0)
        density = Tex("$\lambda$",font_size=35).next_to(line,LEFT,buff=0.1)
        dot = MyLabeledDot(label_out=Tex("P",font_size=25),pos=RIGHT,point=1.5*RIGHT)
        gsurf = Cylinder(1.5,2.5,Y_AXIS,fill_opacity=0.4,resolution=100,
                       checkerboard_colors = [PINK, PINK]).set_stroke(PINK,opacity=0.4,width=0)
        r = MyLabeledLine(label=Tex("$r$",font_size=35),start=line.get_center(),end=1.5*RIGHT,pos=0.2*DOWN,color=GRAY)
        l = MyDoubLabArrow(label=Tex("$l$",font_size=35),start=gsurf.get_top(),end=gsurf.get_bottom(),tip_length=0.1,rot=False,color=GOLD,opacity=1).next_to(gsurf,LEFT)
        
        
        axes = ThreeDAxes(x_range=(-5, 5, 1),
                          y_range=(-5, 5, 1),
                          z_range=(-5, 5, 1),
                          x_length=10,
                          y_length=10,
                          z_length=10,
                          ).scale(0.5)
        
        def plane_func(u, v):
            return np.array([u,2.5, v])

        surf = Surface(lambda u, v: axes.c2p(*plane_func(u, v)), 
                       u_range=[0.5, 1.3],
                       v_range=[0.5, 1.3],
                       fill_opacity=0.99,resolution=1,
                       checkerboard_colors = [RED, RED_E],)
        
        s1 = Arrow3D(surf.get_center(),surf.get_center()+UP,color=BLUE)
        e1 = Arrow3D(surf.get_center(),surf.get_center()+RIGHT,color=RED)
        s1_lbl = Tex(r"$\hat{n}$",font_size=35,color=BLUE).next_to(s1,UP,buff=0.1)
        e1_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).move_to(e1.get_end()).next_to(e1,RIGHT,buff=0)
        ds1 = Tex(r"$S_1$",font_size=35,color=YELLOW).move_to(gsurf.get_center()+gsurf.get_top()+0.8*LEFT)
        ds2 = Tex(r"$S_2$",font_size=35,color=YELLOW).move_to(gsurf.get_center()+gsurf.get_bottom()+0.8*LEFT)
        ds3 = Tex(r"$S_3$",font_size=35,color=YELLOW).move_to(gsurf.get_center()+0.8*LEFT)
        
        def plane_func2(u, v):
            return np.array([u,-2.5, v])

        surf2 = Surface(lambda u, v: axes.c2p(*plane_func2(u, v)), 
                       u_range=[0.5, 1.3],
                       v_range=[0.5, 1.3],
                       fill_opacity=0.99,resolution=1,
                       checkerboard_colors = [GOLD],)
        
        s2 = Arrow3D(surf2.get_center(),surf2.get_center()+DOWN,color=BLUE)
        e2 = Arrow3D(surf2.get_center(),surf2.get_center()+RIGHT,color=RED)
        s2_lbl = Tex(r"$\hat{n}$",font_size=35,color=BLUE).next_to(s2,DOWN,buff=0.1)
        e2_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).next_to(e2,RIGHT,buff=0.1)
        
        def plane_func3(u, v):
            return np.array([1.5,u,v])

        surf3 = Surface(lambda u, v: axes.c2p(*plane_func3(u, v)), 
                       u_range=[0.7, 1.5],
                       v_range=[0.7, 1.5],
                       fill_opacity=0.99,resolution=1,
                       checkerboard_colors = [RED, RED_E],).move_to(1.5*RIGHT+0.5*UP)
        
        s3 = Arrow3D(surf3.get_center()+0.1*UP,surf3.get_center()+0.1*UP+RIGHT,color=BLUE)
        e3 = Arrow3D(surf3.get_center()+0.1*DOWN,surf3.get_center()+0.1*DOWN+RIGHT,color=RED)
        s3_lbl = Tex(r"$\hat{n}$",font_size=35,color=BLUE).next_to(s3,UR,buff=0)
        e3_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).next_to(e3,DR,buff=0)
        pg = VGroup()
        for i in range(0,25):
            pg.add(Tex("$+$",font_size=20,color=BLACK).move_to(line.get_top()+i*0.2*DOWN))

        #self.add_fixed_orientation_mobjects()
        img = VGroup(line,density,dot,gsurf,r,l,pg,surf,surf2,surf3,s1,s2,s3,e1,e2,e3,s1_lbl,s2_lbl,s3_lbl,e1_lbl,e2_lbl,e3_lbl,ds1,ds2,ds3).to_corner(UR).shift(1.5*DOWN)
        self.set_camera_orientation(phi=-20*DEGREES)

        line_charge = ItemList(Item(r"Consider an infinite long straight wire, with uniform charge density $\lambda$",pw="8 cm"),
                          Item(r"We have to find electric field $(E)$ at point P using Gauss's Law.",pw="8 cm"),
                          Item(r"From symmetry, the electric field is radial everywhere and its magnitude only depends on the radial distance $r$",pw="8 cm"),
                          Item(r"From Gauss's Law, Total electric flux through the cylindrical Gaussian surface is: ",pw="8 cm"),
                          Item(r"$\Phi=\oint \vec{E}\cdot d\vec{S}=\dfrac{q_{enc}}{\epsilon_0}$",pw="13 cm"),
                          buff=0.4).next_to(line_title,DOWN).to_corner(LEFT)
        
        line_charge2 = ItemList(Item(r"&\oint \vec{E}\cdot d\vec{S}",r" =\int_{S_1}\vec{E}\cdot d\vec{S}", r"+\int_{S_2}\vec{E}\cdot d\vec{S}", r"+\int_{S_3}\vec{E}\cdot d\vec{S}", r"=\dfrac{q_{enc}}{\epsilon_0}\\",r" & \int_{S_1} E ds\cos(90^\circ)+\int_{S_2} E ds\cos(90^\circ)+\int_{S_3} E ds\cos(0^\circ)=\dfrac{q_{enc}}{\epsilon_0}\\ ",r"&  0+0+E \int_{S_3} ds =\dfrac{q_{enc}}{\epsilon_0}\\",r"& E\times 2\pi r l =\dfrac{\lambda l}{\epsilon_0}\ (\because q_{enc} = \lambda l )\\",r" & E  = \dfrac{1}{2\pi\epsilon_0}\dfrac{\lambda}{r}",math=True,dot=False),
                                Item(r" If charge is $+$Ve ",r"$\implies $ Direction : radially outwards"),
                                Item(r" If charge is $-$Ve ",r"$\implies $ Direction : radially inwards"),buff=0.4).next_to(line_title,DOWN).to_corner(LEFT)
        self.add_fixed_in_frame_mobjects(line_charge,line_charge2)
        self.play(FadeOut(line_charge,line_charge2),run_time=0)

        self.play(Write(line_charge[0]),Create(line),Write(pg),Write(density))
        self.next_slide()
        self.play(Write(line_charge[1]),FadeIn(dot),FadeIn(r))
        self.next_slide()
        self.play(Write(line_charge[2]),FadeIn(e3,e3_lbl))
        self.next_slide()
        self.play(Write(line_charge[3]))
        self.add(gsurf,l)
        self.wait(2)
        self.next_slide()
        self.play(Write(line_charge[4]))
        self.next_slide()
        self.play(Write(VGroup(ds1,ds2,ds3)))
        self.next_slide()
        self.play(FadeIn(VGroup(surf,surf2,surf3,s1,s2,s3,s1_lbl,s2_lbl,s3_lbl)))
        self.next_slide()
        self.play(FadeIn(VGroup(e1,e2,e1_lbl,e2_lbl)))
        self.next_slide()
        self.play(FadeOut(line_charge,cur_title),line_title.animate.to_edge(UL,buff=0.2))
        line_charge2.next_to(line_title,DOWN).to_corner(LEFT)
        self.next_slide()
        sr=SurroundingRectangle(line_charge2[0][-1])
        for item in line_charge2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.add_fixed_in_frame_mobjects(sr)
        self.wait(2)
        self.next_slide()
        self.play(FadeOut(line_charge2,sr))

        axes_2 = (Axes(
        x_range=[0, 5, 0.5],
        y_range=[0, 50, 5],
        y_length=5,
        x_length=6,
        x_axis_config={"include_numbers": True}
      ).to_edge(LEFT).set_color(GREY))
        axes_labels = axes_2.get_axis_labels(x_label="r", y_label="E")

        func = axes_2.plot(lambda x: 4.5/x, x_range=[0.1, 4.5], color=BLUE)
        self.play(Write(line_charge2[0][-1]),line_charge2[0][-1].animate.move_to(axes_2.get_center()))
        self.add_fixed_in_frame_mobjects(axes_2,axes_labels,func)
        self.play(FadeOut(axes_2,axes_labels,func),run_time=0)

        self.play(Create(axes_2),Create(axes_labels))
        self.next_slide()
        self.play(Create(func))


class PlaneSheet(ThreeDScene,Slide):
    def construct(self):
        plane_title = Tex("(2) Electric Filed Due to Uniformly Charged Infinite Plane Sheet:",font_size=35,color=GOLD).to_corner(UL)
        self.play(Write(plane_title))
        self.next_slide()
        axes = ThreeDAxes(x_range=(-6, 6, 1),
                          y_range=(-6, 6, 1),
                          z_range=(-5, 5, 1),
                          x_length=10,
                          y_length=10,
                          z_length=10,
                          ).scale(0.5).shift(1.2*IN+3.5*LEFT-1.5*DOWN)
        def plane_func(x,u, v):
            return np.array([x,u, v])

        plane = Surface(lambda u, v: axes.c2p(*plane_func(0,u, v)), 
                       u_range=[-3, 3],
                       v_range=[-3, 3],
                       fill_opacity=0.95,resolution=30,
                       checkerboard_colors = [GREEN_D, BLUE_D],).set_stroke(GREEN,opacity=0.0,width=0)
        density = Tex("$\sigma$",font_size=35).move_to(plane.get_center()+1.4*OUT)
        pc = VGroup()
        for i in range(-3,3):
            for j in range(-3,3):
                pc.add(Tex("$+$",font_size=35,color=BLACK).move_to(axes.c2p(0,i+0.5,j+0.5)).rotate(PI/2,UP))
        dot = Dot(point=axes.c2p(6,0,0),radius=0.05)
        dot_lbl = Tex("P",font_size=25).next_to(dot,RIGHT,buff=0.1)
        l = Line(start=plane.get_center(),end=dot.get_center(),color=YELLOW_B).set_stroke(opacity=0.7)
        l_lbl=Tex("$r$",font_size=35).move_to(axes.c2p(2,0.25,-1))

        def circ_func(x,v,u):
            return np.array([x, v*np.cos(u), v*np.sin(u)])
        
        cir1 = Surface(lambda u, v: axes.c2p(*circ_func(-6, v,u)), 
                       u_range=[0, 2*PI],
                       v_range=[0, 2],
                       fill_opacity=0.6,resolution=30,
                       checkerboard_colors = [BLUE, BLUE]).set_stroke(BLUE,opacity=0.7,width=0)

        cir2 = Surface(lambda u, v: axes.c2p(*circ_func(6,v, u)), 
                       u_range=[0, 2*PI],
                       v_range=[0, 2],
                       fill_opacity=0.6,resolution=30,
                       checkerboard_colors = [BLUE, BLUE]).set_stroke(BLUE,opacity=0.7,width=0)


        def gsurf_func(u, v):
            return np.array([v, 2*np.cos(u), 2*np.sin(u)])

        gsurf = Surface(lambda u, v: axes.c2p(*gsurf_func(u, v)), 
                       u_range=[0, 2*PI],
                       v_range=[-6, 6],
                       fill_opacity=0.6,resolution=30,
                       checkerboard_colors = [PINK, PINK]).set_stroke(PINK,opacity=0.7,width=0)

        surf1 = Surface(lambda u, v: axes.c2p(*plane_func(-6,u, v)), 
                       u_range=[0.5, 1.3],
                       v_range=[0.5, 1.3],
                       fill_opacity=0.99,resolution=5,
                       checkerboard_colors = [GOLD,LIGHT_BROWN],)
        
        surf2 = Surface(lambda u, v: axes.c2p(*plane_func(6,u, v)), 
                       u_range=[0.5, 1.3],
                       v_range=[0.5, 1.3],
                       fill_opacity=0.99,resolution=5,
                       checkerboard_colors = [GOLD,LIGHT_BROWN],)
        

        surf3 = Surface(lambda u, v: axes.c2p(*gsurf_func(u, v)), 
                       u_range=[1.25, 1.9],
                       v_range=[2.5, 3.3],
                       fill_opacity=0.99,resolution=5,
                       checkerboard_colors = [GOLD,LIGHT_BROWN],)
        

        s1 = Arrow3D(surf1.get_center()+0.1*IN,surf1.get_center()+0.1*IN+0.7*LEFT,color=BLUE)
        e1 = Arrow3D(surf1.get_center()+0.1*OUT,surf1.get_center()+0.1*OUT+LEFT,color=RED)
        s1_lbl = Tex(r"$\hat{n}$",font_size=35,color=BLUE).next_to(s1,LEFT,buff=0.1)
        e1_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).next_to(e1,LEFT,buff=0.1)
        
        s2 = Arrow3D(surf2.get_center()+0.1*IN,surf2.get_center()+0.1*IN+0.7*RIGHT,color=BLUE)
        e2 = Arrow3D(surf2.get_center()+0.1*OUT,surf2.get_center()+0.1*OUT+RIGHT,color=RED)
        s2_lbl = Tex(r"$\hat{n}$",font_size=35,color=BLUE).next_to(s2,RIGHT,buff=0.1)
        e2_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).next_to(e2,RIGHT,buff=0.1)

        s3 = Arrow3D(surf3.get_center(),surf3.get_center()+0.7*OUT,color=BLUE)
        e3 = Arrow3D(surf3.get_center(),surf3.get_center()+RIGHT,color=RED)
        s3_lbl = Tex(r"$\hat{n}$",font_size=35,color=BLUE).next_to(s3,OUT,buff=0.1)
        e3_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).next_to(e3,OUT,buff=0.2)

        ds1 = Tex(r"$S_1$",font_size=35,color=YELLOW).move_to(axes.c2p(-6,-0.9,-0.9)).rotate(PI/2,UP).rotate(PI/2,RIGHT)
        ds2 = Tex(r"$S_2$",font_size=35,color=YELLOW).move_to(axes.c2p(6,-0.9,-0.9)).rotate(PI/2,UP).rotate(PI/2,RIGHT)
        ds3 = Tex(r"$S_3$",font_size=35,color=YELLOW).next_to(s3,IN)

        ca = CurvedArrow(gsurf.get_right()+0.8*IN,gsurf.get_right()+1.5*IN+0.5*RIGHT)
        A_lbl = Tex(r"Area $(A)$",font_size=35,color=YELLOW).move_to(ca.get_tip())
        
        #img = VGroup(plane, density, dot,gsurf,l,pc,surf1,e1,s1,s1_lbl,e1_lbl,surf2,s2,e2,s2_lbl,e2_lbl,surf3,s3,e3,s3_lbl,e3_lbl,ds1,ds2,ds3,dot_lbl,l_lbl,ca,A_lbl)

        plane1 = ItemList(Item(r"Consider an infinite long thin plane sheet, with uniform charge density $\sigma$",pw="12 cm"),
                          Item(r"We have to find electric field $(E)$ at point P using Gauss's Law.",pw="12 cm"),
                          Item(r"From symmetry, the electric field is outward perpendicular to the plane (for $+\sigma$) and inwards (for $-\sigma$) ",pw="10 cm"),
                          Item(r"From Gauss's Law, Total electric flux through the cylindrical Gaussian surface of cross-sectional area $(A)$ is: ",pw="7 cm"),
                          Item(r"$\Phi=\oint \vec{E}\cdot d\vec{S}=\dfrac{q_{enc}}{\epsilon_0}$",pw="13 cm"),
                          buff=0.4).next_to(plane_title,DOWN).to_corner(LEFT)
        
        plane2 = ItemList(Item(r"&\oint \vec{E}\cdot d\vec{S}",r" =\int_{S_1}\vec{E}\cdot d\vec{S}", r"+\int_{S_2}\vec{E}\cdot d\vec{S}", r"+\int_{S_3}\vec{E}\cdot d\vec{S}", r"=\dfrac{q_{enc}}{\epsilon_0}\\",r" & \int_{S_1} E ds\cos(0^\circ)+\int_{S_2} E ds\cos(0^\circ)+\int_{S_3} E ds\cos(90^\circ)=\dfrac{q_{enc}}{\epsilon_0}\\ ",r"&  E \int_{S_1} ds + E \int_{S_2} ds + 0 =\dfrac{q_{enc}}{\epsilon_0}\\",r"& EA + EA =\dfrac{\sigma A}{\epsilon_0}\ (\because q_{enc} = \sigma A )\\",r" & 2EA  = \dfrac{\sigma A}{\epsilon_0}\\",r" & E  = \dfrac{\sigma }{2\epsilon_0}\\",math=True,dot=False),
                                Item(r"\textbf{Electric field} due to uniformly charged infinite plane sheet is \textbf{independent of r, the distance of the point from the plane.}",pw="8 cm"),
                                buff=0.4).next_to(plane_title,DOWN).to_corner(LEFT)
        self.add_fixed_in_frame_mobjects(plane1,plane2)
        self.play(FadeOut(plane1,plane2),run_time=0)
 


        self.set_camera_orientation(phi=80*DEGREES,theta=60*DEGREES,r=6)
        self.add_fixed_in_frame_mobjects(plane_title)
        self.add(plane, pc)
        self.play(Write(plane1[0]))
        self.add_fixed_orientation_mobjects(density)
        self.wait(2)
        self.next_slide()
        self.add(l)
        self.add_fixed_orientation_mobjects(dot,dot_lbl,l_lbl.shift(0.8*DOWN+0.2*RIGHT))
        self.play(Write(plane1[1]))    
        self.wait(2)
        self.next_slide()
        self.add(e2)
        self.add_fixed_orientation_mobjects(e2_lbl)
        self.play(Write(plane1[2]))
        self.wait()
        self.next_slide()
        self.add(cir2,cir1,gsurf)
        self.play(Write(plane1[3]))
        self.wait(2)
        self.play(Write(plane1[4]))
        self.next_slide()
        self.add(surf1,s1,e1,ds1)
        self.add_fixed_orientation_mobjects(s1_lbl,e1_lbl)
        self.wait(3)
        self.next_slide()
        self.add(surf2,s2,ds2)
        self.add_fixed_orientation_mobjects(s2_lbl)
        self.wait(3)
        self.next_slide()
        self.add(surf3,s3,e3)
        self.add_fixed_orientation_mobjects(s3_lbl,e3_lbl,ds3)
        self.wait(3)
        self.next_slide()
        self.play(FadeOut(plane1,plane_title))
        plane2.to_corner(UL)
        self.wait(2)
        for item in plane2[0]:
            self.play(Write(item))
            self.next_slide()

        sr=SurroundingRectangle(plane2[0][-1])
        self.add_fixed_in_frame_mobjects(sr)
        self.wait(2)
        self.play(Write(plane2[1]))
        self.wait()

class SphericalShell(Slide):
    def construct(self):
        # Title
        title = Tex(r"(3) Electric Filed Due to Uniformly Charged Spherical Shell:",font_size=35,color=GOLD).to_corner(UL,buff=0.05)
        self.play(Write(title))
        self.next_slide()

        # Crating Spherical Shell
        radius = 1.7
        shell =  Circle(radius=radius, color=GOLD, fill_opacity=0)
        
        # Adding + charges on the shell
        charges = VGroup()
        for i in range(0, 360,15):
            charges.add(Tex("$+$",font_size=30,color=RED).move_to((radius-0.15)*np.cos(i*DEGREES)*RIGHT+(radius-0.15)*np.sin(i*DEGREES)*UP))
        charge_lbl = Tex(r"$(\sigma /\ Q)$",font_size=35,color=RED).next_to(shell,DOWN, buff=-0.65)

        # Radius of shell
        R_line = Line(start=ORIGIN, end=radius*UP, color=YELLOW)
        R_line_lbl = Tex(r"$R$",font_size=35,color=YELLOW).next_to(R_line,LEFT,buff=0.1)
        centre_dot = Dot(point=ORIGIN,radius=0.05).set_color(YELLOW)
        centre_dot_lbl = Tex(r"$O$",font_size=35,color=YELLOW).next_to(centre_dot,DOWN,buff=0.1)


        Charged_shell = VGroup(shell, charges, R_line, R_line_lbl,charge_lbl,centre_dot,centre_dot_lbl)

        # Creating a point P outside the shell
        P_dot = Dot(point=(radius+1.3)*np.cos(45*DEGREES)*RIGHT+(radius+1.3)*np.sin(45*DEGREES)*UP,radius=0.05).set_color(RED).set_z_index(2)
        P_dot_lbl = Tex(r"$P$",font_size=35,color=RED).next_to(P_dot,RIGHT,buff=0.1)
        P_line = Line(start=ORIGIN, end=P_dot.get_center(), color=BLUE)
        P_line_lbl = Tex(r"$r$",font_size=35,color=BLUE).next_to(P_line.get_center(),DOWN,buff=0.1)
        P_group = VGroup(P_dot,P_dot_lbl,P_line,P_line_lbl)

        # Creating outer gaussian surface passing  through point P
        outer_surf = Circle(radius=radius+1.3, color=BLUE, fill_opacity=0)
        outer_surf_lbl_curv_arrow  = CurvedArrow(outer_surf.get_bottom(),outer_surf.get_bottom()+1*DOWN+0.5*RIGHT,tip_length = 0.15)
        outer_surf_lbl = Tex(r"Gaussian surface",font_size=30,color=WHITE).next_to(outer_surf_lbl_curv_arrow.get_end(),DOWN,buff=0.1)
        gauss_out = VGroup(outer_surf,outer_surf_lbl_curv_arrow,outer_surf_lbl)

        # Creating Electric Field vector at point P
        e_field = Arrow(P_dot.get_center(),P_dot.get_center()+P_line.get_unit_vector(),color=RED,buff=0)
        e_field_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).next_to(e_field.get_end(),RIGHT,buff=0.1)
        e_field_group = VGroup(e_field,e_field_lbl)

        # crating area vector ds on the gaussian surface near point P 
        ds = Arrow(P_dot.get_center(),P_dot.get_center()+0.5*P_line.get_unit_vector(),color=YELLOW, buff=0).shift(0.2*LEFT+0.15*UP)
        ds_lbl = Tex(r"$d\vec{S}$",font_size=35,color=YELLOW).next_to(ds.get_end(),UP,buff=0.1)
        ds_group = VGroup(ds,ds_lbl)

        # Creating a point P inside the shell
        P_dot_in = Dot(point=(radius-0.8)*np.cos(45*DEGREES)*RIGHT+(radius-0.8)*np.sin(45*DEGREES)*UP,radius=0.05).set_color(RED).set_z_index(2)
        P_dot_in_lbl = Tex(r"$P$",font_size=35,color=RED).next_to(P_dot_in,RIGHT,buff=0.1)
        P_line_in = Line(start=ORIGIN, end=P_dot_in.get_center(), color=BLUE)  
        P_line_in_lbl = Tex(r"$r$",font_size=35,color=BLUE).next_to(P_line_in.get_center(),DOWN,buff=0.1)
        P_group_in = VGroup(P_dot_in,P_dot_in_lbl,P_line_in,P_line_in_lbl)

        # Creating inner gaussian surface passing  through point P
        inner_surf = Circle(radius=radius-0.8, color=BLUE, fill_opacity=0)
        inner_surf_lbl_curv_arrow  = CurvedArrow(inner_surf.get_right(),inner_surf.get_right()+1.75*DOWN+1*RIGHT,tip_length = 0.15)
        inner_surf_lbl = Tex(r"Gaussian surface",font_size=30,color=WHITE).next_to(inner_surf_lbl_curv_arrow.get_end(),DOWN,buff=0.1)
        gauss_in = VGroup(inner_surf,inner_surf_lbl_curv_arrow,inner_surf_lbl)
        # Creating Electric Field vector at point P
        e_field_in = Arrow(P_dot_in.get_center(),P_dot_in.get_center()+0.5*P_line_in.get_unit_vector(),color=RED,buff=0)
        e_field_in_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).next_to(e_field_in.get_end(),RIGHT,buff=0.1)
        e_field_group_in = VGroup(e_field_in,e_field_in_lbl)
        # crating area vector ds on the gaussian surface near point P
        ds_in = Arrow(P_dot_in.get_center(),P_dot_in.get_center()+0.25*P_line_in.get_unit_vector(),color=YELLOW, buff=0).shift(0.2*LEFT+0.15*UP) 
        ds_in_lbl = Tex(r"$d\vec{S}$",font_size=35,color=YELLOW).next_to(ds_in.get_end(),UP,buff=0.1)
        ds_group_in = VGroup(ds_in,ds_in_lbl)

        # creating a point P at the surface of the shell
        P_dot_on = Dot(point=(radius+0.04)*np.cos(45*DEGREES)*RIGHT+(radius+0.04)*np.sin(45*DEGREES)*UP).set_color(RED).set_z_index(2)
        P_dot_on_lbl = Tex(r"$P$",font_size=35,color=RED).next_to(P_dot_on,RIGHT,buff=0.1)
        P_line_on = Line(start=ORIGIN, end=P_dot_on.get_center(), color=BLUE)
        P_line_on_lbl = Tex(r"$r=R$",font_size=35,color=BLUE).next_to(P_line_on.get_center(),DOWN,buff=0.1)
        P_group_on = VGroup(P_dot_on,P_dot_on_lbl,P_line_on,P_line_on_lbl)

        # Creating inner gaussian surface passing  through point P
        inner_surf_on = Circle(radius=radius+0.04, color=BLUE, fill_opacity=0)
        inner_surf_lbl_curv_arrow_on  = CurvedArrow(inner_surf_on.get_bottom(),inner_surf_on.get_bottom()+1*DOWN+0.5*RIGHT,tip_length = 0.15)  
        inner_surf_lbl_on = Tex(r"Gaussian surface",font_size=30,color=WHITE).next_to(inner_surf_lbl_curv_arrow_on.get_end(),DOWN,buff=0.1)
        gauss_in_on = VGroup(inner_surf_on,inner_surf_lbl_curv_arrow_on,inner_surf_lbl_on)

        # Creating Electric Field vector at point P
        e_field_on = Arrow(P_dot_on.get_center(),P_dot_on.get_center()+P_line_on.get_unit_vector(),color=RED,buff=0)
        e_field_on_lbl = Tex(r"$\vec{E}$",font_size=35,color=RED).next_to(e_field_on.get_end(),RIGHT,buff=0.1)
        e_field_group_on = VGroup(e_field_on,e_field_on_lbl)
        # crating area vector ds on the gaussian surface near point P
        ds_on = Arrow(P_dot_on.get_center(),P_dot_on.get_center()+0.5*P_line_on.get_unit_vector(),color=YELLOW, buff=0).shift(0.2*LEFT+0.15*UP)
        ds_on_lbl = Tex(r"$d\vec{S}$",font_size=35,color=YELLOW).next_to(ds_on.get_end(),UP,buff=0.1)
        ds_group_on = VGroup(ds_on,ds_on_lbl)

        # Grouping all elements 
        fig = VGroup(Charged_shell,P_group,gauss_out,e_field_group,ds_group,P_group_on,gauss_in_on,e_field_group_on,ds_group_on,P_group_in,gauss_in,e_field_group_in,ds_group_in).to_corner(UR,buff=0.1)

        # Derivation
        shell_gauss = ItemList(Item(r"Consider a uniformly charged spherical shell of radius $R$, charge $Q$ and surface charge density $(\sigma)$.",pw="7.5 cm"),
                          Item(r"We have to find electric field $(E)$ at point P  $(OP=r)$ using Gauss's Law.",pw="6 cm"),
                          buff=0.4).next_to(title,DOWN).to_corner(LEFT)  

        Outside_title = Tex(r"(i) When the point lies Outside the shell $(r>R)$",font_size=35,color=PINK).next_to(shell_gauss,DOWN).to_corner(LEFT,buff=0.05)   
        
        Outside  = ItemList(Item(r"The electric field will be same at each point of Gaussian surface and directed radially because of its spherical symmetry.",pw="6.5 cm"),
                            Item(r"From Gauss's Law, Total electric flux through the spherical Gaussian surface of radius $r$ is: ",pw="7 cm"),
                            Item(r"$\Phi=\oint \vec{E}\cdot d\vec{S}=\dfrac{q_{enc}}{\epsilon_0}$",pw="13 cm"),
                            buff=0.4).next_to(Outside_title,DOWN).to_corner(LEFT)
        
        Outside2 = ItemList(Item(r" & \int_{S} E ds\cos(0^\circ)=\dfrac{q_{enc}}{\epsilon_0}\\ ",r"&  E \int_{S} ds  =\dfrac{q_{enc}}{\epsilon_0}\\",r"& E\times 4\pi r^2  =\dfrac{Q}{\epsilon_0} \quad (\because q_{enc}=Q)\\",r" & E  = \dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r^2}\\",r" & E  = \dfrac{\sigma R^2}{\epsilon_0 r^2} \quad (\because Q = \sigma \times 4\pi R^2)",math=True,dot=False),
                            Item(r"Thus for points outside the shell the electric field is as if the entire charge of the shell is concentrated at the centre O.",pw="7 cm"),
                            buff=0.4).next_to(Outside_title,DOWN).to_corner(LEFT)

        At_surface_title = Tex(r"(ii) When the point lies on the surface of the shell $(r=R)$",font_size=35,color=GREEN).to_corner(UL,buff=0.05)
        Surface = ItemList(Item(r"$E = \dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{R^2}$",r"$ = \dfrac{\sigma}{\epsilon_0}\quad $",r"$ \left(\sigma=\dfrac{Q}{4\pi R^2}\right)$", dot=False,pw="6.5 cm"),
                            buff=0.4).next_to(At_surface_title,DOWN).to_corner(LEFT)
        
        Inside_title = Tex(r"(iii) When the point lies Inside the shell $(r<R)$",font_size=35,color=PINK).next_to(Surface,DOWN).to_edge(LEFT,buff=0.05)  
        
        Inside  = ItemList(Item(r"In this case the charge enclosed by the Gaussian surface, $q_{enc}=0$",pw="6.5 cm"),
                           Item(r" & \int_{S} E ds\cos(0^\circ)=\dfrac{q_{enc}}{\epsilon_0}\\ ",r"&  E \int_{S} ds  =\dfrac{0}{\epsilon_0} \quad (\because q_{enc}=0)\\",r"& E\times 4\pi r^2  =\dfrac{0}{\epsilon_0} \\",r" & E  = 0 \quad (\text{for  } r<R )",math=True,dot=False),
                            buff=0.4).next_to(Inside_title,DOWN).to_corner(LEFT)
        
        sr3 = SurroundingRectangle(Surface[0][0:2])
        sr4 = SurroundingRectangle(Inside[1][-1])
        
        # Graph of E vs r
        axes_2 = (Axes(
        x_range=[0, 8, 2],
        y_range=[0, 19, 2],
        y_length=5,
        x_length=8,
        axis_config={'tip_shape': StealthTip,"tip_width":0.08,"tip_height":0.15},
        y_axis_config={"include_ticks": False}
      ).set_color(GREEN_C))
        axes_labels = axes_2.get_axis_labels(x_label=Tex(r"$r$",font_size=30), y_label=Tex(r"$E(r)$",font_size=30))

        func1 = axes_2.plot(lambda x: 0, x_range=[0, 2], color=BLUE)
        func2 = axes_2.plot(lambda x: 70/(x*x), x_range=[2, 7], color=BLUE)
        lines = VGroup(axes_2.get_lines_to_point(axes_2.c2p(2,70/4),color=RED),
                       axes_2.get_lines_to_point(axes_2.c2p(4,70/16),color=RED),
                       axes_2.get_lines_to_point(axes_2.c2p(6,70/36),color=RED),
                       Dot(axes_2.c2p(2,70/4), color=PINK),
                       Dot(axes_2.c2p(4,70/16), color=GOLD),
                       Dot(axes_2.c2p(6,70/36), color=ORANGE),)
        axes_2.get_x_axis().add_labels({0:"O",2:"R",4:"2R",6:"3R",8:"4R"},font_size=25)
        axes_2.get_y_axis().add_labels({70/4:"$E_0$",70/16:"$E_0/4$",70/36:"$E_0/9$"},font_size=25)
        c1 = CurvedArrow(start_point=func1.get_center(),end_point=func1.get_center()+0.8*UP+0.4*RIGHT,tip_length=0.1)
        V1 = Tex(r"$E=0\ (r<R)$",font_size=25).next_to(c1.get_end(),UP,buff=0.05)
        c2 = CurvedArrow(start_point=axes_2.c2p(3,70/9),end_point=axes_2.c2p(3,70/9)+0.8*UP+0.4*RIGHT,tip_length=0.1)
        V2 = Tex(r"$E=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r^2}\ (r>R)$",font_size=25).next_to(c2.get_end(),UP,buff=0.05).shift(0.5*RIGHT)
        c3 = CurvedArrow(start_point=axes_2.c2p(2,70/4),end_point=axes_2.c2p(2,70/4)+0.8*UP+0.4*RIGHT,tip_length=0.1)
        V3 = Tex(r"$E_0=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{R^2}\ (r=R)$",font_size=25).next_to(c3.get_end(),UP,buff=0.05)
        label = Tex("Graph of Electric field $(E)$ versus $r$ for spherical shell. ",font_size=30,color=GOLD).next_to(axes_2,DOWN)


        self.play(Create(Charged_shell), Write(shell_gauss[0]))
        self.wait()
        self.next_slide()
        self.play(Create(P_group), Write(shell_gauss[1]))
        self.wait()
        self.next_slide()
        self.play(Write(Outside_title))
        self.wait()
        self.next_slide()
        self.play(Create(gauss_out), Create(e_field_group), Create(ds_group))
        self.wait(2)
        self.play(Write(Outside[0]))
        self.next_slide()
        self.play(Write(Outside[1]))
        self.wait()
        self.next_slide()
        self.play(Write(Outside[2]))
        self.wait()
        self.next_slide()
        self.play(FadeOut(title,shell_gauss, Outside))
        self.wait()
        self.play(Outside_title.animate().to_corner(UL, buff=0.05))
        Outside2.next_to(Outside_title,DOWN).to_corner(LEFT,buff=1)
        sr1 = SurroundingRectangle(Outside2[0][-2])
        sr2 = SurroundingRectangle(Outside2[0][-1])
        self.wait(2)
        for item in Outside2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        self.play(Write(sr1),Write(sr2))
        self.wait()
        self.next_slide()
        self.play(ReplacementTransform(Outside_title, At_surface_title))
        self.wait(2)
        self.play(ReplacementTransform(VGroup(P_group,gauss_out,e_field_group,ds_group),VGroup(P_group_on,gauss_in_on,e_field_group_on,ds_group_on)))
        self.wait(2)
        self.next_slide()
        self.play(FadeOut(Outside2,sr1,sr2))
        self.wait()
        for item in Surface:
            self.play(Write(item))
            self.next_slide()
        self.play(Write(sr3))
        self.wait(2)
        self.next_slide()
        R_line_lbl.shift(0.2*UP)
        self.next_slide()
        self.play(Write(Inside_title))
        self.wait(2)    
        self.play(ReplacementTransform(VGroup(P_group_on,gauss_in_on,e_field_group_on,ds_group_on),VGroup(P_group_in,gauss_in,e_field_group_in,ds_group_in)))
        self.wait(2)
        self.next_slide()
        for item in Inside:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        
        self.play(Write(sr4))
        self.wait(2)
        self.next_slide()
        self.play(FadeOut(Inside,sr4,Surface,P_group_in,gauss_in,e_field_group_in,ds_group_in,Charged_shell,sr4,Inside_title,At_surface_title,Surface,sr3))
        self.wait(2)
        self.play(Create(axes_2),Create(axes_labels))
        self.wait()
        self.next_slide()
        self.play(Create(VGroup(func1,c1,V1)))
        self.wait()
        self.next_slide()
        self.play(Create(VGroup(func2,c2,V2,c3,V3)))
        self.wait()
        self.next_slide()
        self.play(Create(lines),Create(label))
        self.wait(2)

class Ex63(Slide):
    def construct(self):

        ex_title = Tex(r"Example 51 :", r" An early model for an atom considered it to have a positively charged point nucleus of charge Ze, surrounded by a uniform density of negative charge up to a radius $R$. The atom as a whole is neutral. For this model, what is the electric field at a distance $r$ from the nucleus?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)

        out_0_img = ImageMobject("out0.png").next_to(ex_title,DOWN,buff=0).to_corner(RIGHT,buff=0.1).shift(0.4*UP)
        out_1_img = ImageMobject("out1.png").next_to(ex_title,DOWN,buff=0).to_corner(RIGHT,buff=0.1).shift(0.4*UP)
        out_2_img = ImageMobject("out2.png").next_to(ex_title,DOWN,buff=0).to_corner(RIGHT,buff=0.1).shift(0.4*UP)
        in_0_img = ImageMobject("ins0.png").next_to(ex_title,DOWN).to_corner(RIGHT)
        in_1_img = ImageMobject("ins1.png").next_to(ex_title,DOWN).to_corner(RIGHT)
        in_2_img = ImageMobject("ins2.png").next_to(ex_title,DOWN).to_corner(RIGHT)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(FadeIn(out_0_img))
        self.next_slide()

        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

        sol_1 = ItemList(Item(r"(1) ",r" Filed Outside the Atom $(r>R)$",pw="6.5 cm"),
                         Item(r"Using Gauss's Law : $\oint_{S} \vec{E}\cdot d\vec{S}=\dfrac{q_{enc}}{\epsilon_0}$" ,pw="6.5 cm"),
                         Item(r"$E\oint_S ds = \dfrac{+Ze-Ze}{\epsilon_0}$",pw="6.5 cm",dot=False),
                         Item(r"$E \times 4\pi r^2 = \dfrac{0}{\epsilon_0}$",pw="6.5 cm",dot=False),
                         Item(r"$E_{out} = 0$",pw="6.5 cm",dot=False),
                         buff=MED_SMALL_BUFF).next_to(sol_label,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        sol_2 = ItemList(Item(r"(2) ",r" Filed Inside the Atom $(r<R)$",pw="6.5 cm"),
                         Item(r"Using Gauss's Law : $\oint_{S} \vec{E}\cdot d\vec{S}=\dfrac{q_{enc}}{\epsilon_0}$" ,pw="6.5 cm"),
                         Item(r"$E\oint_S ds = \dfrac{+Ze+q_{-enc}}{\epsilon_0}$",pw="6.5 cm",dot=False),
                         Item(r"$E \times 4\pi r^2 = \dfrac{+Ze+q_{-enc}}{\epsilon_0}$",pw="6.5 cm",dot=False),
                         Item(r"$q_{-enc}=\rho\times $ Volume enclosed",pw="6.5 cm",dot=False),
                         Item(r"$q_{-enc}=\dfrac{-Ze}{\dfrac{4}{3}\pi R^3}\times \dfrac{4}{3}\pi r^3  $",pw="6.5 cm",dot=False),
                         buff=MED_SMALL_BUFF).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT,buff=0.1)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(sol_1,0.5*RIGHT).align_to(sol_1,UP)

        sol_3 = ItemList(Item(r"$q_{-enc}=-Ze \dfrac{r^3}{R^3}  $",pw="6.5 cm",dot=False),
                         Item(r"$E \times 4\pi r^2 = \dfrac{+Ze+-Ze \dfrac{r^3}{R^3}}{\epsilon_0}$",pw="6.5 cm",dot=False),
                         Item(r"$E = \dfrac{Ze \left[1-\dfrac{r^3}{R^3}\right]}{4\pi \epsilon_0\times r^2}$",pw="6.5 cm",dot=False),
                         Item(r"$E =\dfrac{Ze}{4\pi\epsilon_0}\times  \left[\dfrac{1}{ r^2}-\dfrac{r}{R^3}\right]$",pw="6.5 cm",dot=False),
                         buff=MED_SMALL_BUFF).next_to(line,RIGHT).align_to(sol_2,UP)
        
        
        
        
        self.next_slide()
        sr = SurroundingRectangle(sol_1[4])
        sr2 = SurroundingRectangle(sol_3[-1])
        anm = [Write(sol_1[0]),FadeIn(out_1_img),Write(sol_1[1]),FadeIn(out_2_img),Write(sol_1[2]),Write(sol_1[3]),Write(VGroup(sol_1[4],sr))]
        anm2 = [Write(sol_2[0]),FadeIn(in_1_img),Write(sol_2[1]),FadeIn(in_2_img),Write(sol_2[2]),Write(sol_2[3]),Write(sol_2[4]),Write(VGroup(sol_2[5]))]

        for item in anm:
            self.play(item)
            self.next_slide()

        self.play(FadeOut(out_0_img,out_1_img,out_2_img,sol_1,sr),run_time=0)
        self.play(FadeIn(in_0_img))

        for item in anm2:
            self.play(item)
            self.next_slide()

        self.play(FadeOut(in_0_img,in_1_img,in_2_img),run_time=0)
        self.play(Write(line))
        for item in sol_3:
            self.play(Write(item))
            self.next_slide()
        
        self.play(Write(sr2))
        self.wait(2)

class Ex64(Slide):
    def construct(self):

        ex_title = Tex(r"Example 52 :", r" A conducting sphere of radius 10 cm has an unknown charge. If the electric field 20 cm from the centre of the sphere is $1.5 \times 10^3$ N/C and points radially inward, what is the net charge on the sphere?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class Ex65(Slide):
    def construct(self):

        ex_title = Tex(r"Example 53 :", r"A uniformly charged conducting sphere of 2.4 m diameter has a surface charge density of 80.0 $\mu C m^{-2}$. (a) Find the charge on the sphere. (b) What is the total electric flux leaving the surface of the sphere?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class Ex66(Slide):
    def construct(self):

        ex_title = Tex(r"Example 54 :", r"An infinite line charge produces a field of $9 \times 10^4$ N/C at a distance of 2 cm. Calculate the linear charge density.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class Ex67(Slide):
    def construct(self):

        ex_title = Tex(r"Example 55 :", r"Two large, thin metal plates are parallel and close to each other. On their inner faces, the plates have surface charge densities of opposite signs and of magnitude $17.0 \times 10^{-22}\ C/m^22$. What is $E$: (a) in the outer region of the first plate, (b) in the outer region of the second plate, and (c) between the plates?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class Ex68(Slide):
    def construct(self):

        ex_title = Tex(r"Example 56 :", r" An electron is rotating around an infinite positive linear charge in a circle of radius 0.1 m, if the linear charge density is $1\ \mu$C/m, then the velocity of electron in m/s will be ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) $0.562\times 10^{7}$ ',font_size=35),Tex(r'(b) $5.62\times 10^{7}$  ',font_size=35),Tex(r'(c) $562\times 10^{7}$ C  ',font_size=35),Tex(r'(d) $0.0562\times 10^7$  ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[1]))

class Ex69(Slide):
    def construct(self):
        ex_title = Tex(r"Example 57 :", r" Two isolate metallic spheres of radii 2 cm and 4 cm are given equal charge, then the ratio of charge density on the surface of the spheres will be ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) $4:1$ ',font_size=35),Tex(r'(b) $1:2$   ',font_size=35),Tex(r'(c) $1:4$ C  ',font_size=35),Tex(r'(d) $8:1$  ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[0]))


