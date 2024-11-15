from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Уведомления"),
            KeyboardButton(text="Расписание на неделю")
        ],
        [
            KeyboardButton(text="Изменить группу")
        ]
    ],
    resize_keyboard=True
)

notification_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Включить"),
            KeyboardButton(text="Выключить"),
        ],
        [
            KeyboardButton(text="Как работает?"),
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)
schedule_type_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Числитель"),
            KeyboardButton(text="Знаменатель")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)
