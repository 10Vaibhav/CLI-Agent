from dotenv import load_dotenv
from openai import OpenAI
import json
from config.settings import MODEL_NAME
from tools import available_tools
from prompts.system_prompt import SYSTEM_PROMPT
from models.schemas import MyOutputFormat
from utils.helpers import print_welcome_message, check_exit_command, handle_tool_execution
import asyncio
import speech_recognition as sr
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()

recognizer = sr.Recognizer()

async def speak(text: str):
        """Convert text to speech and play it."""
        async with async_client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="coral",
            instructions="Always speak in cheerful manner with full of delight and happy",
            input=text,
            response_format="pcm"
        ) as response:
            await LocalAudioPlayer().play(response)

def main():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 2

        message_history = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

        while True:
            print("Speak Something...")
            audio = recognizer.listen(source=source)

            print("Processing Audio...(STT)")
            text = recognizer.recognize_google(audio)

            print("You Said: ", text)
            
            if check_exit_command(text):
                print("👋 Goodbye! Chat ended.\n\n\n")
                break
            
            message_history.append({"role": "user", "content": text})

            while True:
                response = client.chat.completions.parse(
                    model=MODEL_NAME,
                    response_format=MyOutputFormat,
                    messages=message_history
                )

                raw_result = response.choices[0].message.content
                message_history.append({"role": "assistant", "content": raw_result})
                parsed_result = response.choices[0].message.parsed

                if parsed_result.step == "START":
                    print("🔥", parsed_result.content)
                    continue

                if parsed_result.step == "TOOL":
                    tool_response = handle_tool_execution(
                        parsed_result.tool,
                        parsed_result.input,
                        available_tools
                    )
                    
                    message_history.append({
                        "role": "developer",
                        "content": json.dumps({
                            "step": "OBSERVE",
                            "tool": parsed_result.tool,
                            "input": parsed_result.input,
                            "output": tool_response
                        })
                    })
                    continue

                if parsed_result.step == "PLAN":
                    print("🧠", parsed_result.content)
                    continue

                if parsed_result.step == "OUTPUT":
                    print("🎁", parsed_result.content)
                    asyncio.run(speak(parsed_result.content))
                    print()
                    break

        print("\n\n\n")

if __name__ == "__main__":
    main()