import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import sqlite3

conn = sqlite3.connect("tasks.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        time TEXT,
        done INTEGER
    )
""")
conn.commit()


def now():
    return datetime.now()


def get_task_status(task):
    task_time = datetime.strptime(task[2], "%Y-%m-%d %H:%M:%S")
    if task[3]:
        return "✔️ Done"
    elif task_time < now():
        return "❌ Expired"
    return "⏳ Pending"


def add_task(name, task_time):
    c.execute("INSERT INTO tasks (task, time, done) VALUES (?, ?, ?)", (name, task_time, 0))
    conn.commit()


def get_tasks():
    c.execute("SELECT * FROM tasks ORDER BY time ASC")
    return c.fetchall()


def mark_done(task_id):
    c.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
    conn.commit()


def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()


st.set_page_config(page_title="Cueflow", layout="centered")

st.markdown("""
<style>
    /* Title size */
    h1 {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
    }

    /* Current time display */
    .current-time {
        font-size: 1.25rem;
        font-weight: 600;
        color: #4A9EFF;
        margin-bottom: 1rem;
    }

    /* Done button - green */
    div[data-testid="column"] button[kind="secondary"]:has(p:contains("✔️")) {
        background-color: #1a7a4a !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 1.1rem !important;
        padding: 0.4rem 0.8rem !important;
        transition: background-color 0.2s ease !important;
    }

    /* Delete button - red */
    div[data-testid="column"] button[kind="secondary"]:has(p:contains("🗑")) {
        background-color: #a12020 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 1.1rem !important;
        padding: 0.4rem 0.8rem !important;
        transition: background-color 0.2s ease !important;
    }

    /* General button hover highlight */
    div.stButton > button {
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.4rem 1rem !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }

    /* Form submit button */
    div.stButton > button[kind="primaryFormSubmit"],
    div.stFormSubmitButton > button {
        background-color: #1a6ee0 !important;
        color: white !important;
        border: none !important;
        font-size: 1.05rem !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 8px !important;
    }

    div.stFormSubmitButton > button:hover {
        background-color: #1456b0 !important;
        transform: scale(1.03) !important;
    }

    /* Metric labels bigger */
    div[data-testid="metric-container"] label {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Welcome to Queflow")
st.markdown(f'<div class="current-time">🕒 {now().strftime("%B %d, %Y  —  %I:%M %p")}</div>', unsafe_allow_html=True)
st.divider()

st.subheader("➕ Add Task")
with st.form("task_form"):
    name = st.text_input("Task Name")
    date = st.date_input("Date")
    time_input = st.time_input("Time", step=timedelta(minutes=1))
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if not name:
            st.error("Task name is required.")
        else:
            task_datetime = datetime.combine(date, time_input)
            if task_datetime < now():
                st.error("Selected time has already passed.")
            else:
                add_task(name, task_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                st.success("Task added successfully.")

st.divider()

tasks = get_tasks()
st.subheader("📌 Tasks")

if not tasks:
    st.info("No tasks found. Add one above.")
else:
    for task in tasks:
        task_id, task_name, time_str, done_flag = task
        status = get_task_status(task)
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write(f"**{task_name}**")
            st.caption(time_str)
        with col2:
            st.write(status)
            colA, colB = st.columns(2)
            with colA:
                if not done_flag:
                    if st.button("✔️", key=f"done_{task_id}"):
                        mark_done(task_id)
                        st.rerun()
            with colB:
                if st.button("🗑 Delete", key=f"del_{task_id}"):
                    delete_task(task_id)
                    st.rerun()

st.divider()

st.subheader("📊 Overview")
total = len(tasks)
done = sum(1 for t in tasks if t[3] == 1)
expired = sum(1 for t in tasks if t[3] == 0 and datetime.strptime(t[2], "%Y-%m-%d %H:%M:%S") < now())
pending = total - done - expired

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total", total)
col2.metric("Done", done)
col3.metric("Pending", pending)
col4.metric("Expired", expired)

st.divider()

st.subheader("📈 Analytics")
if total > 0:
    df = pd.DataFrame({
        "Status": ["Done", "Pending", "Expired"],
        "Count": [done, pending, expired]
    })
    st.bar_chart(df.set_index("Status"))
else:
    st.info("No data to display yet.")