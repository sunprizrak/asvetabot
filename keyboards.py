from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from callback import NextCallbackFactory


def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='📝 Анкета для ученика 👨‍🎓')
    kb.button(text='📝 Анкета для учителя 👨‍🏫')
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите aнкету ↓',
    )


def cansel_form_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='прекратить анкету')
    return kb.as_markup(
        resize_keyboard=True,
    )


def next_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(text='Далее', callback_data=NextCallbackFactory(next=True))

    return kb.as_markup(
        resize_keyboard=True,
    )


def checkbox_and_radio_kb(res: list, adjust: int, factory, data: list = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for answer in res:
        if data:
            if answer in data:
                kb.button(text='✅ ' + answer, callback_data=factory(field=answer))
            else:
                kb.button(text=answer, callback_data=factory(field=answer))
        else:
            kb.button(text=answer, callback_data=factory(field=answer))

    kb.button(text='Далее', callback_data=NextCallbackFactory(next=True))

    kb.adjust(adjust)

    return kb.as_markup(
        resize_keyboard=True,
    )