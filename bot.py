import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import logging
import sys

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#設定（自分のデータに置き換えてください！)
API_ID = yourapi                    #ユアーズAPI ID (受け取る: my.telegram.org)
API_HASH = "-"            # あなたのAPIハッシュ
SESSION_NAME = "-"        # セッションファイル名（例えば，"my_account"）
PHONE_NUMBER = "-"        # あなたの電話番号
RECIPIENT = "-"     # 送信場所（ユーザー名またはチャットID）
MESSAGE_TEXT = "-"    #メッセージテキスト
INTERVAL_SEC = 10                    # 送信間隔（秒）

stop_event = asyncio.Event()

async def send_periodic_messages(client):
    while not stop_event.is_set():
        try:
            await client.send_message(RECIPIENT, MESSAGE_TEXT)
            logger.info(f"メッセージはに送信されます {RECIPIENT}!")
        except Exception as e:
            logger.error(f"エラー: {e}")
        
        for _ in range(INTERVAL_SEC):
            if stop_event.is_set():
                break
            await asyncio.sleep(1)

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    try:
        await client.start(phone=PHONE_NUMBER)
        logger.info("アカウントに正常にログインしました!")
    except SessionPasswordNeededError:
        password = input("2FAパスワードを入力します: ")
        await client.start(phone=PHONE_NUMBER, password=password)

    # 开始发送消息
    send_task = asyncio.create_task(send_periodic_messages(client))

    print("\nスクリプトが実行されています。 Ctrl+Cをクリックするか、'stop'を入力して終了します。")
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
        print("\nスクリプトが停止しました。")
    finally:
        print("作業は完了です。")
