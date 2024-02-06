import streamlit as st

from datetime import datetime

def generate_motivational_greetings():
    greetings = {}
    for hour in range(24):
        if hour == 5:
            greeting = "¡Arriba temprano, Laurita! Cada minuto de estudio te acerca a tu meta."
        elif hour == 6:
            greeting = "Un nuevo amanecer, una nueva oportunidad para superarte. ¡Vamos por ello!"
        elif hour == 7:
            greeting = "Recuerda, el éxito es la suma de pequeños esfuerzos repetidos día tras día."
        elif hour == 8:
            greeting = "Define tus objetivos de estudio para hoy. Planificar es el primer paso hacia el éxito Laurita."
        elif hour == 9:
            greeting = "Sumérgete en tus estudios, Laurita. Cada página te acerca a tu sueño."
        elif hour == 10:
            greeting = "Tómate un momento para revisar lo aprendido amor. Cada repaso fortalece tu memoria."
        elif hour == 11:
            greeting = "La perseverancia es tu mejor amiga en este viaje. Sigue adelante jefita."
        elif hour == 12:
            greeting = "Hora de una pausa activa. Recarga energías amor."
        elif hour == 13:
            greeting = "Renueva tu enfoque post-almuerzo. Cada sesión de estudio cuenta."
        elif hour == 14:
            greeting = "Enfrenta los temas difíciles ahora, Laurita. Es en los desafíos donde más crecemos."
        elif hour == 15:
            greeting = "¿Sientes cansancio? Cambia de tema de estudio para mantener la mente fresca."
        elif hour == 16:
            greeting = "Recuerda, el conocimiento es poder. Cada hora de estudio te hace más fuerte."
        elif hour == 17:
            greeting = "Revisa tus avances del día. Cada pequeño logro te acerca a tu objetivo."
        elif hour == 18:
            greeting = "El esfuerzo de hoy es la recompensa de mañana. Estás construyendo tu futuro, Laurita."
        elif hour == 19:
            greeting = "Desconecta un momento. Una mente descansada es más productiva."
        elif hour == 20:
            greeting = "Planifica tu sesión de estudio para mañana. Dormirás mejor con un plan claro."
        elif hour == 21:
            greeting = "Reflexiona sobre lo aprendido hoy. Cada día te conviertes en una mejor versión de ti misma."
        elif hour == 22:
            greeting = "Es hora de descansar, Amor. El sueño reparador es clave para el aprendizaje."
        elif hour == 23:
            greeting = "Cierra este día con gratitud por el esfuerzo realizado. Mañana es otro día para brillar."
        elif hour == 0 or hour == 1:
            greeting = "Que tus sueños te inspiren, Laurita. El descanso es parte del camino hacia el éxito."
        elif hour == 2 or hour == 3:
            greeting = "Incluso en la quietud de la noche, tu determinación sigue brillando. Descansa bien."
        elif hour == 4:
            greeting = "Pronto amanecerá, un nuevo día lleno de posibilidades y aprendizajes te espera."
        greetings[hour] = greeting
    return greetings



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

questions = load_questions_safely("data/updated_renumbered_questions.txt")



# Function to calculate the score
def calculate_score(questions, user_answers):
    score = 0
    for i, question in enumerate(questions, start=1):
        correct_answer = question['options'][ord(question['answer'].split('.')[0].upper()) - ord('A')]
        if user_answers[i] == correct_answer:
            score += 1
    return score

def app_main(questions):
    greetings = generate_motivational_greetings()

# Get the current hour
    current_hour = datetime.now().hour

    greeting_message = greetings.get(current_hour, "Keep pushing forward, Laura. Every step is progress.")
    st.title(greeting_message)


    # Distribute questions among tests
    #tests = {f"Test {i+1}": questions[i*10:(i+1)*10] for i in range(5)}
    tests = {f"Test {i+1}": questions[i*10:(i+1)*10] for i in range(10)}
    tests["Test 11"] = questions[100:]  # Last test with the remaining questions

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