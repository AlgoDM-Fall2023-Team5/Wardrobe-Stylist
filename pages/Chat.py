import streamlit as st
from snowflake_list import annotations_list
import openai

snowflake_url = st.secrets.project_snowflake.url


role = """
you are my personal wardrobe assistant who has immense experience in the fashion industry. You know the latest trends and people appreciate you often for your fashion choices. You are also funny and give the best advice based on the event. Now, these are my wardrobe data:
Now, answer only the questions I ask and suggest only from the wardrobe.
Return in the following format:\n
CHOICE :
"{"color: ,clothing type: ,pattern: "}"
REASON:

Please only give me responses in the specified format. Remember, the choice should match the exact keyword from the wardrobe. Take only one option into consideration. Also, try to include a funny thing in the reason based on the occasion. Return the output in json.
below the wardrobe is attached :
"""

def main():
    st.sidebar.title("Chat")
    user_input = st.sidebar.text_input("Enter text:")

    if st.sidebar.button("Submit"):
        st.write(user_input)


# def interact_with_gpt(question, role = role()):
#   """
#   Interacts with GPT-3.5 using the OpenAI API.

#   Args:
#     question: The question to ask GPT-3.5.
#     role: The role to give to GPT-3.5.

#   Returns:
#     The response from GPT-3.5.
#   """
#   openai.api_key = st.secrets.openai.keys

#   # Define the parameters for the request
#   prompt = f"{role}: {question}"
#   temperature = 0.7
#   top_p = 1.0
#   max_tokens = 1024

#   # Send the request to OpenAI
#   response = openai.Completion.create(
#     model="gpt-3.5",
#     prompt=prompt,
#     temperature=temperature,
#     top_p=top_p,
#     max_tokens=max_tokens
#   )

#   # Return the response
#   return response.choices[0].text



if __name__ == "__main__":
    st.title("Stylist Opinion")
    main()
    # Example usage
    
    question = "What is the meaning of life?"
    role = "Philosopher"

    #response = interact_with_gpt_35(question, role)

    #st.write(response)