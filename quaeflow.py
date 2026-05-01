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
    task_time = datetime.strptime(task[2], "%Y-%m-%d %H:%M:%S")  # ✅ FIXED
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


st.set_page_config(page_title="Queflow", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Sora', sans-serif !important;
}

.app-header {
    background: linear-gradient(135deg, #0f1c3f 0%, #1a3a6e 50%, #0f1c3f 100%);
    border-radius: 16px;
    padding: 1.8rem 2rem 1.5rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,80,200,0.25);
    border: 1px solid rgba(100,160,255,0.15);
}
.app-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #fff;
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
    color: rgba(180,210,255,0.7);
    margin: 0 0 1rem 0;
}
.current-time {
    display: inline-block;
    font-size: 1rem;
    font-weight: 600;
    color: #a8d4ff;
    background: rgba(74,158,255,0.12);
    border: 1px solid rgba(74,158,255,0.25);
    border-radius: 8px;
    padding: 0.35rem 0.9rem;
}
.section-header {
    font-size: 1.05rem;
    font-weight: 700;
    color: #c8deff;
    padding: 0.5rem 0 0.8rem 0;
    border-bottom: 1px solid rgba(74,158,255,0.15);
    margin-bottom: 1rem;
}
.task-card {
    background: rgba(20,40,90,0.35);
    border: 1px solid rgba(74,158,255,0.12);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
}
.task-name {
    font-size: 1rem;
    font-weight: 700;
    color: #e8f0ff;
    margin: 0 0 0.2rem 0;
}
.task-time {
    font-size: 0.78rem;
    color: rgba(160,190,255,0.55);
    margin: 0;
}
.status-done    { color: #34d399 !important; font-weight: 700 !important; }
.status-expired { color: #f87171 !important; font-weight: 700 !important; }
.status-pending { color: #fbbf24 !important; font-weight: 700 !important; }

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 0.5rem 0 1.5rem 0;
}
.metric-card {
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.07);
}
.mc-total   { background: linear-gradient(135deg, #1e3a6e, #162d56); }
.mc-done    { background: linear-gradient(135deg, #064e35, #053d29); border-color: rgba(52,211,153,0.2) !important; }
.mc-pending { background: linear-gradient(135deg, #4a3000, #3a2500); border-color: rgba(251,191,36,0.2) !important; }
.mc-expired { background: linear-gradient(135deg, #4a1010, #3a0c0c); border-color: rgba(248,113,113,0.2) !important; }
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: rgba(200,220,255,0.5);
    margin: 0 0 0.3rem 0;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #fff;
    margin: 0;
    line-height: 1;
}

.btn-done button {
    background: linear-gradient(135deg, #12b76a, #0e9256) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    box-shadow: 0 3px 10px rgba(18,183,106,0.4) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.btn-done button:hover {
    background: linear-gradient(135deg, #0e9256, #0a7040) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(18,183,106,0.6) !important;
}
.btn-delete button {
    background: linear-gradient(135deg, #f04438, #c0392b) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    box-shadow: 0 3px 10px rgba(240,68,56,0.4) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.btn-delete button:hover {
    background: linear-gradient(135deg, #c0392b, #922b21) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(240,68,56,0.6) !important;
}
.btn-add button {
    background: linear-gradient(135deg, #2563eb, #1a4abf) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.45) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.btn-add button:hover {
    background: linear-gradient(135deg, #1a4abf, #133799) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 20px rgba(37,99,235,0.6) !important;
}
.stTextInput > label,
.stDateInput > label,
.stTimeInput > label {
    color: #a8c8ff !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── HEADER ──
st.markdown(f"""
<div class="app-header">
    <div class="app-title">⚡ <span>Queflow</span></div>
    <div class="app-tagline">Deadline-aware task scheduling — stay ahead, always.</div>
    <div class="current-time">🕒 {now().strftime("%B %d, %Y  —  %I:%M %p")}</div>
</div>
""", unsafe_allow_html=True)


# ── ADD TASK ──
st.markdown('<div class="section-header">➕ Add New Task</div>', unsafe_allow_html=True)
with st.form("task_form"):
    name = st.text_input("Task Name")
    col_d, col_t = st.columns(2)
    with col_d:
        date = st.date_input("Date")
    with col_t:
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

# ── TASK LIST ──
tasks = get_tasks()
st.markdown('<div class="section-header">📌 Tasks</div>', unsafe_allow_html=True)

if not tasks:
    st.info("No tasks yet. Add one above.")
else:
    for task in tasks:
        task_id, task_name, time_str, done_flag = task
        status = get_task_status(task)
        status_class = "status-done" if "Done" in status else "status-expired" if "Expired" in status else "status-pending"

        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"""
            <div class="task-card">
                <p class="task-name">{task_name}</p>
                <p class="task-time">🕐 {time_str}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="{status_class}" style="margin-top:1rem; font-size:0.9rem;">{status}</p>', unsafe_allow_html=True)
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

# ── OVERVIEW ──
total = len(tasks)
done  = sum(1 for t in tasks if t[3] == 1)
expired = sum(1 for t in tasks if t[3] == 0 and datetime.strptime(t[2], "%Y-%m-%d %H:%M:%S") < now())
pending = total - done - expired

st.markdown('<div class="section-header">📊 Overview</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card mc-total">
        <p class="metric-label">Total</p>
        <p class="metric-value">{total}</p>
    </div>
    <div class="metric-card mc-done">
        <p class="metric-label">Done</p>
        <p class="metric-value">{done}</p>
    </div>
    <div class="metric-card mc-pending">
        <p class="metric-label">Pending</p>
        <p class="metric-value">{pending}</p>
    </div>
    <div class="metric-card mc-expired">
        <p class="metric-label">Expired</p>
        <p class="metric-value">{expired}</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── ANALYTICS ──
st.markdown('<div class="section-header">📈 Analytics</div>', unsafe_allow_html=True)
if total > 0:
    df = pd.DataFrame({
        "Status": ["Done", "Pending", "Expired"],
        "Count": [done, pending, expired]
    })
    st.bar_chart(df.set_index("Status"))
else:
    st.info("No data to display yet.")