import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Habit Tracker", layout="centered")

# ------------------------
# Helper functions
# ------------------------

def calculate_current_streak(dates):
    if not dates:
        return 0

    dates = sorted(set(dates))
    streak = 0
    today = date.today()

    for i in range(len(dates)):
        if today - timedelta(days=i) in dates:
            streak += 1
        else:
            break

    return streak


def calculate_longest_streak(dates):
    if not dates:
        return 0

    dates = sorted(set(dates))
    longest = 1
    current = 1

    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest


# ------------------------
# Session State
# ------------------------

if "completions" not in st.session_state:
    st.session_state.completions = []


# ------------------------
# UI
# ------------------------

st.title("🔥 Habit Tracker")

today = date.today()

st.subheader("Actions")

if st.button("✅ Mark Complete Today"):
    if today not in st.session_state.completions:
        st.session_state.completions.append(today)
        st.success("Marked as complete!")
    else:
        st.info("Already completed today.")

if st.button("❌ Remove Today"):
    if today in st.session_state.completions:
        st.session_state.completions.remove(today)
        st.warning("Today's completion removed.")
    else:
        st.info("Nothing to remove today.")


# ------------------------
# Stats
# ------------------------

current_streak = calculate_current_streak(st.session_state.completions)
longest_streak = calculate_longest_streak(st.session_state.completions)

st.divider()
st.subheader("Stats")

col1, col2, col3 = st.columns(3)
col1.metric("Total Completions", len(st.session_state.completions))
col2.metric("Current Streak", current_streak)
col3.metric("Longest Streak", longest_streak)

# ------------------------
# History
# ------------------------

st.divider()
st.subheader("Completion History")

if st.session_state.completions:
    for d in sorted(st.session_state.completions, reverse=True):
        st.write(f"• {d.isoformat()}")
else:
    st.write("No completions yet.")
