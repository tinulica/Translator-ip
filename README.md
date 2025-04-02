# FastAPI Translator (Railway Ready)

Multilingual translation API using Hugging Face Transformers + OpusMT.

## API Endpoint

POST /translate

Body:
{
  "text": "hello",
  "source": "en",
  "target": "ro"
}

Response:
{
  "translatedText": "Salut"
}

## Deploy to Railway
1. Fork this repo to your GitHub
2. Visit https://railway.app
3. New Project > Deploy from GitHub
4. Done!
