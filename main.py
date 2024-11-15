import asyncio
import button

from config import TOKEN
from data import save_user_group, save_notifications_state
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from process_schedule import process_schedule
from scheduler_notification import start_scheduler
from schedule_parser import check_group_exists


bot = Bot(token=TOKEN)
dp = Dispatcher()


class Reg(StatesGroup):
    group = State()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.reply("Введите вашу группу (Например: У-232): ")
    await state.set_state(Reg.group)


@dp.message(Reg.group)
async def save_group_handler(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    user_id = message.from_user.id
    if check_group_exists(message.text):
        data = await state.get_data()
        group = data['group']
        save_user_group(user_id, group)
        await message.reply(f"Ваша группа: {group}", reply_markup=button.main_button)
        await state.clear()
    else:
        await message.reply("Такой группы нету")

@dp.message(lambda message: message.text.lower() == "изменить группу")
async def change_group(message: types.Message, state: FSMContext):
    await message.reply("Введите вашу новую группу (Например: У-232):")
    await state.set_state(Reg.group)

@dp.message()
async def notification2(message: types.Message):
    msg = message.text.strip().lower()
    user_id = message.from_user.id

    if msg == "уведомления":
        await message.answer('Уведомления: ', reply_markup=button.notification_button)
    elif msg == "расписание на неделю":
        await message.answer("Выберите вариант: ", reply_markup=button.schedule_type_buttons)
    elif msg == "назад":
        await message.answer("Вернулись в главное меню", reply_markup=button.main_button)
    elif msg == "числитель":
        await process_schedule(message, "числитель")
    elif msg == "знаменатель":
        await process_schedule(message, "знаменатель")
    elif msg == "включить":
        save_notifications_state(user_id, "on")
        await message.reply("Уведомления включены", reply_markup=button.main_button)
    elif msg == "выключить":
        save_notifications_state(user_id, "off")
        await message.reply("Уведомления выключены", reply_markup=button.main_button)
    elif msg == "как работает?":
        await message.reply(
            "Уведомления отправляют расписание на следующий день каждый вечер в 20:00, если они включены. Вы можете включить или выключить уведомления в меню уведомлений.",
            reply_markup=button.notification_button)
    else:
        await message.reply("Команда не распознана. Попробуйте снова.")


async def main():
    start_scheduler()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
