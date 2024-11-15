import button

from aiogram.types import Message
from schedule_parser import get_schedule
from collections import defaultdict


def format_schedule_html(schedule, week_type):
    grouped_schedule = defaultdict(list)

    for entry in schedule:
        if entry['week_type'] == week_type:
            grouped_schedule[entry['day']].append(entry)

    formatted_text = []
    for day, entries in grouped_schedule.items():
        formatted_text.append(f"\n<b>{day.upper()}</b>\n")
        for idx, entry in enumerate(entries, start=1):
            class_text = f"<b>{idx} пара:</b>  {entry['time']} - {entry['lesson_name']}"
            if entry['details']:
                class_text += f" ({entry['details']})"
            else:
                class_text += " (None)"
            formatted_text.append(class_text)

    return '\n'.join(formatted_text)


async def process_schedule(message: Message, week_type: str):
    user_id = message.from_user.id
    schedule = await get_schedule(user_id)

    if not schedule:
        await message.answer(
            "Ваша группа не найдена. Пожалуйста, введите вашу группу или произошла ошибка")
        return

    schedule_text = format_schedule_html(schedule, week_type)
    await message.answer(f"🗓<b>Расписание на неделю ({week_type.capitalize()}):</b>\n\n{schedule_text}",
                         parse_mode='HTML', reply_markup=button.schedule_type_buttons)
