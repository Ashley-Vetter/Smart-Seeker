import openai
import base64
import json

class ChatInterface:
    keyword = " Keyword : "
    searchprompt = ("In a simple True or False, based off of the keyword chosen, please analyze if the following contains "
                    "anything remotely similar, is in the same environment where one could expect to find the keyword, "
                    "there is a possibility that the keyword can be located in that specific area I.E. think about the objects "
                    "detected and form a conclusion about where in which room the item could be or if the detected object is "
                    "a synonym for the word, also provide a reason why. Remember that we are searching for the keyword. "
                    "The response should be in the format of: Boolean | Reason why")
    keywordGathering = ("From this list of responses, gather for me the object that is the closest variant towards what we are searching for, only return the object name and or similiar objects (synonoums even not found in the list) seperate them with a | : person bicycle car motorcycle airplane bus train truck boat traffic light fire hydrant street sign stop sign parking meter bench bird cat dog horse sheep cow elephant bear zebra giraffe hat backpack umbrella shoe eye glasses handbag tie suitcase frisbee skis snowboard sports ball kite baseball bat baseball glove skateboard surfboard tennis racket bottle plate wine glass cup fork knife spoon bowl banana apple sandwich orange broccoli carrot hot dog pizza donut cake chair couch potted plant bed mirror dining table window desk toilet door tv laptop mouse remote keyboard cell phone microwave oven toaster sink refrigerator blender book clock vase scissors teddy bear hair drier toothbrush hair brush User response : ")
    
    lastResponse = ""
    
    userPrompt = ""
    
    ExplainLocationPrompt = "Find and describe for me the location of the objects in the image similiar to the keyword identified, please give clear instructions and explain where the user might find the keyword(s) identified, the keyword is synonoums or words closly related to the main object, ensure the answer is short and sweet, give only an explanation of where the object is, don't provide any formatting, do not bring up any additional wording from the keywords, only focus on the task and explain it as detailed as possible, be as detailed as possible in your explanation:"

    api_key = "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"


    fullDroneControlMessage = '''
        You must find the object described within Keyword(s), you are in control of a drone and must navigate the area, 
        describe what you see, what you think you should do based on the information present in the picture 
        and formulate a plan to continue searching the area for the object, 
        afterwards execute any of the following python functions, 
        keep in mind you are a drone and can be easily damaged, keep  your movements small and precise, 
        don't overextend yourself and ensure that safety is first, in other words AVOID WALLS AND OTHER OBJECTS,
        distances are in CM, don't move twice, the functions are programmed to only take one command per movement, 
        a new image is only taken once the movement is complete, see the list below for all commands:

        def move_down(self, distance=20):
            self.tello.move_down(distance)

        def move_forward(self, distance=75):
            self.tello.move_forward(distance)

        def rotate_clockwise(self, angle=45):
            self.tello.rotate_clockwise(angle)

        def rotate_counter_clockwise(self, angle=45):
            self.tello.rotate_counter_clockwise(angle)

    Execute your command in the following JSON

    {
        "logic": "Logic reasoning",
        "ReasoningToPassOn" : "Give a message to the next query to assist in finding the object, a sort of message from beyond to assist",
        "python_code": {[
            "CodeSnippet":"String of code"
            ]
        }
    }
    
    '''
    ##def move_back(self, distance=75):
       #self.tello.move_back(distance)
    previousLogic = []
    previousReasoning = []
    previousCommands = []
    
    def __init__(self, api_key):
        openai.api_key = api_key

    def checkIfImageContainsSearchKeyword(self, prompt):
        try:
            lekka = self.__class__.searchprompt + self.__class__.keyword + " " + prompt
            openai.api_key = self.__class__.api_key
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": lekka}
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            self.__class__.lastResponse = response.choices[0].message.content
            parts = response.choices[0].message.content.split('|', 1)
            if len(parts) == 2:
                boolean_part = parts[0].strip()
                message_part = parts[1].strip()
                return boolean_part, message_part
            else:
                return False, response.choices[0].message.content
        except Exception as e:
            print(f"Error fetching instruction from ChatGPT: {e}")
            return ""
        
    def findSimiliarKeywords(self, prompt):
        try:
            search_prompt = self.__class__.ExplainLocationPrompt + "''" + prompt + "''"
            openai.api_key = self.__class__.api_key
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": search_prompt}
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            self.__class__.keyword = "Keyword(s) : (" + response.choices[0].message.content + ")"
        except Exception as e:
            print(f"Error fetching instruction from ChatGPT: {e}")
            return ""
        
    def findObject(self, img):
        try:
            openai.api_key = self.__class__.api_key
            search_prompt = self.__class__.ExplainLocationPrompt + self.__class__.keyword + " Last user resoponse "+ self.__class__.userPrompt + " Last queried response : " + self.__class__.lastResponse
            base64_image = base64.b64encode(img).decode("utf-8")
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": search_prompt},
                    { "role": "user", "content": [
                            {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                            }
                        ] 
                    },
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error fetching instruction from ChatGPT: {e}")
            return ""
        
 
        
    def autoSearch(self, img):
        try:
            openai.api_key = self.__class__.api_key
            search_prompt = self.__class__.fullDroneControlMessage + "\n\r \n\r" + self.__class__.keyword + " Last user resoponse "+ self.__class__.userPrompt
            
            addition = self.create_search_prompt()
            
            search_prompt += addition
            
            base64_image = base64.b64encode(img).decode("utf-8")
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": search_prompt},
                    { "role": "user", "content": [
                            {
                            "type": "image_url",
                            "image_url": 
                                {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ] 
                    },
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={
                    "type": "json_object"
                }
            )
            
            data = json.loads(response.choices[0].message.content)

            logic = data.get("logic")
            reasoning = data.get("ReasoningToPassOn")
            code_snippet = data.get("python_code", {}).get("CodeSnippet")
            
            print(response.choices[0].message.content)
            
            self.previousLogic.append(logic)
            self.previousReasoning.append(reasoning)
            self.previousCommands.append(code_snippet)
            
            return code_snippet
        except Exception as e:
            print(f"Error fetching instruction from ChatGPT: {e}")
            return ""
        
    def create_search_prompt(self):
        all_entries = (self.previousLogic + self.previousReasoning + self.previousCommands)[-5:]

        formatted_entries = ""
        for i, entry in enumerate(all_entries, start=1):
            if i == len(all_entries):
                formatted_entries += f"Last entry (IMPORTANT)\n{entry}\n"
            else:
                formatted_entries += f"{i}. {entry}\n"

        # Final search_prompt string with formatted entries
        search_prompt = f"Search Prompt:\n\n{formatted_entries}"
        return search_prompt
