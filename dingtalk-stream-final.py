import asyncio
from dingtalk_stream import DingTalkStreamClient, CallbackHandler

class OpenClawHandler(CallbackHandler):
    async def process(self, callback):
        text = callback.headers.get('text', {}).get('content', '')
        result = await asyncio.create_subprocess_exec(
            'timeout', '30', 'openclaw', 'ask', text,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd='/root/.openclaw/workspace'
        )
        stdout, stderr = await result.communicate()
        response = (stdout.decode() or stderr.decode())[:2000]
        await self.reply_text(response, callback)

async def main():
    client = DingTalkStreamClient(
        "ding9terdcvatbdu7lif",
        "LXmS1a5gnHto226xk8jZHJc85mrknhC03KULsThMi1mB_I39pQ6OPFfP8QARql8a"
    )
    client.register_callback_handler('/v1.0/im/bot/messages/get', OpenClawHandler())
    await client.start()

if __name__ == '__main__':
    asyncio.run(main())