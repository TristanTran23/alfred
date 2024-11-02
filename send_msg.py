import os
from dotenv import load_dotenv
from twilio.rest import Client
from typing import List, Dict
from openai import OpenAI

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)
alfred = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_conversation_history(account_sid: str, auth_token: str, phone_number: str) -> List[Dict]:
    
    messages = client.messages.list(
        to=phone_number,
        limit=1000
    )
    
    messages_from = client.messages.list(
        from_=phone_number,
        limit=1000
    )
    
    all_messages = messages + messages_from
    
    all_messages.sort(key=lambda x: x.date_sent)
    
    conversation = []
    for msg in all_messages:
        conversation.append({
            'date': msg.date_sent.strftime('%Y-%m-%d %H:%M:%S'),
            'from': msg.from_,
            'to': msg.to,
            'body': msg.body,
            'status': msg.status,
            'direction': 'incoming' if msg.to == phone_number else 'outgoing'
        })
    
    return conversation

def print_conversation(conversation: List[Dict]) -> None:
    for msg in conversation:
        direction = "→" if msg['direction'] == 'outgoing' else "←"
        print(f"[{msg['date']}] {direction} From: {msg['from']}")
        print(f"    To: {msg['to']}")
        print(f"    {msg['body']}")
        print(f"    Status: {msg['status']}")
        print("-" * 50)

def prompt_gpt (prompt: str) -> str:
    output = alfred.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an event organizer for a group of friends. You are helping them to find a place and time that works for everyone. You "},
            {"role": "user", "content": "Hello"}
        ]
    )
    print(output.choices[0].message.content)
    return output.choices[0].message.content

if __name__ == '__main__':
    prompt_gpt("Hello")