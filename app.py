import streamlit as st



def load_questions_safely(file_path):
    questions = []
    with open(file_path, "r", encoding='utf-8') as file:
        question_blocks = file.read().strip().split("\n\n")  # Splitting by double newline to separate questions
        
        for block in question_blocks:
            lines = block.split("\n")
            if len(lines) >= 6:  # Ensuring there are enough lines for a question and options
                question_text = lines[0].split(": ")[1] if ": " in lines[0] else lines[0]
                options = [line.split(". ")[1] if ". " in line else line for line in lines[1:5]]
                correct_answer_line = lines[5]
                correct_answer = correct_answer_line.split(": ")[1].strip() if ": " in correct_answer_line else correct_answer_line.strip()
                questions.append({
                    "question": question_text,
                    "options": options,
                    "answer": correct_answer
                })
                
    return questions

questions = load_questions_safely("data/renumbered_questions.txt")



# Function to calculate the score
def calculate_score(questions, user_answers):
    score = 0
    for i, question in enumerate(questions, start=1):
        correct_answer = question['options'][ord(question['answer'].split('.')[0].upper()) - ord('A')]
        if user_answers[i] == correct_answer:
            score += 1
    return score

def app_main(questions):
    st.title("Hola mi Amorcito")

    # Distribute questions among tests
    tests = {f"Test {i+1}": questions[i*10:(i+1)*10] for i in range(5)}
    tests["Test 6"] = questions[50:]  # Last test with the remaining questions

    # Sidebar for test selection
    test_selection = st.sidebar.selectbox("Select a Test", list(tests.keys()))

    # Display questions and options for the selected test
    if test_selection:
        questions = tests[test_selection]
        user_answers = {}
        user_responses = {}  # To store user responses for feedback
        
        for i, question in enumerate(questions, start=1):
            st.write(f"Q{i}: {question['question']}")
            options = question['options']
            answer = st.radio(f"Options for Q{i}", options, key=f"Q{i}")
            user_answers[i] = answer
            correct_option_index = ord(question['answer'][0].upper()) - ord('A')
            correct_answer = question['options'][correct_option_index]
            user_responses[i] = {"question": question['question'], "correct_answer": correct_answer, "user_answer": answer}

        # Submit button with feedback on correct answers
        if st.button('Submit Answers'):
            score = calculate_score(questions, user_answers)
            st.write(f"##### Your score: {score}/{len(questions)}")
            
            if score >= 7:
                st.write('MMMUYYYY BIEEEEEEEEEENNNNNNNNN')
            
            else:
                st.write('#### No te preocupes mi amor, sigue practicando que lo vas a lograr')
    
            st.write("### Correct Answers and Your Responses")
            for i, response in user_responses.items():
                st.write(f"Q{i}: {response['question']}")
                st.write(f"Correct Answer: {response['correct_answer']}")
                if response['user_answer'] == response['correct_answer']:
                    st.success(f"Your answer: {response['user_answer']} ✅")
                else:
                    st.error(f"Your answer: {response['user_answer']} ❌")

# Run the app main function if the script is run directly
if __name__ == "__main__":
    app_main(questions)