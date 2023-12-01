from typing import ClassVar

from aiogram.filters.callback_data import CallbackData


class CheckBoxFactory(CallbackData, prefix='check_box'):
    field: str


class RadioFactory(CallbackData, prefix='radio'):
    field: str


class NextCallbackFactory(CallbackData, prefix='next'):
    next: bool
