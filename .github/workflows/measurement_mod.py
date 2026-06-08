import re

def solve_mod(text):
    raw = text.lower().strip()
    
    # 🏃 ১. গতি (Speed) ক্যালকুলেশন ও কনভার্সন
    if raw.startswith("speed"):
        # ফরম্যাট ১: speed d=100 t=5 (গতি বের করা)
        d_match = re.search(r'd=(\d+\.?\d*)', raw)
        t_match = re.search(r't=(\d+\.?\d*)', raw)
        if d_match and t_match:
            d = float(d_match.group(1))
            t = float(t_match.group(1))
            if t == 0: 
                return "❌ সময় (t) কখনো ০ হতে পারে না!"
            v = d / t
            return (f"🏃 [SPEED CALCULATION]\n"
                    f"• দূরত্ব (d) = {d} মিটার\n"
                    f"• সময় (t) = {t} সেকেন্ড\n"
                    f"▶️ গতি (v = d/t) = {v:.2f} m/s")
        
        # ফরম্যাট ২: speed 36 kmh (km/h থেকে m/s কনভার্ট করা)
        kmh_match = re.search(r'(\d+\.?\d*)\s*kmh', raw)
        if kmh_match:
            kmh = float(kmh_match.group(1))
            ms = kmh / 3.6
            return (f"🔄 [SPEED CONVERSION]\n"
                    f"• {kmh} km/h = {ms:.2f} m/s")
            
        return ("💡 Speed মডিউল ব্যবহারের নিয়ম:\n"
                "• গতি বের করতে লিখুন: speed d=100 t=5\n"
                "• km/h থেকে m/s করতে লিখুন: speed 36 kmh")

    # ⚖️ ২. ওজন (Weight) ক্যালকুলেশন
    if raw.startswith("weight"):
        # ফরম্যাট: weight m=50 (ভর থেকে ওজন বের করা)
        m_match = re.search(r'm=(\d+\.?\d*)', raw)
        if m_match:
            m = float(m_match.group(1))
            g = 9.8
            w = m * g
            return (f"⚖️ [WEIGHT CALCULATION]\n"
                    f"• ভর (m) = {m} কেজি\n"
                    f"• অভিকর্ষজ ত্বরণ (g) = 9.8 m/s²\n"
                    f"▶️ ওজন (W = mg) = {w:.2f} N (নিউটন)")
        return "💡 Weight মডিউল ব্যবহারের নিয়ম:\n• ওজন বের করতে লিখুন: weight m=50"

    # 📐 ৩. ক্ষেত্রফল (Area) ক্যালকুলেশন
    if raw.startswith("area"):
        # ফরম্যাট: area l=10 w=5 (আয়তক্ষেত্রের দৈর্ঘ্য ও প্রস্থ)
        l_match = re.search(r'l=(\d+\.?\d*)', raw)
        w_match = re.search(r'w=(\d+\.?\d*)', raw)
        if l_match and w_match:
            l = float(l_match.group(1))
            w = float(w_match.group(1))
            area = l * w
            return (f"📐 [AREA CALCULATION]\n"
                    f"• দৈর্ঘ্য (l) = {l}\n"
                    f"• প্রস্থ (w) = {w}\n"
                    f"▶️ ক্ষেত্রফল (Area = l × w) = {area:.2f} বর্গ একক")
        return "💡 Area মডিউল ব্যবহারের নিয়ম:\n• ক্ষেত্রফল বের করতে লিখুন: area l=10 w=5"

    return None