import streamlit as st
import json

DATA_FILE = "tasks.json"


# ---------- Data helpers ----------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------- Session setup ----------
if "passphrase" not in st.session_state:
    st.session_state.passphrase = None


# ---------- Login screen ----------
if st.session_state.passphrase is None:
    st.set_page_config(page_title="Task Tracker", layout="centered")
    st.title("🔐 Task Tracker")

    passphrase = st.text_input(
        "Enter your passphrase (case sensitive):",
        type="password",
        help="This passphrase controls your personal task list"
    )

    if st.button("Enter"):
        if passphrase.strip() == "":
            st.warning("Passphrase cannot be empty.")
        else:
            st.session_state.passphrase = passphrase
            st.rerun()

    st.stop()


# ---------- Main App ----------
st.set_page_config(page_title="Task Tracker", layout="centered")
st.title("🧠 Task Tracker")

data = load_data()
user = st.session_state.passphrase

# Ensure user space exists
if user not in data:
    data[user] = {}
    save_data(data)

tasks = data[user]

# ---- Logout ----
if st.button("🚪 Log out"):
    st.session_state.passphrase = None
    st.rerun()

st.divider()

# ---- Add task ----
st.subheader("Add a new task")
new_task = st.text_input("task name")

if st.button("Add task"):
    if new_task.strip() == "":
        st.warning("task name cannot be empty.")
    elif new_task in tasks:
        st.warning("task already exists.")
    else:
        tasks[new_task] = {"total": 0}
        save_data(data)
        st.success(f"Added task: {new_task}")
        st.rerun()

st.divider()

# ---- task list ----
st.subheader("Your tasks")

if not tasks:
    st.info("No tasks yet.")
else:
    for task in list(tasks.keys()):
        count = tasks[task]["total"]

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"**{task}**")
            st.caption(f"Total completions: {count}")

        with col2:
            if st.button("➕ Done", key=f"add_{task}"):
                tasks[task]["total"] += 1
                save_data(data)
                st.rerun()

        with col3:
            if st.button("❌", key=f"delete_{task}"):
                del tasks[task]
                save_data(data)
                st.rerun()
