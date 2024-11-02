import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize the DataFrame in session state if not already done
if 'tasks_df' not in st.session_state:
    days = [(datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(90)]
    tasks_df = pd.DataFrame({
        'Date': days,
        'Task 1': [False] * 90,
        'Task 2': [False] * 90,
        'Task 3': [False] * 90,
        'Task 4': [False] * 90,
        'Task 5': [False] * 90,
        'Notes': [''] * 90,
    })
    st.session_state['tasks_df'] = tasks_df

# App Title and Introduction
st.title("90-Day Goal Tracker: 90 Minutes a Day!")
st.subheader("Stay motivated and consistent by tracking daily tasks, reviewing progress, and reflecting over a 90-day journey.")
st.write("Each day, check off tasks, add notes, and see your progress grow. Remember, small steps make big changes!")

# Sidebar for Date Navigation
st.sidebar.title("Day Selector")
selected_day = st.sidebar.selectbox("Navigate to a Day:", st.session_state['tasks_df']['Date'])
day_index = st.session_state['tasks_df'][st.session_state['tasks_df']['Date'] == selected_day].index[0]

# Task Tracking Section
st.header(f"Task Completion for {selected_day}")
st.write("Mark tasks as completed for today:")
for i in range(1, 6):
    task_col = f'Task {i}'
    st.session_state['tasks_df'].at[day_index, task_col] = st.checkbox(
        task_col, value=st.session_state['tasks_df'].at[day_index, task_col])

# Notes Section
st.subheader("Daily Reflections and Notes")
st.session_state['tasks_df'].at[day_index, 'Notes'] = st.text_area(
    "Capture your thoughts or insights from the day:", value=st.session_state['tasks_df'].at[day_index, 'Notes'])

# Save Progress Button
if st.button("Save Today’s Progress"):
    st.success("Your progress for today has been saved!")

# Progress Overview Section
st.header("Progress Overview")
completed_tasks = st.session_state['tasks_df'].iloc[:, 1:6].sum(axis=1)
st.session_state['tasks_df']['Completed Tasks'] = completed_tasks

# Display progress as a bar chart
st.write("### Daily Task Completion Trend")
st.line_chart(st.session_state['tasks_df']['Completed Tasks'], use_container_width=True)

# Calculate and Display Overall Progress
total_tasks = 5 * 90
completed_total = completed_tasks.sum()
completion_percentage = (completed_total / total_tasks) * 100
st.write(f"**Overall Progress:** {completion_percentage:.2f}% ({completed_total} of {total_tasks} tasks completed)")

# Motivational Feedback
st.write("### Keep Going!")
if completion_percentage < 33:
    st.warning("You’re getting started! Every small action is a step closer to your goal.")
elif 33 <= completion_percentage < 66:
    st.info("Solid progress! Keep up the momentum—you’re more than halfway!")
else:
    st.success("Amazing dedication! You’re nearing the finish line!")

# Export to CSV
st.header("Export Your Progress")
if st.button("Download Progress CSV"):
    st.session_state['tasks_df'].to_csv('90_day_goal_tracker_progress.csv', index=False)
    st.success("Progress data exported as '90_day_goal_tracker_progress.csv'.")

# Weekly Overview and Analytics
st.header("Weekly Analysis")
st.write("### Task Completion by Week")
weekly_completion = st.session_state['tasks_df'].groupby(
    np.arange(len(st.session_state['tasks_df'])) // 7)['Completed Tasks'].sum().reset_index()
weekly_completion['Week'] = weekly_completion.index + 1
st.bar_chart(weekly_completion['Completed Tasks'], use_container_width=True)

# Daily Notes Review
st.header("Daily Reflections Summary")
selected_notes_day = st.selectbox("Select a Day to Review Notes:", st.session_state['tasks_df']['Date'])
notes_index = st.session_state['tasks_df'][st.session_state['tasks_df']['Date'] == selected_notes_day].index[0]
st.write(f"**Notes for {selected_notes_day}:**")
st.write(st.session_state['tasks_df'].at[notes_index, 'Notes'])

# 90-Day Reflection Section
st.header("90-Day Reflection")
if st.button("View Full 90-Day Summary"):
    st.write("### Completion Summary for the 90 Days")
    st.write(st.session_state['tasks_df'][['Date', 'Completed Tasks', 'Notes']])
    
# Save Final Reflection
st.subheader("Save Your 90-Day Reflection")
reflection_text = st.text_area("Reflect on your 90-day journey here:")
if st.button("Save Reflection"):
    with open('90_day_reflection.txt', 'w') as f:
        f.write(reflection_text)
    st.success("Reflection saved as '90_day_reflection.txt'.")
