import numpy as np
import sympy as sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, Line
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

transformations = standard_transformations + (implicit_multiplication_application,)

class GraphWidget(RelativeLayout):
    def __init__(self, expr, **kwargs):
        super().__init__(**kwargs)
        self.expr = expr
        self.bind(size=self.draw_graph, pos=self.draw_graph)
        
    def draw_graph(self, *args):
        self.canvas.clear()
        with self.canvas:
            # ১. ব্যাকগ্রাউন্ড কালার (লোকাল কোঅর্ডিনেট ০, ০ থেকে শুরু)
            Color(0.05, 0.05, 0.05, 1)
            Rectangle(pos=(0, 0), size=self.size)
            
            # ২. রিলেটিভ লেআউটের কেন্দ্র নির্ধারণ
            Color(0.3, 0.3, 0.3, 1)
            cx, cy = self.width / 2, self.height / 2
            
            # X এবং Y অক্ষ রেখা অঙ্কন
            Line(points=[0, cy, self.width, cy], width=1.5)  # X Axis
            Line(points=[cx, 0, cx, self.height], width=1.5) # Y Axis
            
            # ৩. গ্রাফের পয়েন্ট ক্যালকুলেশন (NumPy ও SymPy এর মাধ্যমে)
            Color(0, 0.7, 1, 1)
            points = []
            x_vals = np.linspace(-10, 10, 200)
            scale_x = self.width / 20
            scale_y = self.height / 20
            x_sym = sp.Symbol('x')
            
            for xv in x_vals:
                try:
                    yv = float(self.expr.subs(x_sym, xv))
                    screen_x = cx + xv * scale_x
                    screen_y = cy + yv * scale_y
                    
                    # পয়েন্টটি উইজেটের সীমানার ভেতরে থাকলে যুক্ত হবে
                    if 0 <= screen_y <= self.height:
                        points.extend([screen_x, screen_y])
                except:
                    pass
                    
            if len(points) >= 4:
                Line(points=points, width=2.5)

def solve_mod(text):
    raw = text.lower().strip()
    if raw.startswith("plot"):
        try:
            eq_body = raw.replace("plot", "").strip()
            # ^ চিহ্নের পরিবর্তে পাইথনের পাওয়ার চিহ্ন ** ব্যবহার নিশ্চিত করা
            expr = parse_expr(eq_body.replace("^", "**"), transformations=transformations)
            
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            graph_view = GraphWidget(expr=expr)
            close_btn = Button(text="CLOSE GRAPH", size_hint_y=0.15, background_color=(0.8, 0.2, 0.2, 1), bold=True)
            
            content.add_widget(graph_view)
            content.add_widget(close_btn)
            
            popup = Popup(title=f"Graph: y = {eq_body}", content=content, size_hint=(0.9, 0.75))
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
            
            return f"Successfully plotted graph for: y = {eq_body}"
        except:
            return "Failed to plot graph. Make sure it uses variable 'x' (e.g., plot x**2)."
    return None
