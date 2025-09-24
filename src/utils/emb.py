from openai import OpenAI
from ..config import cfg

client = OpenAI(api_key=cfg.openai_key)

def embed(text:str)->list[float]:
    r = client.embeddings.create(model="text-embedding-3-small", input=text)
    return r.data[0].embedding