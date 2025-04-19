import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI


load_dotenv()

llm = ChatOpenAI(temperature=0)

def is_message_inappropriate(message: str, banned_topics: list) -> bool:
    if not banned_topics:
        return False

    prompt = (
        f"Voici un message utilisateur : \"{message}\"\n"
        f"Les sujets interdits sont : {', '.join(banned_topics)}.\n"
        "Le message traite-t-il d’un sujet interdit ? Réponds uniquement par OUI ou NON."
    )

    try:
        response = llm.predict(prompt)
        return "oui" in response.lower()
    except Exception as e:
        print(f"Erreur lors de l'appel LLM : {e}")
        return False
