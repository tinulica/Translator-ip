from fastapi import FastAPI
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer
from functools import lru_cache
import torch

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str
    source: str
    target: str

@lru_cache(maxsize=20)
def load_model(src: str, tgt: str):
    model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# Warm up the most common model to avoid cold start errors
load_model("en", "ro")

@app.post("/translate")
async def translate(req: TranslationRequest):
    try:
        tokenizer, model = load_model(req.source, req.target)
        encoded = tokenizer([req.text], return_tensors="pt", padding=True)
        with torch.no_grad():
            generated_tokens = model.generate(**encoded)
        result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return {"translatedText": result}
    except Exception as e:
        return {"error": str(e)}
