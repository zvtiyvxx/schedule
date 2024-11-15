from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from config import TOKEN
from data import load_user_groups, load_notifications_state
from schedule_parser import get_schedule


bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()


def is_numerator_week(date):
    week_number = date.isocalendar()[1]
    return week_number % 2 != 0


async def scheduled_notification():
    tomorrow_date = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow_date.strftime('%A')

    days_map = {
        'Monday': 'понедельник',
        'Tuesday': 'вторник',
        'Wednesday': 'среда',
        'Thursday': 'четверг',
        'Friday': 'пятница',
        'Saturday': 'суббота',
        'Sunday': 'воскресенье'
    }

    tomorrow_russian = days_map.get(tomorrow, "").lower()
    is_numerator = is_numerator_week(tomorrow_date)
    week_type = 'числитель' if is_numerator else 'знаменатель'

    user_data = load_user_groups()

    for user_id, group in user_data.items():
        notifications = load_notifications_state(user_id)

        if notifications == 'on':
            schedule = get_schedule(user_id)

            if schedule:
                next_day_schedule = [
                    entry for entry in schedule
                    if
                    entry['day'].lower() == tomorrow_russian and entry.get('week_type', '').lower() == week_type.lower()
                ]

                if next_day_schedule:
                    message = f"<b>Расписание на завтра ({tomorrow_russian.title()}, {week_type}):</b>\n\n"
                    for entry in next_day_schedule:
                        message += f"{entry['time']} - {entry['lesson_name']}: {entry['details']}\n"

                    await bot.send_message(user_id, message, parse_mode="HTML")
                else:
                    message = "<b>Завтра пар нет</b>"
                    await bot.send_message(user_id, message, parse_mode="HTML")
                    await bot.send_sticker(user_id, sticker = "CAACAgIAAxkBAALhwmc2mEUZQFM6aIUNq8Stvo5VBzNsAAIoEgACSpfRS1V8PHkKHjrGNgQ" )


def start_scheduler():
    scheduler.add_job(scheduled_notification, 'cron', hour=20, minute=0)
    scheduler.start()
