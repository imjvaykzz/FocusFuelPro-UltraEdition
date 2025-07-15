
import streamlit as st
import pandas as pd
import random
from utils import (
    add_todo_item, complete_todo, delete_todo,
    log_study_session, load_quotes, load_music_library,
    get_today_focus_data, load_data, save_data
)

# Load quotes and music
quotes = load_quotes()
music_library = load_music_library()

# ---- UI Settings ----
st.set_page_config(page_title="FocusFuelPro", layout="wide")

# ---- Header ----
st.markdown("<h1 style='font-size: 48px; color: #4A90E2;'>FocusFuelPro</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px; color: #888;'>Premium Productivity Suite for Serious Students</p>", unsafe_allow_html=True)

# ---- Sidebar Controls ----
st.sidebar.title("🎯 Study Planner")
with st.sidebar.form(key="todo_form"):
    task = st.text_input("Add New Task")
    due_date = st.date_input("Due Date")
    if st.form_submit_button("Add Task"):
        if task:
            add_todo_item(task, str(due_date))
            st.success("Task added!")

# ---- Display TODO ----
st.subheader("📋 Your Tasks")
todos = load_data("data/todo_data.json")
if todos:
    for task_id, task_info in todos.items():
        cols = st.columns([6, 1, 1])
        with cols[0]:
            status = "✅" if task_info["completed"] else "🔲"
            st.write(f"{status} {task_info['task']} (Due: {task_info['due']})")
        with cols[1]:
            if st.button("✔️", key=f"done_{task_id}"):
                complete_todo(task_id)
        with cols[2]:
            if st.button("🗑️", key=f"del_{task_id}"):
                delete_todo(task_id)
else:
    st.info("No tasks added yet!")

# ---- Study Session Logger ----
st.subheader("⏱️ Log Study Session")
with st.form(key="session_form"):
    subject = st.text_input("Subject / Topic")
    duration = st.slider("Duration (in minutes)", 15, 180, 45)
    selected_music = st.selectbox("Music Track", [track["title"] for track in music_library])
    if st.form_submit_button("Log Session"):
        if subject:
            music_url = [track["url"] for track in music_library if track["title"] == selected_music][0]
            log_study_session(subject, duration, music_url)
            st.success("Session logged!")

# ---- Daily Stats ----
st.subheader("📊 Today's Focus Summary")
minutes_today = get_today_focus_data()
st.metric(label="Minutes Focused Today", value=f"{minutes_today} min")

# ---- Motivational Quote ----
st.markdown("---")
st.subheader("💡 Stay Motivated")
if quotes:
    quote = random.choice(quotes)
    st.markdown(f"<blockquote style='color: #F5A623;'>{quote}</blockquote>", unsafe_allow_html=True)

# ---- Music Player ----
st.subheader("🎧 Focus Music")
for track in music_library:
    st.markdown(f"**{track['title']}**")
    st.audio(track["url"])
