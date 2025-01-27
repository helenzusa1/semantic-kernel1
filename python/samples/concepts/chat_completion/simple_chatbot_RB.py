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
You are a chat bot. Your mission is to generate Ruby code to create 2D/3D images, and edit the images. 
You interact with the user to understand how the user wants to generate the image and edit the image. 
For the Ruby code part, you give clear indication of starting line and ending line

# Start of Ruby code
ruby code
# End of Ruby code

For the code portion, you need to file with path C:/Users/helenzeng/computer-vision/Ruby/3d-image-test.rb.
"""

# Create a chat history object with the system message.
chat_history = ChatHistory(system_message=system_message)

def code_generation(my_response):
    # Convert the response to a string
    rb_code_str = str(my_response)

    # Extract the HTML code block
    ruby_match = re.search(r'# Start of Ruby code(.*?)# End of Ruby code', rb_code_str, re.DOTALL)
    if ruby_match:
        ruby_code = ruby_match.group(1).strip()

        # Specify the folder path where you want to save the file
        folder_path = 'C:/Users/helenzeng/computer-vision/Ruby/'
        file_path = os.path.join(folder_path, '3d-image-test.rb')

        try:
            # Save the HTML code to a file in the specified folder
            with open(file_path, 'w') as file:
                file.write(ruby_code)
            print(f"Ruby code has been saved to {file_path}")
        except FileNotFoundError:
            print(f"Error: The directory {folder_path} does not exist.")
        
        # Respond back the other text to the user
        other_text = rb_code_str.replace(ruby_code, '').strip()
        if other_text:
            print(other_text)
    else:
        # Respond back the entire response if no HTML code block is found
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
