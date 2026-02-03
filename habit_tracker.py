import streamlit as st
import json

DATA_FILE = "habits.json"


# ---------- Data helpers ----------
def load_habits():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_habits(habits):
    with open(DATA_FILE, "w") as f:
        json.dump(habits, f, indent=2)


# ---------- App ----------
st.set_page_config(page_title="Habit Tracker", layout="centered")
st.title("🧠 Habit Tracker")

habits = load_habits()

# ---- Add habit ----
st.subheader("Add a new habit")
new_habit = st.text_input("Habit name")

if st.button("Add Habit"):
    if new_habit.strip() == "":
        st.warning("Habit name cannot be empty.")
    elif new_habit in habits:
        st.warning("Habit already exists.")
    else:
        habits[new_habit] = {"total": 0}
        save_habits(habits)
        st.success(f"Added habit: {new_habit}")
        st.rerun()

st.divider()

# ---- Habit list ----
st.subheader("Your habits")

if not habits:
    st.info("No habits yet. Add one above.")
else:
    for habit in list(habits.keys()):
        count = habits[habit]["total"]

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"**{habit}**")
            st.caption(f"Total completions: {count}")

        with col2:
            if st.button("➕ Done", key=f"add_{habit}"):
                habits[habit]["total"] += 1
                save_habits(habits)
                st.rerun()

        with col3:
            if st.button("❌", key=f"delete_{habit}"):
                del habits[habit]
                save_habits(habits)
                st.rerun()
