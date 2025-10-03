"""Interactive AI Q&A Assistant using Gemini"""

import from os { getenv }
import from byllm.llm { Model }

# Load Gemini model with your API key from environment variable
glob llm = Model(
    model_name="gemini/gemini-2.0-flash",
    api_key=getenv("GEMINI_API_KEY"),
    verbose=True
);

"""Ask the LLM a question and return an answer"""
def ask_llm(question: str) -> str by llm();

walker ChatBot {
    has question: str;

    can start with root entry;
    can get_answer with turn entry;
}

node turn {
    has q: str;
}

# --- Walker implementations ---

impl ChatBot.start {
    if not [root --> (`?turn)] {
        next = root ++> turn(self.question);
    } else {
        next = [root --> (`?turn)];
    }
    visit next |> get_answer;
}

impl ChatBot.get_answer {
    if [-->] {
        visit [-->];
    } else {
        print("Q: " + here.q);
        answer = ask_llm(here.q);
        print("Gemini says: " + answer);
        disengage;
    }
}

# --- Run once in CLI mode ---
with entry:__main__ {
    q = input("Ask Gemini (or type 'exit' to quit): ");
    if q != "exit" {
        root spawn ChatBot(q);
    }
}
