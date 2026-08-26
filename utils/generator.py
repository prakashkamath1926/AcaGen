from ollama import chat 
from utils.prompts import ANSWER_PROMPT
def generate_answer(question,chunks):
    context="\n\n".join(chunks)
    prompt=ANSWER_PROMPT.format(
        context=context,
        question=question
    )
    response=chat(
        model="qwen3:8b",
        messages=[
            {
                "role":"user",
                "content": prompt
            }
        ]
    )
    return response["message"]["content"]