import json
from telethon import TelegramClient
import asyncio

managers = []

def get_active_manager():
    return next((manager for manager in managers if manager.active), None)

class AccountManager:
    def __init__(self, phone, api_id, api_hash):
        self.client = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._create_client(phone, api_id, api_hash))

    async def _create_client(self, phone, api_id, api_hash):
        self.client = TelegramClient(phone, api_id, api_hash)
        await self.client.connect()


    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def join_group(self, link):
        await self.client.join_chat(link)

    async def send_message(self, target, message):
        await self.client.send_message(target, message)

def load_managers_from_config(config_file):
    managers = []
    with open(config_file, 'r') as f:
        config = json.load(f)

    for account in config['accounts']:
        managers.append(AccountManager(account['phone'], account['api_id'], account['api_hash']))
    return managers


def save_managers_to_config(config_file):
    global managers
    config = {"accounts": []}

    for manager in managers:
        config["accounts"].append({
            "api_id": manager.api_id,
            "api_hash": manager.api_hash,
            "phone": manager.phone,
            "username": manager.username
        })

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
