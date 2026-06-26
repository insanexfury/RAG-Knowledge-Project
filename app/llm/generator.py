from openai import OpenAI
from app.core.config import settings

class Generator:
    def __init__(self):
        """"""
        self.client = OpenAI(api_key = settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        
    def generate(self, query: str,  retrieved_chunks:list[dict]) ->str:
        """"""
        response = self.client.chat.completions.create(model ="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": "You are answering questions about a document.If the user asks for- a summary- an overview- what the document is aboutthen synthesize information from all retrieved passages into a concise summary of the entire document rather than focusing on a single detail."},
                {
                "role":"user",
                "content": self._build_prompt(query,retrieved_chunks)   
                }],
            temperature=0)
        return response.choices[0].message.content 
    
    def _build_prompt(self, query:str ,retrieved_chunks:list[dict]) ->str:
        """"""
        prompt = ""
        for i,chunk in enumerate(retrieved_chunks):
            prompt = prompt +f"{i+1}Source:{chunk['metadata']['source']} Page Number:{chunk['metadata']['page_number']} \n {chunk['text']}\n\n"
        prompt =prompt+f"\n Question: {query}"
        return prompt
        
        
    
