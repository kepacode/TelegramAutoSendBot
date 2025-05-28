import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import logging
import sys

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置（用自己的数据替换！)
API_ID = yourapi                     # 您的API ID (接收: my.telegram.org)
API_HASH = "-"            # 您的API哈希
SESSION_NAME = "-"        # 会话文件名（例如，"my_account"）
PHONE_NUMBER = "-"        # 您的电话号码
RECIPIENT = "-"     # 发送位置（用户名或聊天ID）
MESSAGE_TEXT = "-"    # 消息文本
INTERVAL_SEC = 10                    # 发送间隔（秒）

stop_event = asyncio.Event()

async def send_periodic_messages(client):
    while not stop_event.is_set():
        try:
            await client.send_message(RECIPIENT, MESSAGE_TEXT)
            logger.info(f"该消息被发送到 {RECIPIENT}!")
        except Exception as e:
            logger.error(f"错误: {e}")
        
        for _ in range(INTERVAL_SEC):
            if stop_event.is_set():
                break
            await asyncio.sleep(1)

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    try:
        await client.start(phone=PHONE_NUMBER)
        logger.info("成功登入户口!")
    except SessionPasswordNeededError:
        password = input("输入2FA密码: ")
        await client.start(phone=PHONE_NUMBER, password=password)

    # 开始发送消息
    send_task = asyncio.create_task(send_periodic_messages(client))

    print("\n脚本正在运行。 点击 Ctrl+C 或输入'stop'退出。")
    while True:
        user_input = await asyncio.get_event_loop().run_in_executor(None, input)
        if user_input.strip().lower() == "stop":
            stop_event.set()
            await send_task 
            break

    await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n脚本已停止。")
    finally:
        print("工作完成了。")
