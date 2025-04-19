from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
banned_topics = []

class Topic(BaseModel):
    subject: str

@app.get("/rules", response_model=List[str])
def get_rules():
    return banned_topics

@app.post("/rules")
def add_rule(topic: Topic):
    if topic.subject in banned_topics:
        raise HTTPException(status_code=400, detail="Sujet déjà banni")
    banned_topics.append(topic.subject)
    return {"message": "Sujet ajouté"}

@app.delete("/rules")
def remove_rule(topic: Topic):
    if topic.subject not in banned_topics:
        raise HTTPException(status_code=404, detail="Sujet introuvable")
    banned_topics.remove(topic.subject)
    return {"message": "Sujet supprimé"}
