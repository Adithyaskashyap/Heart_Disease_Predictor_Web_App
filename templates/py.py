import google.generativeai as genai

genai.configure(api_key="AIzaSyCEq1MU8DvpMMQg8TmAtFid4yhHgVo9U1E")

print("\nAVAILABLE MODELS:\n")

for model in genai.list_models():

    if "generateContent" in model.supported_generation_methods:

        print(model.name)