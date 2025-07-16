import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def set_korean_font():
    font_path = "C:/Windows/Fonts/malgun.ttf"
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    return font_prop
