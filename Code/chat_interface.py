import openai

class ChatInterface:
    def __init__(self, api_key):
        openai.api_key = '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'

    def get_instruction(self, prompt):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt='Test migration issue',
                max_tokens=50
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error fetching instruction from ChatGPT: {e}")
            return ""


#keyopenai.api_key = 'your_openai_api_key_here' response = openai.Completion.create(     engine="text-davinci-003",     prompt="Test migration issue",     max_tokens=50 ) print(response.choices[0].text.strip())