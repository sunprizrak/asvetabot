from aiogram.fsm.state import StatesGroup, State

from callback import CheckBoxFactory, RadioFactory
from keyboards import cansel_form_kb, checkbox_and_radio_kb


def get_state_form(form_name: str):

    def _get_subclasses(cls=MyRootForm):
        subclasses = []
        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
            subclasses.extend(_get_subclasses(subclass))
        return subclasses

    subclasses_of_root = _get_subclasses()

    for subclass in subclasses_of_root:
        if form_name == subclass.__name__:
            return subclass


class MyRootForm(StatesGroup):

    @classmethod
    def next_state(cls, curr_state):
        states = [state_name.split(':')[1] for state_name in cls.__all_states_names__]
        curr_index = states.index(curr_state)
        if curr_index + 1 == len(states):
            return False
        else:
            return states[curr_index + 1]


class TeacherForm(MyRootForm):
    name = State()
    subjects = State()
    class_number = State()
    work_experience = State()
    count_hours = State()
    place_work = State()
    doc = State()
    about_me = State()
    experience = State()
    online_platforms = State()
    choice_online_platforms = State()
    email_or_phone = State()

    params = {
        'name': {
            'quest': 'Фамилия, Имя, Отчество',
            'keyboard': lambda: cansel_form_kb(),
        },
        'subjects': {
            'quest': 'Предмет/ы, который/е вы хотите преподавать',
            'keyboard': lambda data=None: checkbox_and_radio_kb(
                            data=data,
                            res=[
                                'Математика',
                                'Физика',
                                'Русский язык',
                                'Белорусский язык',
                                'Английский язык',
                                'Другое',
                            ],
                            adjust=2,
                            factory=CheckBoxFactory,
                        )
        },
        'class_number': {
            'quest': 'В каких классах вы готовы преподавать',
            'keyboard': lambda data=None: checkbox_and_radio_kb(
                            data=data,
                            res=['5', '6', '7', '8', '9', '10', '11'],
                            adjust=3,
                            factory=CheckBoxFactory,
                        )
        },
        'work_experience': {
            'quest': 'Стаж работы преподавателем (лет)',
            'keyboard': lambda data=None: checkbox_and_radio_kb(
                            data=data,
                            res=['0-5', '5-10', '10-20', 'более 20'],
                            adjust=2,
                            factory=RadioFactory,
                        )
        },
        'count_hours': {
            'quest': 'Сколько академических часов в неделю вы готовы преподавать',
            'keyboard': lambda: cansel_form_kb(),
        },
        'place_work': {
            'quest': 'Настоящее место работы / занятости',
            'keyboard': lambda: cansel_form_kb(),
        },
        'doc': {
            'quest': 'Предоставьте дополнительные документы (резюме, а также копию диплома, трудовой книги или иные документы, подтверждающие квалификацию)',
            'keyboard': lambda: cansel_form_kb(),
        },
        'about_me': {
            'quest': 'Что дополнительно вы хотели бы сообщить вашим ученикам и их родителям о себе?',
            'keyboard': lambda: cansel_form_kb(),
        },
        'experience': {
            'quest': 'У вас уже есть опыт проведения онлайн-занятий?',
            'keyboard': lambda data=None: checkbox_and_radio_kb(
                            data=data,
                            res=['Да', 'Нет'],
                            adjust=2,
                            factory=RadioFactory,
                        )
        },
        'online_platforms': {
            'quest': 'Какими онлайн платформами с функцией видеозвонка вы пользовались?',
            'keyboard': lambda data=None: checkbox_and_radio_kb(
                            data=data,
                            res=[
                                'Google Classroom / Google Meet',
                                'Skype',
                                'Zoom',
                                'Мне всё равно',
                                'Я затрудняюсь ответить',
                                'Другое',
                            ],
                            adjust=1,
                            factory=CheckBoxFactory,
                        )
        },
        'choice_online_platforms': {
            'quest': 'Какую платформу вы бы предпочли использовать для проведения онлайн занятий?',
            'keyboard': lambda data=None: checkbox_and_radio_kb(
                            data=data,
                            res=[
                                'Google Classroom / Google Meet',
                                'Skype',
                                'Zoom',
                                'Мне всё равно',
                                'Я затрудняюсь ответить',
                                'Другое',
                            ],
                            adjust=1,
                            factory=CheckBoxFactory,
                        )
        },
        'email_or_phone': {
            'quest': 'Оставьте, пожалуйста, свои контактные данные для обратной связи (email, номер телефона)',
            'keyboard': lambda: cansel_form_kb(),
        },
    }


if __name__ == '__main__':
    print(TeacherForm.next_state('subjects'))