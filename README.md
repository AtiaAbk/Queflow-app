# Cueflow

> A lightweight, deadline-aware task scheduling dashboard built with Streamlit and SQLite.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-embedded-lightgrey?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Overview

**Cueflow** is a minimal productivity dashboard that helps you track tasks with real-time deadline awareness. Each task is automatically classified as **Pending**, **Done**, or **Expired** based on the current time — no manual updates needed.

---

## Features

- Add tasks with a specific date and time
- Auto-status detection: ⏳ Pending / ✅ Done / ❌ Expired
- Mark tasks as complete or delete them instantly
- Overview metrics: Total, Done, Pending, Expired
- Bar chart analytics for task distribution
- Persistent storage via embedded SQLite database

---

## Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| Frontend   | Streamlit         |
| Database   | SQLite (local)    |
| Language   | Python 3.8+       |
| Data Layer | pandas            |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cueflow.git
cd cueflow
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Project Structure

```
cueflow/
├── app.py              # Main application
├── tasks.db            # SQLite database (auto-generated)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## Requirements

Create a `requirements.txt` with the following:

```
streamlit
pandas
```

---

## Screenshots

> _Add screenshots here after deployment_

---

## Roadmap

- [ ] Task categories and priority levels
- [ ] Email or browser notifications before deadlines
- [ ] Export tasks to CSV
- [ ] Dark mode toggle
- [ ] User authentication

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Built with ☕ and Python.  
Feel free to fork, improve, and contribute.
