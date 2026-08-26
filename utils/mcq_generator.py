from ollama import chat 
from utils.prompts import MCQ_PROMPT
def generate_mcqs(topic,chunks):
    context="\n\n".join(chunks)
    prompt=MCQ_PROMPT.format(
        context=context,
        topic=topic
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