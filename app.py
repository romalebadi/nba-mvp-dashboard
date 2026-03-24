import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import numpy as np

st.set_page_config(page_title="NBA MVP Dashboard", layout="wide")
st.title("NBA MVP vs Runner-Up: 40 Years of Stats")

df = pd.read_csv("C:/Users/Owner/OneDrive/Desktop/Code/mvp_stats.csv")

# --- Sidebar filters ---
st.sidebar.header("Filters")
seasons = df["SEASON"].unique().tolist()
selected_seasons = st.sidebar.multiselect("Seasons", seasons, default=seasons)
stat_options = ["PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FT_PCT", "FG3_PCT", "TOV", "MIN"]
selected_stat = st.sidebar.selectbox("Stat to chart over time", stat_options, index=0)

filtered = df[df["SEASON"].isin(selected_seasons)]

# --- Section 1: Stat over time ---
st.subheader(f"{selected_stat} over time — MVP vs Runner-Up")
fig1 = px.line(
    filtered, x="SEASON", y=selected_stat, color="ROLE",
    hover_data=["PLAYER", "TEAM"], markers=True,
    color_discrete_map={"MVP": "#185FA5", "Runner-Up": "#D85A30"}
)
fig1.update_layout(xaxis_tickangle=-45, height=400)
st.plotly_chart(fig1, use_container_width=True)

# --- Section 2: Head to head ---
st.subheader("Season breakdown — head to head")
season_pick = st.selectbox("Pick a season", sorted(df["SEASON"].unique(), reverse=True))
season_df = df[df["SEASON"] == season_pick]

mvp_row = season_df[season_df["ROLE"] == "MVP"].iloc[0]
ru_row = season_df[season_df["ROLE"] == "Runner-Up"].iloc[0]

col1, col2, col3 = st.columns(3)

# MVP column
col1.markdown(f"### {mvp_row['PLAYER']} — {mvp_row['TEAM']}")
col1.markdown("**MVP**")
for stat in ["PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FT_PCT", "FG3_PCT", "TOV", "GP"]:
    col1.metric(stat, mvp_row[stat])

# Runner-up column
col2.markdown(f"### {ru_row['PLAYER']} — {ru_row['TEAM']}")
col2.markdown("**Runner-Up**")
for stat in ["PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FT_PCT", "FG3_PCT", "TOV", "GP"]:
    col2.metric(stat, ru_row[stat])

# Difference column
col3.markdown("### Difference")
col3.markdown("**MVP vs Runner-Up**")
for stat in ["PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FT_PCT", "FG3_PCT", "TOV", "GP"]:
    diff = round(mvp_row[stat] - ru_row[stat], 1)
    # For TOV lower is better so flip the color logic
    if stat == "TOV":
        delta_color = "inverse"
    else:
        delta_color = "normal"
    col3.metric(stat, diff, delta=diff, delta_color=delta_color)


# --- Section 3: Radar chart ---
st.subheader("Radar comparison")
cats = ["PTS", "AST", "REB", "STL", "BLK"]
fig2 = go.Figure()
colors = {"MVP": "#185FA5", "Runner-Up": "#D85A30"}

for _, row in season_df.iterrows():
    vals = [row[c] for c in cats] + [row[cats[0]]]
    fig2.add_trace(go.Scatterpolar(
        r=vals, theta=cats + [cats[0]],
        fill='toself', name=f"{row['PLAYER']} — {row['TEAM']} ({row['ROLE']})",
        line_color=colors[row["ROLE"]]
    ))

fig2.update_layout(polar=dict(radialaxis=dict(visible=True)), height=450)
st.plotly_chart(fig2, use_container_width=True)

# --- Section 4: Leaderboard ---
st.subheader("All-time MVP averages")
mvp_only = df[df["ROLE"] == "MVP"]
leaderboard = mvp_only.groupby("PLAYER")[stat_options].mean().round(1).reset_index()
leaderboard = leaderboard.sort_values("PTS", ascending=False)
st.dataframe(leaderboard, use_container_width=True)

# --- Section 5: Greatest MVP Season Ever ---
st.subheader("Greatest MVP season ever")
st.markdown("Ranked by composite score — raw stats vs other MVPs + dominance over that season's runner-up.")

mvp_df = df[df["ROLE"] == "MVP"].copy()
ru_df = df[df["ROLE"] == "Runner-Up"].copy()

