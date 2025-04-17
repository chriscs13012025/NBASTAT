import streamlit as st
import requests
import pandas as pd

st.title("📊 NBA Team Stats Viewer (Live from BallDontLie API)")
st.markdown("Choose an NBA team and season to view recent game performance using real stats.")

team_options = {
    "Atlanta Hawks": 1, "Boston Celtics": 2, "Brooklyn Nets": 3, "Charlotte Hornets": 4,
    "Chicago Bulls": 5, "Cleveland Cavaliers": 6, "Dallas Mavericks": 7, "Denver Nuggets": 8,
    "Detroit Pistons": 9, "Golden State Warriors": 10, "Houston Rockets": 11, "Indiana Pacers": 12,
    "LA Clippers": 13, "Los Angeles Lakers": 14, "Memphis Grizzlies": 15, "Miami Heat": 16,
    "Milwaukee Bucks": 17, "Minnesota Timberwolves": 18, "New Orleans Pelicans": 19,
    "New York Knicks": 20, "Oklahoma City Thunder": 21, "Orlando Magic": 22, "Philadelphia 76ers": 23,
    "Phoenix Suns": 24, "Portland Trail Blazers": 25, "Sacramento Kings": 26, "San Antonio Spurs": 27,
    "Toronto Raptors": 28, "Utah Jazz": 29, "Washington Wizards": 30
}

team_name = st.selectbox("Choose an NBA Team", list(team_options.keys()))
season = st.selectbox("Select Season", [2023, 2022, 2021, 2020], index=0)

@st.cache_data
def get_team_games(team_id, season):
    url = f"https://api.balldontlie.io/v1/games?team_ids[]={team_id}&seasons[]={season}&per_page=10"
    headers = {
        "Authorization": st.secrets["BALLDONTLIE_API_KEY"]
    }
    res = requests.get(url, headers=headers)
    return res.json().get("data", []) if res.status_code == 200 else []

team_id = team_options[team_name]
games = get_team_games(team_id, season)

if games:
    df = pd.DataFrame([{
        "Date": game["date"][:10],
        "Opponent": game["home_team"]["full_name"] if game["visitor_team"]["id"] == team_id else game["visitor_team"]["full_name"],
        "Team Score": game["home_team_score"] if game["home_team"]["id"] == team_id else game["visitor_team_score"],
        "Opponent Score": game["visitor_team_score"] if game["home_team"]["id"] == team_id else game["home_team_score"],
    } for game in games])

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    st.markdown(f"### Last {len(df)} Games for the {team_name}")
    st.dataframe(df)

    st.markdown("### 📈 Performance Over Time")
    chart_data = df[["Date", "Team Score", "Opponent Score"]].set_index("Date")
    st.line_chart(chart_data)
else:
    st.warning("No data available for this team/season.")
