import openai

class ChatInterface:
    def __init__(self, api_key):
        openai.api_key = 'sk-XNyK3X5f1Z1V1JhiwQva--oyHGVtqgFU7kXrlCABzaT3BlbkFJ09eRS0fmY65c_7uqObTokzeHOpfD3G99FaoYuhGb4A'

    def get_instruction(self, prompt):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error fetching instruction from ChatGPT: {e}")
            return ""
