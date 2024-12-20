# Copyright (c) Microsoft. All rights reserved.

import asyncio
import sys
import re
import os

sys.path.append("C:\\Users\\helenzeng\\My-SK\\python\\")

from samples.concepts.setup.chat_completion_services import (
    Services,
    get_chat_completion_service_and_request_settings,
)
from semantic_kernel.contents import ChatHistory

# This sample shows how to create a chatbot. This sample uses the following two main components:
# - a ChatCompletionService: This component is responsible for generating responses to user messages.
# - a ChatHistory: This component is responsible for keeping track of the chat history.
# The chatbot in this sample is called Mosscap, who responds to user messages with long flowery prose.


# You can select from the following chat completion services:
# - Services.OPENAI
# - Services.AZURE_OPENAI
# - Services.AZURE_AI_INFERENCE
# - Services.ANTHROPIC
# - Services.BEDROCK
# - Services.GOOGLE_AI
# - Services.MISTRAL_AI
# - Services.OLLAMA
# - Services.ONNX
# - Services.VERTEX_AI
# Please make sure you have configured your environment correctly for the selected chat completion service.
chat_completion_service, request_settings = get_chat_completion_service_and_request_settings(Services.AZURE_OPENAI)

# This is the system message that gives the chatbot its personality.
system_message = """
You are a chat bot. Your mission is to generate JavaScript code to create 2D/3D images,
and edit the images. You interact with the user to understand how the user wants to 
generate the image and edit the image. You include THREE.js library. For the code generated, 
you need to save to a file in a designated folder.
"""

# Create a chat history object with the system message.
chat_history = ChatHistory(system_message=system_message)

def code_generation(my_response):
    # Extract the text content from each ChatMessageContent object
    #js_code_list = [message.content for message in my_response]

    # Convert the list to a string
    js_code_str = str(my_response)

    # Extract the HTML code block
    html_match = re.search(r'(<\!DOCTYPE html>.*?</html>)', js_code_str, re.DOTALL)
    if html_match:
        html_code = html_match.group(1).strip()

        # Specify the folder path where you want to save the file
        folder_path = 'C:/Users/helenzeng/computer-vision/JavaScript/'
        file_path = os.path.join(folder_path, '3d-image.html')

        # Save the HTML code to a file in the specified folder
        with open(file_path, 'w') as file:
            file.write(html_code)
        print(f"HTML code has been saved to {file_path}")
    else:
        #print("No HTML code block found in the output.")
        print(f"{my_response}")

async def chat() -> bool:
    try:
        user_input = input("User:> ")
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False

    if user_input == "exit":
        print("\n\nExiting chat...")
        return False

    # Add the user message to the chat history so that the chatbot can respond to it.
    chat_history.add_user_message(user_input)

    # Get the chat message content from the chat completion service.
    response = await chat_completion_service.get_chat_message_content(
        chat_history=chat_history,
        settings=request_settings,
    )
    if response:       
        #print(f"Agent:> {response}")
        print("Agent:> \n")
        code_generation(response)

        # Add the chat message to the chat history to keep track of the conversation.
        chat_history.add_message(response)

    return True


async def main() -> None:
    # Start the chat loop. The chat loop will continue until the user types "exit".
    chatting = True
    while chatting:
        chatting = await chat()

    # Sample output:
    # User:> Why is the sky blue in one sentence?
    # Mosscap:> The sky is blue due to the scattering of sunlight by the molecules in the Earth's atmosphere,
    #           a phenomenon known as Rayleigh scattering, which causes shorter blue wavelengths to become more
    #           prominent in our visual perception.


if __name__ == "__main__":
    asyncio.run(main())
