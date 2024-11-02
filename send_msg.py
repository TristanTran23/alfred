import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

from twilio.rest import Client
from datetime import datetime
from typing import List, Dict

def get_conversation_history(account_sid: str, auth_token: str, phone_number: str) -> List[Dict]:
    client = Client(account_sid, auth_token)
    
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