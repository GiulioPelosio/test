import streamlit as st 
import pandas as pd



import pandas as pd
import streamlit as st

import pandas as pd
import streamlit as st

def display_score_by_attempt(selected_test):
    try:
        # Load data from the CSV file
        data = pd.read_csv("test_attempts.csv")

        # Calculate the score for each attempt
        # Assuming 'Outcome' column has 'Correct' for correct answers and 'Incorrect' for incorrect answers
        data['Score'] = data['Outcome'] == 'Correct'
        
        # Aggregate data to get score per test attempt (assuming each attempt is uniquely identified by 'Timestamp' and 'Test Name')
        scores_by_attempt = data.groupby(['Test Name', 'Timestamp']).agg({'Score': 'sum'}).reset_index()

        # Add an attempt number for each test (chronologically)
        scores_by_attempt['Attempt Number'] = scores_by_attempt.groupby('Test Name').cumcount() + 1
        
        # Allow users to select a test to view score progression
        test_names = scores_by_attempt['Test Name'].unique()
        selected_test = selected_test

        # Filter data for the selected test
        selected_test_scores = scores_by_attempt[scores_by_attempt['Test Name'] == selected_test]

        # Plotting the line chart
        st.write(f"### Score Progression for {selected_test}")
        st.line_chart(selected_test_scores[['Attempt Number', 'Score']].set_index('Attempt Number'))

    except FileNotFoundError:
        st.write("No test attempts have been logged yet.")

# To incorporate this into your Streamlit app, ensure you have a button or a way to call this function

    display_score_by_attempt()





def display_progress_analysis():
    try:
        # Load data from the CSV file
        data = pd.read_csv("test_attempts.csv")

        # For counting attempts by test, consider each unique timestamp per test as one attempt
        attempts_by_test = data.groupby('Test Name')['Timestamp'].nunique().reset_index(name='Attempt Count')

        st.write("### Attempts by Test")
        st.bar_chart(attempts_by_test.set_index('Test Name'))
        
        # Allow users to select a specific test to view detailed error analysis
        test_names = data['Test Name'].unique()
        selected_test = st.selectbox('Select a Test to View Detailed Analysis', test_names)
        display_score_by_attempt(selected_test)
        # Filter data for the selected test
        selected_test_data = data[data['Test Name'] == selected_test]

        # Filter out correct answers to focus on errors for the selected test
        incorrect_attempts = selected_test_data[selected_test_data['Outcome'] == 'Incorrect']

        # Count errors for each question and find the most common incorrect answer
        error_counts = incorrect_attempts['Question Text'].value_counts().reset_index()
        error_counts.columns = ['Question Text', 'Error Count']

        most_common_incorrect = incorrect_attempts.groupby('Question Text')['User\'s Answer'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "Various").reset_index()
        most_common_incorrect.columns = ['Question Text', 'Most Common Incorrect Answer']

        # Merge the two DataFrames
        error_analysis = pd.merge(error_counts, most_common_incorrect, on='Question Text')

        # Get a DataFrame with unique questions and their correct answers for the selected test
        correct_answers = selected_test_data[['Question Text', 'Correct Answer']].drop_duplicates()

        # Merge to include correct answers in the analysis
        final_analysis = pd.merge(error_analysis, correct_answers, on='Question Text')

        # Sort by 'Error Count' to get the questions with the most errors at the top
        final_analysis = final_analysis.sort_values(by='Error Count', ascending=False)

        st.write(f"### Questions with Most Errors, Most Common Incorrect Answer, and Correct Answer for {selected_test}")
        
        for _, row in final_analysis.iterrows():
            st.write(f"**Question:** {row['Question Text']}")
            st.write(f"**Errors:** {row['Error Count']}, **Most Common Incorrect Answer:** {row['Most Common Incorrect Answer']}, **Correct Answer:** {row['Correct Answer']}")

    except FileNotFoundError:
        st.write("No test attempts have been logged yet.")


display_progress_analysis()