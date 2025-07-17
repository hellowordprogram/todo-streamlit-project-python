import streamlit as st
import mysql.connector

# --- MySQL Connection Setup ---
conn = mysql.connector.connect(
    host = "localhost",
    port = 3307,
    username = "root",
    password = "1234",
    database = "streamlitproject"
)
cursor = conn.cursor()

# --- Create Table if Not Exists ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task TEXT NOT NULL,
    done BOOLEAN DEFAULT FALSE
);
""")
conn.commit()

# --- App Title ---
st.set_page_config(page_title="ToDo App", page_icon="✅", layout="centered")
st.title("📝 ToDo App with MySQL")

# --- Add Task ---
def add_task(task):
    if task.strip() != "":
        cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
        conn.commit()
        st.success("Task added!")

# --- Update Task Status ---
def toggle_done(task_id, done):
    cursor.execute("UPDATE todos SET done = %s WHERE id = %s", (done, task_id))
    conn.commit()

# --- Delete Task ---
def delete_task(task_id):
    cursor.execute("DELETE FROM todos WHERE id = %s", (task_id,))
    conn.commit()
    st.success("Task deleted!")

# --- Fetch Tasks from DB ---
def get_tasks():
    cursor.execute("SELECT id, task, done FROM todos")
    return cursor.fetchall()

# --- Task Input ---
task_input = st.text_input("Add a new task:", placeholder="e.g. Walk the dog")
if st.button("➕ Add Task"):
    add_task(task_input)

# --- Display Tasks ---
st.markdown("## 📋 Your Tasks")
tasks = get_tasks()

if not tasks:
    st.info("No tasks found. Add your first task!")
else:
    for task_id, task_text, done in tasks:
        col1, col2, col3 = st.columns([0.05, 0.75, 0.2])

        with col1:
            checked = st.checkbox("", value=done, key=f"chk_{task_id}")
            if checked != done:
                toggle_done(task_id, checked)

        with col2:
            st.write(f"✅ {task_text}" if done else task_text)

        with col3:
            if st.button("❌ Delete", key=f"del_{task_id}"):
                delete_task(task_id)
                st.rerun()
