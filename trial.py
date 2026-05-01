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
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
    }

    .app-header {
        background: linear-gradient(135deg, #0f1c3f 0%, #1a3a6e 50%, #0f1c3f 100%);
        border-radius: 16px;
        padding: 1.8rem 2rem 1.5rem 2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 32px rgba(0, 80, 200, 0.25);
        border: 1px solid rgba(100, 160, 255, 0.15);
    }

    .app-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0 0 0.2rem 0;
    }

    .app-title span {
        background: linear-gradient(90deg, #4A9EFF, #64dcb4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .app-tagline {
        font-size: 0.85rem;
        color: rgba(180, 210, 255, 0.7);
        font-weight: 400;
        margin: 0 0 1rem 0;
    }

    .current-time {
        display: inline-block;
        font-size: 1rem;
        font-weight: 600;
        color: #a8d4ff;
        background: rgba(74, 158, 255, 0.12);
        border: 1px solid rgba(74, 158, 255, 0.25);
        border-radius: 8px;
        padding: 0.35rem 0.9rem;
    }

    /* Done button — green */
    .btn-done button {
        background: linear-gradient(135deg, #12b76a, #0e9256) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 3px 12px rgba(18, 183, 106, 0.45) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    .btn-done button:hover {
        background: linear-gradient(135deg, #0e9256, #0a7040) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(18, 183, 106, 0.6) !important;
    }

    /* Delete button — red */
    .btn-delete button {
        background: linear-gradient(135deg, #f04438, #c0392b) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 3px 12px rgba(240, 68, 56, 0.45) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    .btn-delete button:hover {
        background: linear-gradient(135deg, #c0392b, #922b21) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(240, 68, 56, 0.6) !important;
    }

    /* Add Task button — blue */
    .btn-add button {
        background: linear-gradient(135deg, #2563eb, #1a4abf) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    .btn-add button:hover {
        background: linear-gradient(135deg, #1a4abf, #133799) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 7px 20px rgba(37, 99, 235, 0.6) !important;
    }

    div[data-testid="metric-container"] {
        background: rgba(30, 50, 100, 0.08);
        border: 1px solid rgba(74, 158, 255, 0.15);
        border-radius: 12px;
        padding: 0.8rem !important;
        text-align: center;
    }

    div[data-testid="metric-container"] label {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }

    h3 {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="app-header">
    <div class="app-title">⚡ <span>Cueflow</span></div>
    <div class="app-tagline">Deadline-aware task scheduling — stay ahead, always.</div>
    <div class="current-time">🕒 {now().strftime("%B %d, %Y  —  %I:%M %p")}</div>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("➕ Add Task")
with st.form("task_form"):
    name = st.text_input("Task Name")
    date = st.date_input("Date")
    time_input = st.time_input("Time", step=timedelta(minutes=1))

    st.markdown('<div class="btn-add">', unsafe_allow_html=True)
    submitted = st.form_submit_button("➕ Add Task")
    st.markdown('</div>', unsafe_allow_html=True)

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
                    st.markdown('<div class="btn-done">', unsafe_allow_html=True)
                    if st.button("✔️ Done", key=f"done_{task_id}"):
                        mark_done(task_id)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            with colB:
                st.markdown('<div class="btn-delete">', unsafe_allow_html=True)
                if st.button("🗑 Delete", key=f"del_{task_id}"):
                    delete_task(task_id)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

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