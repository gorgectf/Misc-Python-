import logging, os
from random import randint
logging.basicConfig(level=logging.INFO, filename='quizgame.log', format='%(asctime)s :: %(levelname)s :: Module %(module)s :: Line No %(lineno)s :: %(message)s')

quiz: dict[str] = {}
qa_dict: dict[str] = {
    "What is the capital of France?": "Paris",
    "What is 2 + 2?": "4",
    "Who wrote '1984'?": "George Orwell",
    "What is the boiling point of water in Celsius?": "100",
    "What is the chemical symbol for gold?": "Au",
    "Who painted the Mona Lisa?": "Leonardo da Vinci",
    "What planet is known as the Red Planet?": "Mars",
    "What is the largest ocean on Earth?": "Pacific Ocean",
    "What gas do plants absorb from the atmosphere?": "Carbon dioxide",
    "What language is primarily spoken in Brazil?": "Portuguese"
}

def input_questions_answers() -> bool:
    local_quiz = quiz

    if len(quiz) >= 0:
        answer: any = None
        question: any = None
        q_present: bool = True
        a_present: bool = True
        
        while q_present:
            question = input(f"Input a valid question {len(local_quiz)}: ")

            if len(question) > 0 and isinstance(question, str):
                for q in local_quiz.keys():
                    if q == question:
                        print("Question already present, input another.")
                        break
                else:
                    print("Question not present, proceeding...")
                    q_present = False
            else:
                print("A valid question must not be nothing, and be a string.")

        while a_present:
            answer = input("Input a valid answer to the question: ")

            if len(answer) > 0 and isinstance(answer, str):
                a_present = False
            else:
                print("A valid answer must not be nothing, and be a string.")

        quiz.update({question: answer})

        if question in quiz:
            logging.debug("Quiz dict appended to successfully")
            return True
        else:
            logging.warning("Quiz dict was not appended to!")
            quit()

def compare_answer(q, a) -> bool:
    validation: int = 0

    if isinstance(q, str):
        validation += 1
    
    if isinstance(a, str):
        validation += 1

    if len(q) > 0:
        validation += 1
    
    if len(a) > 0:
        validation += 1

    if validation == 4:
        right_answer = quiz[q]
        a = a.lower()
        right_answer = right_answer.lower()

        if right_answer == a : return True
        logging.info(f"User answered correctly to {q} with answer {a}!")
        return False
    else:
        logging.info(f"User input answer incorrect validation. Score: {validation}")
        return False
    
def generate_random_question(last_qes=None) -> str:
    try:
        questions: list[str] = list(quiz.keys())
        random_question: str = questions[randint(0, randint(0, len(quiz) - 1))]

        while random_question == last_qes:
            guess = randint(0, len(quiz) - 1)
            throwoff = max(randint(0, guess), randint(0, guess))
            random_question = questions[throwoff]

        logging.debug(f"Random question is {random_question}")
        return random_question
    except Exception as exc:
        print(exc)

def main() -> bool:
    example_q_ask: any = input("Use example quiz? Y/N ")
    if example_q_ask.upper() == 'Y':
        quiz.update(qa_dict)

    if len(quiz) <= 0:
        logging.debug("Quiz is empty, asking user for input")
        print("Quiz is empty, please enter in questions.")

        while True:
            input_questions_answers()
            ask: any = input("Continue inputting? Y/N: ")

            if isinstance(ask, str):
                if ask.upper() == 'Y':
                    continue
                else:
                    print("Finished inputting questions.")
                    break
            
    playing: bool = True
    score: int = 0
    print("Beginning quiz!")

    while playing:
        last_question = None
        qes: function = generate_random_question(last_question)
        print(qes)
        ans: any = input("Answer (Not case sensitive): ")
        result: bool = compare_answer(qes, ans)

        if result:
            score += 1
            print(f"You were right! Score is now {score}.")
        else:
            print(f"You were wrong. Score remains at {score}.")
            print(f"Correct answer was {quiz[qes]}")

        quitask = input("Quit? Y/N")
        logging.info("Cleared screen.")
        os.system('cls' if os.name == 'nt' else 'clear')

        last_question = qes

        if quitask.upper() == 'Y':
            quit()

    """
        exceptionraise = input("y or n")
        if exceptionraise == "y":
            raise Exception
    """
    return True

logging.debug("Running main loop...")
main()