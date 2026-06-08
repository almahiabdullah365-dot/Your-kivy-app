import re
import math
import ast
import random
import datetime
import numpy as np    # NumPy লাইব্রেরি সম্পূর্ণ সুরক্ষিত
import sympy as sp    # SymPy লাইব্রেরি সক্রিয় রাখা হয়েছে

# 👤 ডাইনামিক ইউজার নেম স্টেট
USER_NAME = "User"

# 📚 অ্যালজেব্রা ডাটাবেস
ALGEBRA_DATA = [
    ("square minus", {"formula": "(a - b)² = a² - 2ab + b²", "note": "Square subtraction formula"}),
    ("square", {"formula": "(a + b)² = a² + 2ab + b²", "note": "Standard square formula"}),
    ("cube minus", {"formula": "(a - b)³ = a³ - 3a²b - 3ab² - b³", "note": "Cube subtraction formula"}),
    ("cube", {"formula": "(a + b)³ = a³ + 3a²b + 3ab² + b³", "note": "Standard cube formula"}),
    ("simplify", {"formula": "a² - b² = (a + b)(a - b)", "note": "Difference of two squares"}),
    ("corollary 1", {"formula": "a² + b² = (a + b)² - 2ab", "note": "Used for finding values"}),
    ("4ab", {"formula": "4ab = (a + b)² - (a - b)²", "note": "4ab identity"}),
]

# সংরক্ষিত ম্যাথ কিওয়ার্ডের তালিকা
MATH_KEYWORDS = [
    "sin", "cos", "tan", "matrix", "[", "]", "convert", "solve", "plot", 
    "quadratic", "ohm", "power", "interest", "speed", "weight", "area", 
    "vector", "force", "suvat", "motion", "square", "cube", "simplify", "log",
    "pythagoras", "celsius", "fahrenheit", "km", "miles", "kilometer", "kilometers", "mile",
    "f=ma", "v=u+at", "diff", "integrate", "stats", "probability", "prob", "bin", "hex", "logic", "gas", "ph"
]

# মোটিভেশনাল মেসেজের তালিকা
MOTIVATIONAL_MESSAGES = [
    "Back at it 🚀",
    "Ready to conquer math? 🔥",
    "Let's solve some problems! 💻",
    "Welcome back! 🛠️",
    "Time for some calculations! 📊",
    "Let's do this! 💪"
]

def get_dynamic_welcome_message():
    """ডিভাইসের সময় এবং ইউজারের নাম অনুযায়ী ডাইনামিক গ্রিটিংস তৈরি করার ফাংশন"""
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        time_greeting = "Good morning ☀️"
    elif 12 <= current_hour < 17:
        time_greeting = "Good afternoon 🌤️"
    elif 17 <= current_hour < 21:
        time_greeting = "Good evening 🌆"
    else:
        time_greeting = "Good night 🌙"
        
    random_motivation = random.choice(MOTIVATIONAL_MESSAGES)
    return f"{time_greeting}, {USER_NAME}! {random_motivation}"

def parse_text_number(s):
    """ইংরেজি টেক্সট শব্দকে সংখ্যায় রূপান্তর করার হেল্পার ফাংশন"""
    word_to_num = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
        "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
        "eighty": 80, "ninety": 90
    }
    match = re.search(r'(\d+\.?\d*)', s)
    if match:
        return float(match.group(1))
    
    words = s.split()
    total = 0
    found = False
    for w in words:
        w = w.strip(",.-")
        if w in word_to_num:
            total += word_to_num[w]
            found = True
        elif w == "hundred":
            if total == 0: total = 100
            else: total *= 100
            found = True
    return float(total) if found else None

def safe_boolean_eval(expr_str):
    """eval() এর বিকল্প হিসেবে সম্পূর্ণ সুরক্ষিত কাস্টম AST লজিক ইভালুয়েটর"""
    try:
        node = ast.parse(expr_str, mode='eval').body
        def _walk(n):
            if isinstance(n, ast.Constant): return bool(n.value)
            elif isinstance(n, ast.Num): return bool(n.n)
            elif isinstance(n, ast.BinOp):
                left = _walk(n.left)
                right = _walk(n.right)
                if isinstance(n.op, ast.BitAnd): return left and right
                if isinstance(n.op, ast.BitOr): return left or right
            elif isinstance(n, ast.UnaryOp):
                operand = _walk(n.operand)
                if isinstance(n.op, ast.Invert): return not operand
            raise ValueError("Unsafe operation")
        return 1 if _walk(node) else 0
    except:
        return None

