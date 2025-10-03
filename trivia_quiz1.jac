"""A Trivia Quiz Game"""

walker QuizGame {
    has question: str;
    has answer: str;

    def start;
    def check_answer;
}

node turn {
    has correct_answer: str;
    has question_text: str;

    def entry;
}

with entry:__main__ {
    root spawn QuizGame("What is the capital of France?", "Paris");
    root spawn QuizGame("What is 2 + 2?", "4");
}
