from ollama import chat 
from utils.prompts import NOTES_PROMPT
def generate_notes(topic,chunks):
    context="\n\n".join(chunks)
    prompt=NOTES_PROMPT.format(
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