def solve_mod(text):
    global USER_NAME
    raw = text.lower().strip()
    
    # 👤 ১. নাম পার্সিং ও পরিবর্তন লজিক
    if raw.startswith("my name is ") or raw.startswith("change name to "):
        parts = text.split()
        if len(parts) >= 4:
            USER_NAME = " ".join(parts[3:])
        else:
            USER_NAME = parts[-1]
        return f"✨ Name updated successfully! Hello, {USER_NAME}."
    
    # 💬 চ্যাট ও গ্রিটিংস লজিক
    if raw in ["hi", "hello", "hey", "yo", "greetings", "hello bot", "start", "good morning", "good afternoon", "good evening", "good night"]:
        prefix = get_dynamic_welcome_message()
        return f"✨ {prefix} ✨\nHello {USER_NAME}! How can I help you today? Type 'guide' to see what I can calculate!"
    if raw in ["how are you", "how r u", "how are you doing", "how's it going"]:
        return f"I am doing great, thank you! Ready to solve some math, physics, or electronics problems. What about you, {USER_NAME}?"
    if raw in ["who are you", "what is your name", "your name"]:
        return "I am MathBot, your smart assistant for science, mathematics, and engineering calculations."
    if raw in ["thank you", "thanks", "ty", "thank u"]:
        return f"You're welcome, {USER_NAME}! I'm always happy to help you."
    if raw in ["bye", "goodbye", "see you"]:
        return f"Goodbye, {USER_NAME}! Have a wonderful day ahead."
    if raw in ["ok", "okay", "fine", "cool", "nice"]:
        return "Awesome! Let me know if you want to calculate something."

    # 📖 মাস্টার ইউজার গাইড মেনু (১১-১৯ আইটেম সম্পূর্ণভাবে যুক্ত করা হয়েছে)
    if raw in ["guide", "help", "menu"]:
        return (
            "--- MATHBOT APP - MASTER USER GUIDE ---\n"
            "----------------------------------------\n"
            "0. Set/Change Name: my name is Abdullah OR change name to Alex\n"
            "1. Algebra Formula: square OR simplify OR log product\n"
            "2. Symbolic Solver: solve x^2 - 9 = 0\n"
            "3. Graph Plotter: plot x**2\n"
            "4. Matrix Handler: [[1,2],[3,4]] (Supports Rank, Trace, Eig, Inverse)\n"
            "5. Physics Force & SUVAT: force m=10 a=5 OR suvat u=0 a=2 t=10\n"
            "6. Speed: speed d=200 t=8 OR speed 90 kmh\n"
            "7. Weight: weight m=75\n"
            "8. Area: area l=20 w=12\n"
            "9. Electronics: ohm v=12 r=6 OR power v=5 i=2\n"
            "10. Smart Converter: convert 37celsius OR ninety miles to km\n"
            "11. Geometry & Trig: pythagoras a=3 b=4 OR sin 45\n"
            "12. Vector Math: vector mag 3 4 OR vector dot 1 2 3 4\n"
            "13. Interest Calc: interest p=10000 r=5 t=3 OR interest compound p=5000 r=6 t=2\n"
            "14. Quadratic Equation: quadratic a=1 b=-5 c=6\n"
            "15. Calculus Engine: diff x**3 + 2*x OR integrate sin(x)\n"
            "16. Stats & Probability: stats 10, 20, 30 OR prob n=5 r=2\n"
            "17. Digital Logic & Bases: bin 255 OR hex 1024 OR logic 1 AND 0\n"
            "18. Chemistry Solver: gas p=2 v=10 t=300 OR ph h=0.01\n"
            "19. Entity Counter: 5 apples 10 bananas\n"
            "----------------------------------------\n"
            "Tip: Type 'guide' anytime to see this menu."
        )

    # 📌 অ্যালজেব্রা সূত্র লজিক
    for name, data in ALGEBRA_DATA:
        if name in raw:
            return f"📌 ALGEBRA: {name.upper()}\nFormula: {data['formula']}\nNote: {data['note']}"
    if "log" in raw and ("*" in raw or "product" in raw):
        return "📌 LOG PRODUCT RULE\nFormula: log(m * n) = log(m) + log(n)\nNote: log multiplication rule"

    # 📊 SymPy সিম্বলিক ইকুয়েশন সলভার
    if raw.startswith("solve "):
        eq_text = raw[6:].strip().replace("^", "**")
        if "=" in eq_text: lhs, rhs = eq_text.split("=", 1)
        else: lhs, rhs = eq_text, "0"
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(f"({lhs}) - ({rhs})")
            solutions = sp.solve(expr, x)
            return f"📊 [SYMBOLIC EQUATION SOLVER]\n* Equation: {eq_text}\n-> Solutions for x: {solutions}"
        except Exception as e: return f"ERROR: SymPy solver failed! Details: {e}"

    # 📈 গ্রাফ প্লটার ইঞ্জিন
    if raw.startswith("plot "):
        expr_text = raw[5:].strip().replace("^", "**")
        try:
            x_sym = sp.Symbol('x')
            expr = sp.sympify(expr_text)
            f_lamb = sp.lambdify(x_sym, expr, "numpy")
            x_vals = np.linspace(-4, 4, 9)
            y_vals = f_lamb(x_vals)
            graph_str = f"📈 [TEXT-BASED GRAPH PLOT: {expr_text}]\nCoordinates Table:\n"
            for xv, yv in zip(x_vals, y_vals): graph_str += f"  x: {xv:4.1f} ➔ y: {yv:6.2f}\n"
            graph_str += "\nVisual Chart (Axis Center = 0):\n"
            for xv, yv in zip(x_vals, y_vals):
                if np.isnan(yv) or not np.isfinite(yv):
                    graph_str += f" {xv:4.1f} | Error\n"; continue
                val_int = int(max(-15, min(15, yv)))
                line = " " * 15 + "|" + "*" * val_int if val_int > 0 else (" " * (15 + val_int) + "*" * abs(val_int) + "|" if val_int < 0 else " " * 15 + "|")
                graph_str += f" {xv:4.1f} |{line}\n"
            return graph_str
        except Exception as e: return f"ERROR: Plotting failed! Details: {e}"

    # 🧮 ম্যাট্রিক্স ইঞ্জিন
    if raw.startswith("matrix") or ("[[" in raw and "]]" in raw):
        try:
            matrix_match = re.search(r'(\[\[.*?\]\])', raw)
            if matrix_match:
                matrix_str = matrix_match.group(1)
                matrix_data = ast.literal_eval(matrix_str)
                arr = np.array(matrix_data); shape = arr.shape
                trace_val = np.trace(arr); rank_val = np.linalg.matrix_rank(arr)
                res = f"📊 [MATRIX ANALYSIS]\n📏 Shape: {shape}\n📈 Rank: {rank_val}\n🔄 Trace: {trace_val}\n"
                if len(shape) == 2 and shape[0] == shape[1]:
                    det = round(np.linalg.det(arr), 3); res += f"💎 Determinant: {det}\n"
                    try:
                        eigenvals = np.linalg.eigvals(arr)
                        res += f"🧬 Eigenvalues: [{', '.join([f'{val:.2f}' for val in eigenvals])}]\n"
                    except: res += f"🧬 Eigenvalues: Error\n"
                    if det != 0: res += f"🔄 Inverse Matrix:\n{np.linalg.inv(arr)}\n"
                    else: res += f"🔄 Inverse: Not Possible (Singular Matrix)\n"
                else: res += f"⚠️ Note: Square matrix required for Det, Eigen, and Inverse.\n"
                return res
            return "ভুল ম্যাট্রিক্স ফরম্যাট! [[1,2],[3,4]] এভাবে লিখুন।"
        except: return "ভুল ম্যাট্রিক্স ফরম্যাট! [[1,2],[3,4]] এভাবে লিখুন।"

    # 🌌 ফিজিক্স ফোর্স ক্যালকুলেশন
    if raw.startswith("physics") or raw.startswith("force") or "suvat" in raw or raw.startswith("motion") or "f=ma" in raw or "v=u+at" in raw:
        f_match = re.search(r'\bf=(-?\d+\.?\d*)', raw); m_match = re.search(r'\bm=(\d+\.?\d*)', raw); a_match = re.search(r'\ba=(-?\d+\.?\d*)', raw)
        u_match = re.search(r'\bu=(-?\d+\.?\d*)', raw); v_match = re.search(r'\bv=(-?\d+\.?\d*)', raw); t_match = re.search(r'\bt=(\d+\.?\d*)', raw); s_match = re.search(r'\bs=(-?\d+\.?\d*)', raw)
        
        if raw.startswith("force") or "f=ma" in raw or (m_match and a_match and not (u_match or v_match or t_match or s_match)):
            if m_match and a_match: 
                return f"🌌 [PHYSICS - FORCE CALCULATION]\n* Mass (m): {m_match.group(1)} kg\n* Acceleration (a): {a_match.group(1)} m/s²\n-> Force (F = ma): {float(m_match.group(1))*float(a_match.group(1)):.2f} N"
            elif f_match and a_match: 
                a_val = float(a_match.group(1))
                if a_val == 0: return "⚠️ ERROR: Acceleration cannot be zero when calculating mass!"
                return f"🌌 [PHYSICS - FORCE CALCULATION]\n* Force (F): {f_match.group(1)} N\n* Acceleration (a): {a_match.group(1)} m/s²\n-> Mass (m = F/a): {float(f_match.group(1))/a_val:.2f} kg"
            elif f_match and m_match: 
                m_val = float(m_match.group(1))
                if m_val == 0: return "⚠️ ERROR: Mass cannot be zero!"
                return f"🌌 [PHYSICS - FORCE CALCULATION]\n* Force (F): {f_match.group(1)} N\n* Mass (m): {m_match.group(1)} kg\n-> Acceleration (a = F/m): {float(f_match.group(1))/m_val:.2f} m/s²"
            return "Format error! Use: force m=10 a=5"
        
        # 🏃 SUVAT COMPLETENESS
        suvat_vals = {}
        if u_match: suvat_vals['u'] = float(u_match.group(1))
        if v_match: suvat_vals['v'] = float(v_match.group(1))
        if a_match: suvat_vals['a'] = float(a_match.group(1))
        if t_match: suvat_vals['t'] = float(t_match.group(1))
        if s_match: suvat_vals['s'] = float(s_match.group(1))
        
        if len(suvat_vals) >= 3:
            res = "🏃 [PHYSICS - SUVAT MOTION SOLVER]\nGiven Parameters:\n"
            for k, val in suvat_vals.items(): res += f"  * {k} = {val}\n"
            
            # Case 1: u, a, t
            if 'u' in suvat_vals and 'a' in suvat_vals and 't' in suvat_vals:
                u, a, t = suvat_vals['u'], suvat_vals['a'], suvat_vals['t']
                res += f"Calculated Outputs:\n  -> Final Velocity (v = u + at): {u + a * t:.2f} m/s\n  -> Displacement (s = ut + 0.5at²): {u * t + 0.5 * a * (t**2):.2f}"
            # Case 2: u, v, t
            elif 'u' in suvat_vals and 'v' in suvat_vals and 't' in suvat_vals:
                u, v, t = suvat_vals['u'], suvat_vals['v'], suvat_vals['t']
                if t == 0: return "⚠️ ERROR: Time cannot be zero!"
                res += f"Calculated Outputs:\n  -> Acceleration (a = (v-u)/t): {(v - u) / t:.2f} m/s²\n  -> Displacement (s = 0.5(u+v)t): {0.5 * (u + v) * t:.2f}"
            # Case 3: u, a, s
            elif 'u' in suvat_vals and 'a' in suvat_vals and 's' in suvat_vals:
                u, a, s = suvat_vals['u'], suvat_vals['a'], suvat_vals['s']
                v_squared = (u**2) + (2 * a * s)
                if v_squared < 0: return "⚠️ ERROR: Mathematically impossible motion (v² < 0)!"
                v = math.sqrt(v_squared)
                t = ((v - u) / a) if a != 0 else (s / u if u != 0 else 0)
                res += f"Calculated Outputs:\n  -> Final Velocity (v = √(u²+2as)): ±{v:.2f} m/s\n  -> Time Taken (t): {t:.2f}s"
            # Case 4: v, a, t
            elif 'v' in suvat_vals and 'a' in suvat_vals and 't' in suvat_vals:
                v, a, t = suvat_vals['v'], suvat_vals['a'], suvat_vals['t']
                u = v - (a * t)
                s = (v * t) - (0.5 * a * (t**2))
                res += f"Calculated Outputs:\n  -> Initial Velocity (u = v - at): {u:.2f} m/s\n  -> Displacement (s = vt - 0.5at²): {s:.2f}"
            # Case 5: u, v, s
            elif 'u' in suvat_vals and 'v' in suvat_vals and 's' in suvat_vals:
                u, v, s = suvat_vals['u'], suvat_vals['v'], suvat_vals['s']
                if s == 0: return "⚠️ ERROR: Displacement cannot be zero for calculating acceleration!"
                if (u + v) == 0: return "⚠️ ERROR: Sum of velocities is zero, cannot calculate time!"
                a = ((v**2) - (u**2)) / (2 * s)
                t = (2 * s) / (u + v)
                res += f"Calculated Outputs:\n  -> Acceleration (a = (v²-u²)/2s): {a:.2f} m/s²\n  -> Time Taken (t = 2s/(u+v)): {t:.2f}s"
            else:
                res += "-> Provide valid sets: (u,a,t), (u,v,t), (u,a,s), (v,a,t), or (u,v,s)."
            return res
        return "Format error! Give at least 3 SUVAT variables."

    # 🏃 SPEED LOGIC
    if raw.startswith("speed"):
        d_match = re.search(r'd=(\d+\.?\d*)', raw); t_match = re.search(r't=(\d+\.?\d*)', raw)
        if d_match and t_match: 
            t_val = float(t_match.group(1))
            if t_val == 0: return "⚠️ ERROR: Time cannot be zero!"
            return f"[SPEED CALCULATION]\n* Distance (d): {d_match.group(1)}\n* Time (t): {t_match.group(1)}\n-> Speed (v = d/t): {float(d_match.group(1))/t_val:.2f} m/s"
        kmh_match = re.search(r'(\d+\.?\d*)\s*kmh', raw)
        if kmh_match: return f"[SPEED CONVERSION]\n* {kmh_match.group(1)} km/h = {float(kmh_match.group(1)) / 3.6:.2f} m/s"
        return "Format error!"

    # ⚖️ WEIGHT LOGIC
    if raw.startswith("weight"):
        m_match = re.search(r'm=(\d+\.?\d*)', raw)
        if m_match: return f"[WEIGHT CALCULATION]\n* Mass (m): {m_match.group(1)}\n* Gravity (g): 9.8\n-> Weight (W = mg): {float(m_match.group(1)) * 9.8:.2f} N"
        return "Format error!"

    # 📐 AREA LOGIC
    if raw.startswith("area"):
        l_match = re.search(r'l=(\d+\.?\d*)', raw); w_match = re.search(r'w=(\d+\.?\d*)', raw)
        if l_match and w_match: return f"[AREA CALCULATION]\n* Length (l): {l_match.group(1)}\n* Width (w): {w_match.group(1)}\n-> Area (l x w): {float(l_match.group(1)) * float(w_match.group(1)):.2f}"
        return "Format error!"

    # ⚡ ELECTRONICS LOGIC
    if raw.startswith("ohm"):
        v_match = re.search(r'v=(\d+\.?\d*)', raw); r_match = re.search(r'r=(\d+\.?\d*)', raw); i_match = re.search(r'i=(\d+\.?\d*)', raw)
        if v_match and r_match: return f"[OHM'S LAW]\n* Voltage (V): {v_match.group(1)} V\n* Resistance (R): {r_match.group(1)} Ohm\n-> Current (I = V/R): {float(v_match.group(1))/float(r_match.group(1)):.2f} A"
        elif v_match and i_match: return f"[OHM'S LAW]\n* Voltage (V): {v_match.group(1)} V\n* Current (I): {i_match.group(1)} A\n-> Resistance (R = V/I): {float(v_match.group(1))/float(i_match.group(1)):.2f} Ohm"
        elif i_match and r_match: return f"[OHM'S LAW]\n* Current (I): {i_match.group(1)} A\n* Resistance (R): {r_match.group(1)} Ohm\n-> Voltage (V = I*R): {float(i_match.group(1))*float(r_match.group(1)):.2f} V"
        return "Format error!"
    if raw.startswith("power"):
        v_match = re.search(r'v=(\d+\.?\d*)', raw); i_match = re.search(r'i=(\d+\.?\d*)', raw)
        if v_match and i_match: return f"[POWER CALCULATION]\n* Voltage (V): {v_match.group(1)} V\n* Current (I): {i_match.group(1)} A\n-> Power (P = V*I): {float(v_match.group(1))*float(i_match.group(1)):.2f} W"
        return "Format error!"

    # 🌡️ SMART UNIT CONVERTER LOGIC
    if raw.startswith("convert ") or "to miles" in raw or "to km" in raw:
        try:
            val = parse_text_number(raw)
            if val is None:
                unit_match = re.search(r'(\d+\.?\d*)\s*(celsius|fahrenheit|\bc\b|\bf\b|km|mile|miles)', raw)
                if unit_match: val = float(unit_match.group(1))
            if val is not None:
                if "km" in raw and "mile" in raw:
                    if raw.find("km") < raw.find("mile"):
                        return f"[LENGTH CONVERSION]\n-> {val} km = {val * 0.621371:.2f} miles"
                    else:
                        return f"[LENGTH CONVERSION]\n-> {val} miles = {val / 0.621371:.2f} km"
                elif "km" in raw: return f"[LENGTH CONVERSION]\n-> {val} km = {val * 0.621371:.2f} miles"
                elif "mile" in raw: return f"[LENGTH CONVERSION]\n-> {val} miles = {val / 0.621371:.2f} km"
                elif "celsius" in raw or re.search(r'\bc\b', raw): return f"[TEMPERATURE CONVERSION]\n-> {val} C = {(val * 9/5) + 32:.2f} F"
                elif "fahrenheit" in raw or re.search(r'\bf\b', raw): return f"[TEMPERATURE CONVERSION]\n-> {val} F = {(val - 32) * 5/9:.2f} C"
            return "Format error!"
        except Exception as e: return f"ERROR: Conversion failed! Details: {e}"

    # 📐 GEOMETRY & TRIGONOMETRY LOGIC
    if raw.startswith("pythagoras"):
        a_match = re.search(r'a=(\d+\.?\d*)', raw); b_match = re.search(r'b=(\d+\.?\d*)', raw)
        if a_match and b_match: return f"[PYTHAGORAS THEOREM]\n* Side A: {a_match.group(1)}\n* Side B: {b_match.group(1)}\n-> Hypotenuse C: {math.sqrt(float(a_match.group(1))**2 + float(b_match.group(1))**2):.2f}"
        return "Format error!"
    if raw.startswith("sin ") or raw.startswith("cos ") or raw.startswith("tan "):
        parts = raw.split()
        if len(parts) == 2:
            try:
                deg = float(parts[1]); rad = math.radians(deg)
                if parts[0] == "sin": return f"[TRIGONOMETRY]\n* sin({deg}°) = {math.sin(rad):.4f}"
                elif parts[0] == "cos": return f"[TRIGONOMETRY]\n* cos({deg}°) = {math.cos(rad):.4f}"
                elif parts[0] == "tan":
                    if math.isclose(math.cos(rad), 0, abs_tol=1e-9): return "ERROR: tan is Undefined!"
                    return f"[TRIGONOMETRY]\n* tan({deg}°) = {math.tan(rad):.4f}"
            except Exception as e: return f"ERROR: Details: {e}"
        return "Format error!"

    # 📊 VECTOR MATHEMATICS LOGIC
    if raw.startswith("vector "):
        parts = raw.split()
        if len(parts) >= 3:
            sub_cmd = parts[1]
            try:
                nums = [float(p) for p in parts[2:]]
                if sub_cmd == "mag": return f"[VECTOR MAGNITUDE]\n-> Magnitude: {math.sqrt(sum(n**2 for n in nums)):.4f}"
                if sub_cmd == "dot" and len(nums) % 2 == 0:
                    mid = len(nums) // 2; v1, v2 = nums[:mid], nums[mid:]
                    return f"[VECTOR DOT PRODUCT]\n-> Dot Product: {sum(v1[i]*v2[i] for i in range(mid)):.2f}"
            except Exception as e: return f"ERROR: Details: {e}"
        return "Format error!"

    # 💰 FINANCIAL INTEREST LOGIC
    if raw.startswith("interest"):
        p_match = re.search(r'p=(\d+\.?\d*)', raw); r_match = re.search(r'r=(\d+\.?\d*)', raw); t_match = re.search(r't=(\d+\.?\d*)', raw); n_match = re.search(r'n=(\d+)', raw)
        if p_match and r_match and t_match:
            p, r, t = float(p_match.group(1)), float(r_match.group(1)), float(t_match.group(1))
            if "compound" in raw:
                n = int(n_match.group(1)) if n_match else 1; a = p * ((1 + (r / (100 * n))) ** (n * t))
                return f"[COMPOUND INTEREST]\n-> Compound Interest (CI): {a - p:.2f}\n-> Total Amount (A): {a:.2f}"
            else: return f"[SIMPLE INTEREST]\n-> Interest Profit (I): {(p * r * t) / 100:.2f}\n-> Total Amount (A): {p + ((p * r * t) / 100):.2f}"
        return "Format error!"

    # 📐 QUADRATIC EQUATION SOLVER LOGIC
    if raw.startswith("quadratic"):
        a_match = re.search(r'a=(-?\d+\.?\d*)', raw); b_match = re.search(r'b=(-?\d+\.?\d*)', raw); c_match = re.search(r'c=(-?\d+\.?\d*)', raw)
        if a_match and b_match and c_match:
            a, b, c = float(a_match.group(1)), float(b_match.group(1)), float(c_match.group(1))
            if a == 0: return "ERROR: 'a' cannot be 0!"
            dis = (b**2) - (4*a*c)
            if dis > 0: return f"[QUADRATIC]\n* x1 = {(-b + math.sqrt(dis)) / (2*a):.4f}\n* x2 = {(-b - math.sqrt(dis)) / (2*a):.4f}"
            elif dis == 0: return f"[QUADRATIC]\n* Equal Root: x = {-b / (2*a):.4f}"
            else: return f"[QUADRATIC]\n* x1 = {-b / (2*a):.4f} + {math.sqrt(-dis) / (2*a):.4f}i\n* x2 = {-b / (2*a):.4f} - {math.sqrt(-dis) / (2*a):.4f}i"
        return "Format error!"

    # 📐 CALCULUS ENGINE
    if raw.startswith("diff "):
        expr_text = raw[5:].strip().replace("^", "**")
        try: return f"📐 [CALCULUS - DERIVATIVE]\n-> d/dx: {sp.diff(sp.sympify(expr_text), sp.Symbol('x'))}"
        except Exception as e: return f"ERROR: Details: {e}"
    if raw.startswith("integrate "):
        expr_text = raw[10:].strip().replace("^", "**")
        try: return f"📐 [CALCULUS - INTEGRAL]\n-> ∫ dx: {sp.integrate(sp.sympify(expr_text), sp.Symbol('x'))} + C"
        except Exception as e: return f"ERROR: Details: {e}"

    # 📊 STATISTICS & PROBABILITY ENGINE
    if raw.startswith("stats "):
        num_str = raw[6:].replace(",", " ")
        try:
            nums = [float(x) for x in num_str.split() if re.match(r'^-?\d+\.?\d*$', x)]
            if not nums: return "ERROR: No valid numbers!"
            return f"📊 [STATISTICS ANALYSIS]\n-> Mean: {np.mean(nums):.2f}\n-> Median: {np.median(nums):.2f}\n-> Std Deviation: {np.std(nums):.2f}"
        except Exception as e: return f"ERROR: Details: {e}"
    if raw.startswith("prob ") or raw.startswith("probability "):
        n_match = re.search(r'n=(\d+)', raw); r_match = re.search(r'r=(\d+)', raw)
        if n_match and r_match:
            n, r = int(n_match.group(1)), int(r_match.group(1))
            if r > n: return "ERROR: 'r' cannot be greater than 'n'!"
            return f"🎲 [PROBABILITY]\n-> Combination (nCr): {math.comb(n, r)}\n-> Permutation (nPr): {math.perm(n, r)}"
        return "Format error!"

    # 🔢 DIGITAL LOGIC & NUMBER SYSTEMS
    if raw.startswith("bin ") or (raw.startswith("convert ") and "to binary" in raw):
        val = parse_text_number(raw) or (int(re.search(r'(\d+)', raw).group(1)) if re.search(r'(\d+)', raw) else None)
        if val is not None: return f"🔢 [NUMBER SYSTEM]\n-> Binary: {bin(int(val))[2:]}"
        return "Format error!"
    if raw.startswith("hex ") or (raw.startswith("convert ") and "to hex" in raw):
        val = parse_text_number(raw) or (int(re.search(r'(\d+)', raw).group(1)) if re.search(r'(\d+)', raw) else None)
        if val is not None: return f"🔢 [NUMBER SYSTEM]\n-> Hexadecimal: {hex(int(val))[2:].upper()}"
        return "Format error!"
    if raw.startswith("logic "):
        expr = raw[6:].strip(); safe_expr = expr.replace("and", "&").replace("or", "|").replace("not", "~")
        if not re.match(r'^[01\s&|~()]+$', safe_expr): return "ERROR: Invalid boolean logic!"
        res = safe_boolean_eval(safe_expr)
        if res is not None: return f"🔌 [DIGITAL LOGIC]\n-> Result: {res}"
        return "ERROR: Logic evaluation failed."

    # 🧪 CHEMISTRY SOLVER ENGINE
    if raw.startswith("gas"):
        p_match = re.search(r'p=(\d+\.?\d*)', raw); v_match = re.search(r'v=(\d+\.?\d*)', raw); n_match = re.search(r'n=(\d+\.?\d*)', raw); t_match = re.search(r't=(\d+\.?\d*)', raw); R = 0.0821
        vals = {}
        if p_match: vals['P'] = float(p_match.group(1))
        if v_match: vals['V'] = float(v_match.group(1))
        if n_match: vals['n'] = float(n_match.group(1))
        if t_match: vals['T'] = float(t_match.group(1))
        if len(vals) == 3:
            if 'P' not in vals: return f"🧪 [CHEMISTRY]\n-> Pressure: {(vals['n'] * R * vals['T']) / vals['V']:.4f} atm"
            elif 'V' not in vals: return f"🧪 [CHEMISTRY]\n-> Volume: {(vals['n'] * R * vals['T']) / vals['P']:.4f} L"
            elif 'n' not in vals: return f"🧪 [CHEMISTRY]\n-> Moles: {(vals['P'] * vals['V']) / (R * vals['T']):.4f} mol"
            elif 'T' not in vals: return f"🧪 [CHEMISTRY]\n-> Temperature: {(vals['P'] * vals['V']) / (vals['n'] * R):.4f} K"
        return "Format error!"
    if raw.startswith("ph "):
        h_match = re.search(r'h=(\d+\.?\d*(?:e[+-]?\d+)?)', raw); oh_match = re.search(r'oh=(\d+\.?\d*(?:e[+-]?\d+)?)', raw)
        try:
            if h_match:
                h_conc = float(h_match.group(1))
                if h_conc <= 0: return "ERROR: Concentration must be > 0!"
                ph_val = -math.log10(h_conc); type_str = "Acidic" if ph_val < 7 else ("Neutral" if ph_val == 7 else "Basic")
                return f"🧪 [CHEMISTRY - pH]\n-> pH: {ph_val:.2f} ({type_str})"
            elif oh_match:
                oh_conc = float(oh_match.group(1))
                if oh_conc <= 0: return "ERROR: Concentration must be > 0!"
                ph_val = 14 - (-math.log10(oh_conc)); type_str = "Acidic" if ph_val < 7 else ("Neutral" if ph_val == 7 else "Basic")
                return f"🧪 [CHEMISTRY - pH]\n-> pH: {ph_val:.2f} ({type_str})"
        except Exception as e: return f"ERROR: Details: {e}"
        return "Format error!"

    # 🍎 ENTITY COUNTER LOGIC
    has_math_keyword = any(keyword in raw for keyword in MATH_KEYWORDS)
    if not has_math_keyword:
        items = re.findall(r'(\d+)\s*([\u0980-\u09FF\w]{2,})', text)
        if items:
            result = "🍎 [ENTITY COUNTER / হিসাব তালিকা]:\n"; total = 0
            for count, item in items: result += f"• {item}: {count} টি\n"; total += int(count)
            result += f"━━━━━━━━━━━━━━━━━━\n✨ মোট সংখ্যা: {total} টি"
            return result

    # 🤖 CHAT FALLBACK
    return "I'm focused on science and math! Type 'hi' for a greeting or 'guide' to see my calculation formulas."
