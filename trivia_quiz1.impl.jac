"""Implementation of Trivia Quiz"""

impl QuizGame {
    can start with entry {
        report "Question: " + question;
        # create a turn node and attach correct answer
        spawn here ++> turn(question_text=question, correct_answer=answer);
        take -> check_answer;
    }

    can check_answer with entry {
        if answer == turn.correct_answer {
            report "✅ Correct!";
        } else {
            report "❌ Wrong! The correct answer is " + turn.correct_answer;
        }
    }
}

impl turn {
    can entry {
        report "Turn created with question: " + question_text;
    }
}
