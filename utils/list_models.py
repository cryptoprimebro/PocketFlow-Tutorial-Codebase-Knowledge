import os
import ssl
import certifi

import dotenv

dotenv.load_dotenv()

# Переопределяем ssl.create_default_context так, чтобы он не вызывал load_default_certs
_orig_create_default_context = ssl.create_default_context

def patched_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=certifi.where())
    return context

ssl.create_default_context = patched_create_default_context

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

models = genai.list_models()
for model in models:
    print(f"{model.name} | generation: {model.supported_generation_methods}")