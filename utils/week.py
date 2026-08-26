from ollama import chat 
from utils.prompts import WEEK_WISE
def week_wise(topic,chunks):
    context="\n\n".join(chunks)
    prompt=WEEK_WISE.format(
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