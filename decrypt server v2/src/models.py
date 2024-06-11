from openai import OpenAI, AsyncOpenAI
from config import OPENAI_API_KEY
from rag_config import VectorStore

class Model(VectorStore):
    def __init__(self) -> None:
        VectorStore.__init__(self)
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.ref = self.process_file()

    def get_completion(self, prompt, client_instance, model="gpt-3.5-turbo"):
        # context = url = ''
        id = self.retriever(prompt)[1]
        context = self.ref[id]['text']
        url = self.ref[id]['url']

        sys = f"""You are a helpful assistant guiding the user through querying their cryptocurrency wallet. 
            You give concise but helpful answers. If you are using bullet points in your response, limit them to three.
            Take the users context and use it to increase your understanding of the cryptocurrency domain.
            Think step by step. If you do not know the answer, then say you don't know.
            For any context you've used to inform your response, ALWAYS provide the corresponding url as a helpful link for the user to refer to.

            Context: {context}
            Url: {url}
            """

        messages = [
            {
            "role": "system", 
            "content" : sys
            }
            ,
            {
                "role": "user", "content": prompt
                }
                    ]
        
        response = client_instance.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=500,
            temperature=0,
        )
        return response.choices[0].message.content

class Prompters:
    def CoT_prompt_engineer(self, user_input, client_instance, model = "gpt-3.5-turbo"):

        # prompt = f"The user said: '{user_input}'. Is the user requesting a specific action (like checking their balance or P&L), or are they asking a general question or making a statement? Please respond with 'action' or 'general'."
        featured_prompts = {
            'Is this a good p&l value?': 'general',
            'What volatility should I be looking for?': 'general',
            'What is the risk of BTC in the last year?': 'action',
            'What is the sharpe ratio of bitcoin within the last year': 'action',
            'What is the volatility of XRP within the last year': 'action',
            'What is the sharpe ratio of bitcoin within the last 6 months': 'action',
            'What is the risk ratio of XRP within the last 6 months': 'action',
            'How does one interpret sharpe ratio?' : 'general',
            'How does on understand and interpret risk/volatility?' : 'general',
            'Which tokens out of those are the least in value?' : 'general',
            'Which tokens out of those are the greatest in value?' : 'general',
            'I want to see the value and balance for all my tokens' : 'action',
            'all my tokens' : 'action'
        }

        prompt = "Consider the following examples to understand user intent:\n"
        for example, category in featured_prompts.items():
            prompt += f"- '{example}' is a {category} query.\n"
        prompt += f"\nThe user said: '{user_input}'. Is the user requesting a specific action or are they asking a general question? Respond with 'action' or 'general'."

        messages = [{"role": "user", "content": prompt}]
        response = client_instance.chat.completions.create(
            model = model,
            messages = messages,
            max_tokens = 500,
            temperature = 0,
        )

        chatbot_decision = response.choices[0].message.content.strip().lower()

        if "action" in chatbot_decision:
            return "yes" 
        else:
            return "no" 