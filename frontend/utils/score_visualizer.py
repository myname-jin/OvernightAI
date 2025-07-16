import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from math import pi

def draw_bar(score_dict, team_name, font_prop):
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(score_dict.keys(), score_dict.values(), color='skyblue')
    ax.set_ylabel("점수", fontsize=12, rotation=0, labelpad=30, fontproperties=font_prop)
    ax.set_ylim(0, max(score_dict.values()) + 10)
    plt.xticks(rotation=0, fontproperties=font_prop)
    ax.set_title(f'<{team_name}> 막대 그래프\n\n', fontsize=20, fontweight='bold', fontproperties=font_prop)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontsize=10)
    fig.tight_layout()
    return fig

def draw_radar(score_dict, team_name, font_prop):
    labels = list(score_dict.keys())
    values = list(score_dict.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontproperties=font_prop)
    ax.set_title(f'<{team_name}> 방사형 그래프\n\n', fontsize=20, fontweight='bold', fontproperties=font_prop)
    return fig

def draw_donut(score_dict, team_name, font_prop):
    labels = []
    values = []
    for k, v in score_dict.items():
        if v > 0:
            labels.append(k)
            values.append(v)
    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax.pie(values, labels=labels,
                                      autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
                                      startangle=90, textprops={'fontproperties': font_prop})
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title(f'<{team_name}> 도넛 차트\n\n', fontsize=20, fontweight='bold', fontproperties=font_prop)
    return fig

def draw_line(score_dict, team_name, font_prop):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(score_dict.keys(), score_dict.values(), marker='o', color='skyblue')
    ax.set_ylim(0, max(score_dict.values()) + 5)
    ax.set_title(f'<{team_name}> 꺾은선 그래프\n\n', fontsize=20, fontweight='bold', fontproperties=font_prop)
    ax.set_ylabel("점수", fontproperties=font_prop, rotation=0, labelpad=20)
    plt.xticks(rotation=0, fontproperties=font_prop)
    return fig

def draw_heatmap(score_dict, team_name, font_prop):
    fig, ax = plt.subplots(figsize=(6, 2))
    df_heat = pd.DataFrame([score_dict.values()], columns=score_dict.keys())
    sns.heatmap(df_heat, annot=True, cmap="YlGnBu", ax=ax, cbar=False, fmt=".1f")
    ax.set_yticks([])
    ax.set_title(f'<{team_name}> 히트맵\n\n', fontsize=20, fontweight='bold', fontproperties=font_prop)
    return fig

def draw_scorecard(score_dict, team_name, font_prop):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axis('off')
    table = pd.DataFrame({'항목': list(score_dict.keys()), '점수': list(score_dict.values())})
    ax.table(cellText=table.values, colLabels=table.columns, cellLoc='center', loc='center')
    ax.set_title(f'<{team_name}> 점수 카드\n\n', fontsize=20, fontweight='bold', fontproperties=font_prop)
    return fig
