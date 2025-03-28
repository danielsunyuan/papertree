import os
import openai
import traceback

openai.api_key = os.environ["OPENAI_API_KEY"]

def essayAI(text):

    try:
        # Configuration
        model_engine = "text-davinci-003"
        temperature = 0.5 # Deterministic (0.0) to Random (1.0)
        choices = 1

        # Send the concatenated response to the API
        prompt = f"SENTENCES: {text}\
            \n\
            \n\
            Write a science paper essay summary from the SENTENCES,\
            Essay length at least 400 words."

        # Call the API and get the response
        response = openai.Completion.create(
            engine=model_engine, 
            prompt=prompt, 
            max_tokens=1000, 
            temperature=temperature,
            n=choices
            )

        return response["choices"][0]["text"]
    except Exception as e:
        print(f"An error occurred in essayAI: {e}")
        traceback.print_exc()

def chatAI(user_text, paper):
    try:
        # Configuration
        model_engine = "text-davinci-003"
        temperature = 0.9 # Deterministic (0.0) to Random (1.0)
        choices = 1

        # Send the concatenated response to the API
        additional_prompt = 'In regards to the paper...'
        designed_prompt = f'The following is a conversation with an AI assistant. \
        The assistant will only answer questions about the paper.\n\
        """\n\
        PAPER: {paper}\
        """\n\
        \n\
        \n\
        Human: {user_text}\
        AI:'

        start_sequence = "\nAI:"
        restart_sequence = f"\nHuman: {additional_prompt} "

        response = openai.Completion.create(
        model=model_engine,
        prompt=designed_prompt,
        temperature=temperature,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["Human:", " AI:"]
        )

        # Extract the generated response from the API's response
        print(response.choices[0].text.strip())
        return response.choices[0].text.strip()

    except Exception as e:
        print(f"An error occurred in chatAI: {e}")
        traceback.print_exc()