import streamlit as st
import random
import time

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Typing Practice App", page_icon="⌨️", layout="centered")

# ====== INITIAL DATA ======
sentences = [
    "Python is fun to learn",
    "Practice makes you perfect",
    "Typing speed improves with time",
    "Never stop learning new things",
    "Code more to think better"
]

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "test_sentence" not in st.session_state:
    st.session_state.test_sentence = ""

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

daily_goal = 30  # words per minute

# ====== THEME SWITCH ======
theme_choice = st.radio("🎨 Choose Theme", ["Light", "Dark"])
if theme_choice != st.session_state.theme:
    st.session_state.theme = theme_choice

if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        body { background-color: #222; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ====== MAIN MENU ======
st.title("⌨️ Typing Practice App")
menu = st.radio("Select an Option:", ["Start Test", "View Leaderboard", "Daily Goal"])

# ====== START TEST ======
if menu == "Start Test":
    if st.button("🎯 Start New Test"):
        st.session_state.test_sentence = random.choice(sentences)
        st.session_state.start_time = time.time()

    if st.session_state.test_sentence:
        st.write("👉 **Type this sentence:**")
        st.info(st.session_state.test_sentence)
        typed_text = st.text_area("Start typing below:")

        if st.button("✅ Submit"):
            end_time = time.time()
            time_taken = end_time - st.session_state.start_time

            words = len(typed_text.split())
            wpm = round((words / time_taken) * 60)

            correct_chars = 0
            for i in range(min(len(typed_text), len(st.session_state.test_sentence))):
                if typed_text[i] == st.session_state.test_sentence[i]:
                    correct_chars += 1

            accuracy = round((correct_chars / len(st.session_state.test_sentence)) * 100)

            st.subheader("📊 Results")
            st.write("⏱ Time Taken:", round(time_taken, 2), "seconds")
            st.write("⚡ Speed:", wpm, "WPM")
            st.write("🎯 Accuracy:", accuracy, "%")

            name = st.text_input("Enter your name to save score:")
            if st.button("💾 Save to Leaderboard"):
                st.session_state.leaderboard.append([name, wpm, accuracy])
                if wpm >= daily_goal:
                    st.success("🎉 Great job! You reached your daily goal!")
                else:
                    st.info(f"💪 Keep practicing to reach {daily_goal} WPM!")
                st.session_state.test_sentence = ""

# ====== VIEW LEADERBOARD ======
elif menu == "View Leaderboard":
    st.subheader("🏆 Leaderboard")
    if len(st.session_state.leaderboard) == 0:
        st.info("No scores yet. Try a typing test first!")
    else:
        for i in range(len(st.session_state.leaderboard)):
            entry = st.session_state.leaderboard[i]
            st.write(f"{i+1}) {entry[0]} - {entry[1]} WPM - {entry[2]}% accuracy")

# ====== DAILY GOAL ======
elif menu == "Daily Goal":
    st.subheader("🎯 Daily Typing Goal")
    st.write("Goal:", daily_goal, "WPM")

    if len(st.session_state.leaderboard) > 0:
        last_speed = st.session_state.leaderboard[-1][1]
        if last_speed >= daily_goal:
            st.success("✅ Goal Achieved Today!")
        else:
            st.warning("❌ Keep practicing to hit your goal!")
    else:
        st.info("No tests completed yet.")

# ====== FOOTER ======
st.markdown("---")
st.caption("Simple Streamlit Typing Practice App (using only lists and if-elif-else) 💡")
