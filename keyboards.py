from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from callback import NextCallbackFactory


def main_kb(admin=False) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Подобрать группу 👥')
    kb.button(text='Анкета для учителя 👨‍🏫')
    kb.button(text='Обратиться к методисту')

    if admin:
        kb.button(text='Панель администратора')
        kb.adjust(2, 1, 1)
    else:
        kb.adjust(2)

    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите aнкету ↓',
    )


def admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Никнейм методиста')
    kb.button(text='Выход в меню')

    kb.adjust(1)

    return kb.as_markup(
        resize_keyboard=True,
    )


def methodist_nickname_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(text='Изменить', callback_data='methodist_edit')

    kb.adjust(1)

    return kb.as_markup(
        resize_keyboard=True,
    )


def cansel_form_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    kb.button(text='прекратить анкету')

    return kb.as_markup(
        resize_keyboard=True,
    )


def next_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(text='==== Далее ====', callback_data=NextCallbackFactory(next=True))

    return kb.as_markup(
        resize_keyboard=True,
    )


def checkbox_and_radio_kb(res: list, adjust: int | tuple, factory, data: list = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for answer in res:
        if data:
            if answer in data:
                kb.button(text='✅ ' + answer, callback_data=factory(field=answer))
            else:
                kb.button(text=answer, callback_data=factory(field=answer))
        else:
            kb.button(text=answer, callback_data=factory(field=answer))

    kb.button(text='==== Далее ====', callback_data=NextCallbackFactory(next=True))

    if isinstance(adjust, tuple):
        kb.adjust(*adjust)
    elif isinstance(adjust, int):
        kb.adjust(adjust)

    return kb.as_markup(
        resize_keyboard=True,
    )