# Merge MVP and runner-up stats side by side
merged = mvp_df.merge(ru_df, on="SEASON", suffixes=("_MVP", "_RU"))

# Stats where higher = better
positive = ["PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FT_PCT", "FG3_PCT"]
# Stats where lower = better
negative = ["TOV"]

scaler = MinMaxScaler()

# 1. How good was the MVP compared to ALL other MVPs
raw_scores = scaler.fit_transform(merged[[f"{s}_MVP" for s in positive]]).mean(axis=1)
tov_score = (1 - scaler.fit_transform(merged[["TOV_MVP"]])).flatten()

# 2. How dominant were they over their runner-up
for stat in positive + negative:
    merged[f"DIFF_{stat}"] = merged[f"{stat}_MVP"] - merged[f"{stat}_RU"]

diff_scores = scaler.fit_transform(merged[[f"DIFF_{s}" for s in positive]]).mean(axis=1)
diff_tov = (1 - scaler.fit_transform(merged[["DIFF_TOV"]])).flatten()

# Final score: 50% raw performance, 50% dominance over runner-up
merged["SCORE"] = (
    (raw_scores * 0.35) +
    (tov_score * 0.15) +
    (diff_scores * 0.35) +
    (diff_tov * 0.15)
) * 100

merged["SCORE"] = merged["SCORE"].round(1)

# Build clean display table
display = merged[[
    "SEASON", "PLAYER_MVP", "TEAM_MVP",
    "PTS_MVP", "AST_MVP", "REB_MVP", "STL_MVP", "BLK_MVP",
    "FG_PCT_MVP", "FG3_PCT_MVP", "FT_PCT_MVP", "TOV_MVP", "SCORE"
]].sort_values("SCORE", ascending=False).reset_index(drop=True)

display.index += 1
display.columns = [
    "SEASON", "PLAYER", "TEAM",
    "PTS", "AST", "REB", "STL", "BLK",
    "FG%", "3P%", "FT%", "TOV", "SCORE"
]

st.dataframe(display, use_container_width=True)

# Top 10 bar chart
st.markdown("#### Top 10 greatest MVP seasons")
top10 = display.head(10).copy()
top10["LABEL"] = top10["PLAYER"] + " (" + top10["SEASON"] + ")"
fig_greatest = px.bar(
    top10, x="SCORE", y="LABEL", orientation="h",
    color="SCORE", color_continuous_scale=["#B5D4F4", "#185FA5"],
    labels={"SCORE": "Composite Score", "LABEL": ""}
)
fig_greatest.update_layout(height=420, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_greatest, use_container_width=True)

# --- Section 6: Team Win % With vs Without MVP ---
st.subheader("Team performance with vs without MVP on the court")
st.markdown("Based on team win % in games the MVP played vs games they missed.")

onoff_df = pd.read_csv("C:/Users/Owner/OneDrive/Desktop/Code/mvp_onoff.csv")

# Drop rows where win_pct_without is null (player never missed a game)
onoff_df = onoff_df.dropna(subset=["win_pct_without", "win_pct_diff"])
onoff_df = onoff_df.sort_values("win_pct_diff", ascending=False).reset_index(drop=True)
onoff_df.index += 1

# Summary table
st.dataframe(
    onoff_df[["player", "season", "games_played", "win_pct_with", "games_missed", "win_pct_without", "win_pct_diff"]],
    use_container_width=True
)

# Bar chart
st.markdown("#### Win % difference (with minus without)")
fig_onoff = px.bar(
    onoff_df, x="win_pct_diff", y="player", orientation="h",
    text="season", hover_data=["win_pct_with", "win_pct_without", "games_missed"],
    color="win_pct_diff",
    color_continuous_scale=["#D85A30", "#ffffff", "#185FA5"],
    color_continuous_midpoint=0,
    labels={"win_pct_diff": "Win % Difference", "player": ""}
)
fig_onoff.update_layout(height=900, yaxis=dict(autorange="reversed"))
fig_onoff.update_traces(textposition="inside")
st.plotly_chart(fig_onoff, use_container_width=True)

# Highlight biggest impact seasons
st.markdown("#### Top 10 most impactful MVP seasons")
top_impact = onoff_df.head(10)[["player", "season", "win_pct_with", "win_pct_without", "win_pct_diff"]]
top_impact.index = range(1, 11)
st.dataframe(top_impact, use_container_width=True)