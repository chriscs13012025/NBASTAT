import streamlit as st

st.title("Welcome to Our Lab03 Web App!")

st.header("Team Info")
st.markdown("**Team Number**: 29")
st.markdown("**Section**: A")
st.markdown("**Team Members**: Christophe Clement, William Price")

st.header("Page Descriptions")
st.markdown("""
1. **Home Page**: Overview of the project and team members.
2. **Standings Page**: Displays updated team standings and statistics using real-time sports data from a public API.
3. **Insights Page**: Uses Google Gemini to generate dynamic summaries and comparisons between teams based on API data.
4. **Chatbot Page**: Interactive chatbot that answers questions about current standings, team matchups, and season projections.
""")

st.header("Intro")
st.write("Welcome to our real-time sports data app! Use the sidebar to view live standings, AI-generated insights, and interact with our chatbot.")
