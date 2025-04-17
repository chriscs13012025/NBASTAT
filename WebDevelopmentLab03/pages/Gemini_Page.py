import streamlit as st
import requests
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 NBA Matchup Preview (Powered by Gemini + BallDontLie API)")
st.markdown("Select two NBA teams to compare using real stats. Gemini will write a game preview for you.")

teams = {
    "Atlanta Hawks": 1, "Boston Celtics": 2, "Brooklyn Nets": 3, "Charlotte Hornets": 4,
    "Chicago Bulls": 5, "Cleveland Cavaliers": 6, "Dallas Mavericks": 7, "Denver Nuggets": 8,
    "Detroit Pistons": 9, "Golden State Warriors": 10, "Houston Rockets": 11, "Indiana Pacers": 12,
    "LA Clippers": 13, "Los Angeles Lakers": 14, "Memphis Grizzlies": 15, "Miami Heat": 16,
    "Milwaukee Bucks": 17, "Minnesota Timberwolves": 18, "New Orleans Pelicans": 19,
    "New York Knicks": 20, "Oklahoma City Thunder": 21, "Orlando Magic": 22, "Philadelphia 76ers": 23,
    "Phoenix Suns": 24, "Portland Trail Blazers": 25, "Sacramento Kings": 26, "San Antonio Spurs": 27,
    "Toronto Raptors": 28, "Utah Jazz": 29, "Washington Wizards": 30
}

team1 = st.selectbox("Select Team 1", list(teams.keys()))
team2 = st.selectbox("Select Team 2", list(teams.keys()), index=1)

if team1 == team2:
    st.warning("Please choose two different teams.")
    st.stop()

@st.cache_data
def get_recent_stats(team_id):
    url = f"https://api.balldontlie.io/v1/games?team_ids[]={team_id}&seasons[]=2023&per_page=5"
    headers = {
        "Authorization": st.secrets["BALLDONTLIE_API_KEY"],
        "Accept": "application/json"
    }

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return 0, [f"⚠️ API failed with code {res.status_code}"]

    try:
        data = res.json()["data"]
    except Exception:
        return 0, ["⚠️ Could not decode API response"]

    if not data:
        return 0, ["⚠️ No recent games found"]

    total_pts = 0
    game_results = []

    for game in data:
        if game["home_team"]["id"] == team_id:
            pts = game["home_team_score"]
            opp_pts = game["visitor_team_score"]
            opp = game["visitor_team"]["full_name"]
        else:
            pts = game["visitor_team_score"]
            opp_pts = game["home_team_score"]
            opp = game["home_team"]["full_name"]

        total_pts += pts
        game_results.append(f"{pts}-{opp_pts} vs {opp}")

    avg_pts = round(total_pts / len(data), 1)
    return avg_pts, game_results

team1_avg, team1_games = get_recent_stats(teams[team1])
team2_avg, team2_games = get_recent_stats(teams[team2])

if "⚠️" in team1_games[0] or "⚠️" in team2_games[0]:
    st.error("Could not retrieve game data for one or both teams. Please try different teams.")
    st.stop()

prompt = (
    f"You're a professional NBA analyst. Compare these two teams based on recent games.\n\n"
    f"{team1} - Avg Points: {team1_avg}\nGames: {', '.join(team1_games)}\n\n"
    f"{team2} - Avg Points: {team2_avg}\nGames: {', '.join(team2_games)}\n\n"
    f"Write a matchup preview predicting who is likely to win and why."
)

if st.button("Generate Matchup Preview"):
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt)
        st.markdown("### 🧠 Gemini's Analysis")
        st.write(response.text)
    except Exception as e:
        st.error(f"Gemini error: {e}")
