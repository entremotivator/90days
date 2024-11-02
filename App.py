import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize data for 90 days (only if it hasn't been initialized)
if 'tasks_df' not in st.session_state:
    # Create a dataframe for 90 days with sample tasks
    days = [(datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(90)]
    tasks_df = pd.DataFrame({
        'Date': days,
        'Task 1': [False]*90,
        'Task 2': [False]*90,
        'Task 3': [False]*90
    })
    st.session_state['tasks_df'] = tasks_df

# Title and Description
st.title("90-Day, 90-Minute Daily Task Tracker")
st.write("Track your daily tasks and keep your momentum going for the next 90 days!")

# Select Day
selected_day = st.selectbox("Choose a Day:", st.session_state['tasks_df']['Date'])

# Filter dataframe for the selected day
day_tasks = st.session_state['tasks_df'][st.session_state['tasks_df']['Date'] == selected_day]

# Display Checklist for Tasks
st.write(f"Tasks for {selected_day}:")
for col in day_tasks.columns[1:]:
    day_tasks.loc[:, col] = st.checkbox(col, value=day_tasks[col].values[0])

# Update session state with changes
st.session_state['tasks_df'].update(day_tasks)

# Save Progress Button
if st.button("Save Progress"):
    st.write("Progress Saved!")
    # (Optional) Save to a CSV file for persistence if required:
    # st.session_state['tasks_df'].to_csv('90_day_tasks.csv', index=False)

# Progress Tracking
st.write("## Progress Overview")
completed_tasks = st.session_state['tasks_df'].iloc[:, 1:].sum(axis=1)
progress_df = pd.DataFrame({
    'Date': st.session_state['tasks_df']['Date'],
    'Tasks Completed': completed_tasks
})

# Plot progress
st.line_chart(progress_df.set_index('Date')['Tasks Completed'])

# Summary Analytics
total_tasks = len(st.session_state['tasks_df']) * (len(st.session_state['tasks_df'].columns) - 1)
completed_total = completed_tasks.sum()
st.write("### Total Completion Status")
st.write(f"Tasks Completed: {completed_total} / {total_tasks}")
st.write(f"Overall Progress: {completed_total / total_tasks * 100:.2f}%")

# Motivation / Reminder Message
if completed_total < total_tasks / 2:
    st.warning("Keep going! You're halfway there!")
elif completed_total >= total_tasks / 2 and completed_total < total_tasks:
    st.info("Great job! You're on track to reach 100%.")
else:
    st.success("Congratulations! You've completed all tasks!")
