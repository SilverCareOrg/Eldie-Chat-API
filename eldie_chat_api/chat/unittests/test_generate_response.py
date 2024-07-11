import pytest
import time
import os

from eldie_chat_api.chat.utils import generate_response
from openai import OpenAI
# Read OpenAI API key from "../../eldie_chat_api/.env" file
from dotenv import load_dotenv
load_dotenv("../../eldie_chat_api/.env")

@pytest.mark.parametrize( "user, previous_chat, message", [
    ( "user-generate-response-test1", "What's the weather like?", "The weather is sunny."),
    ( "user-generate-response-test2", "Care este temperatura azi?", "Temperatura este de 25 de grade."),
    ( "user-generate-response-test3", "Tell me a joke.", "Why did the chicken cross the road? To get to the other side!"),
    ( "user-generate-response-test4", "What's the news today?", "Today's news includes..."),
    ( "user-generate-response-test5", "Ce zi este azi?", "Azi este vineri."),
    ( "user-generate-response-test6", "What time is it?", "It's 3 PM."),
    ( "user-generate-response-test7", "Can you help me?", "Of course, how can I assist you?"),
    ( "user-generate-response-test8", "What can you do?", "I can assist with various tasks..."),
    ( "user-generate-response-test9", "Cum te simți?", "Mă simt foarte bine."),
    ( "user-generate-response-test10", "Where are you from?", "I am a virtual assistant."),
    ( "user-generate-response-test11", "What's 2+2?", "2+2 is 4."),
    ( "user-generate-response-test12", " ", "I recommend 'To Kill a Mockingbird'."),
    ( "user-generate-response-test13", "Ce vârstă ai?", "Nu am o vârstă, sunt un asistent virtual."),
    ( "user-generate-response-test14", "What movies are out?", "Currently, the top movies are..."),
    ( "user-generate-response-test15", "Who won the game?", "The home team won the game."),
    ( "user-generate-response-test16", "What's for dinner?", "How about some pasta?"),
    ( "user-generate-response-test17", "Cine ești tu?", "Sunt Eldie, asistentul tău virtual."),
    ( "user-generate-response-test18", "Tell me about space.", "Space is vast and full of stars."),
    ( "user-generate-response-test19", "What's the capital of France?", "The capital of France is Paris."),
    ( "user-generate-response-test20", "Unde este biblioteca?", "Biblioteca este pe strada principală."),
    ( "user-generate-response-test21", "What is AI?", "AI stands for Artificial Intelligence."),
    ( "user-generate-response-test22", "What do you think?", "I think it's a great idea."),
    ( "user-generate-response-test23", "What's your favorite color?", "I don't have a favorite color."),
    ( "user-generate-response-test24", "Cum e vremea?", "Vremea este frumoasă azi."),
    ( "user-generate-response-test25", "Can you sing?", "I can’t sing, but I can tell you a joke.")
])
def test_generate_response(user, previous_chat, message):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = generate_response(openai_client, user, previous_chat, message)
    assert isinstance(response, str)
    assert len(response) > 0
    print(f"Response for {user} -> {response}")

if __name__ == "__main__":
    pytest.main([__file__])
