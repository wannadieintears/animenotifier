from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Add a title"),
            KeyboardButton(text="Delete a title"),
            KeyboardButton(text="Show titles")
        ],
        [
            KeyboardButton(text="On"),
            KeyboardButton(text="Off")
        ]
    ],
    resize_keyboard=True,
    selective=True,
    input_field_placeholder="ilysm"
)