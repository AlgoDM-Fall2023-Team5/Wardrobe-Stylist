import streamlit as st
from snowflake_list import annotations_list
from openai import OpenAI
import json
from macys_items import fetch_product_info

snowflake_url = st.secrets.project_snowflake.url
# role ######################
wardrobe_list = annotations_list(snowflake_url)
role = """
you are my personal wardrobe assistant who has immense experience in the fashion industry. You know the latest trends and people appreciate you often for your fashion choices. You are also funny and give the best advice based on the event. Now, these are my wardrobe data:
Now, answer only the questions I ask and suggest only from the wardrobe.\n {wardrobe_list}
Return in the following format:\n.
"Top : (color: ,clothing type: ,pattern:), 
Bottom : (color: ,clothing type:,pattern:) 
Reason:"\n 
Please only give me responses in the specified format.No spelling error in keys. Remember, the choice should match the exact keyword from the wardrobe. Also, try to include a funny thing in the reason based on the occasion. Return the output in json only.
If any questions other than fashion are asked kindly reply in your words you are not able to. 
""".format(
    wardrobe_list="\n".join(wardrobe_list)
)
Gender = "Men"

def main():
    st.sidebar.title("Chat")
    user_input = st.sidebar.text_area("Enter text:")

    if st.sidebar.button("Submit"):
        return user_input


def interact_with_gpt(question, key, role=role):
    """
    Interacts with GPT-3.5 using the OpenAI API.

    Args:
      question: The question to ask GPT-3.5.
      role: The role to give to GPT-3.5.

    Returns:
      The response from GPT-3.5.
    """

    api_key = key
    client = OpenAI(api_key=api_key)

    # Define the parameters for the request
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": question},
    ]
    temperature = 0.3

    # Send the request to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, temperature=temperature
    )

    answer = response.choices[0].message.model_dump_json()
    # Return the response
    return answer


if __name__ == "__main__":
    st.title("Stylist Opinion")

    # question ###################
    openai_key = openai_key_input = st.sidebar.text_input("Enter your OpenAI Key :")

    question = main()

    # handling None while display
    if question is None:
        st.write(
            """:red[Please] :orange[provide] :green[details] :blue[about] :violet[your] :gray[outfit.]"""
        )

    else:

        response = interact_with_gpt(question=question, key=openai_key)
        # Convert the response to a JSON object
        response_json = json.loads(json.loads(response)['content'])
        # Access the specific content you need
        #content = json.loads(response_json["content"])
        
        st.write("Top Wear")
        st.write(response_json['Top'])
        st.write("Bottom Wear")
        st.write(response_json['Bottom'])
        st.write("Reason")
        st.write(response_json['Reason'])


        # Recommendations
        st.header("Top Recommendations:")
        top_recommendations = fetch_product_info(response_json['Top']['color'],
                                                  response_json['Top']['clothing type'],
                                                  "outerwear",
                                                  response_json['Top']['pattern'],
                                                  Gender)
        if top_recommendations:
            count = 1
            for product in top_recommendations:
                st.write(f"Product {count}: [link]"+"www.macys.com"+f"{product['product_url']}")
                count = count + 1
        else:
            st.write("Error Retrieving Recommendations")


        st.header("Bottom Recommendations:")
        Bottom_recommendations = fetch_product_info(response_json['Bottom']['color'],
                                                  response_json['Bottom']['clothing type'],
                                                  response_json['Bottom']['pattern'],
                                                  Gender)
        
        if Bottom_recommendations:
            count = 1
            for product in Bottom_recommendations:
                st.write(f"Product {count}: [link]"+"www.macys.com"+f"{product['product_url']}")
                count = count + 1
        else:
            st.write("Error Retrieving Recommendations")



