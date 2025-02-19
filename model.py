import os
import openai
from transformers import pipeline
from transformers import LlamaForCausalLM, LlamaTokenizer

class LLMProcessor:
    def __init__(self, model_type):
        self.model_type = model_type
        self.auth_token = os.getenv("HUGGINGFACE_TOKEN")
        if model_type == "gpt2":
            self.generator = pipeline("text-generation", model="gpt2")
        elif model_type == "llama":
            self.generator = pipeline("text-generation", model="meta-llama/Llama-2-7b-chat-hf", use_auth_token=self.auth_token)
    
    def call_model(self, prompt):
        if self.model_type == "openai-gpt3":
            openai.api_key = os.getenv("OPENAI_API_KEY")
            try:
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                return str(e)
        elif self.model_type in ["gpt2", "llama"]:
            return self.generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
        else:
            return "Unsupported model."