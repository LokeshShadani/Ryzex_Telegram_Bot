import asyncio

async def set_reminder(minutes, message, context):
    await context.bot.send_message(chat_id=context._chat_id, text=f"✅ Reminder set for {minutes} minutes!")
    await asyncio.sleep(minutes * 60)
    await context.bot.send_message(chat_id=context._chat_id, text=f"⏰ Reminder: {message}")
