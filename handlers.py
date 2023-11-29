import logging
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import get_state_form, TeacherForm
from keyboards import main_kb, cansel_form_kb, next_kb
from callback import CheckBoxFactory, RadioFactory, NextCallbackFactory

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=main_kb())


form_router = Router()


@form_router.message(Command('прекратить анкету'))
@form_router.message(F.text.casefold() == 'прекратить анкету')
async def cansel_profile(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        return

    logging.info(f'Cancelling state {current_state}')

    await state.clear()
    await message.answer(
        'анкета прекращена',
        reply_markup=main_kb(),
    )


@form_router.message(F.text.lower() == '📝 анкета для ученика 👨‍🎓')
async def student_profile(message: types.Message, state: FSMContext):
    await message.reply(text='Ваше: Фамилия, Имя, Отчество')


@form_router.message(F.text.lower() == '📝 анкета для учителя 👨‍🏫')
async def teacher_profile(message: types.Message, state: FSMContext) -> None:
    await state.set_state(TeacherForm.name)
    await message.answer(
        text=TeacherForm.params['name']['quest'],
        reply_markup=TeacherForm.params['name']['keyboard'](),
    )


@form_router.message(TeacherForm.email_or_phone)
@form_router.message(TeacherForm.about_me)
@form_router.message(TeacherForm.place_work)
@form_router.message(TeacherForm.count_hours)
@form_router.message(TeacherForm.name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    received_state = await state.get_state()
    form_state, curr_state = (el for el in received_state.split(':'))
    form = get_state_form(form_state)

    print(curr_state)

    await state.update_data({curr_state: message.text})

    next_state = form.next_state(curr_state)

    if next_state:
        await state.set_state(f'{form_state}:{next_state}')

        await message.answer(
            text=form.params[next_state]['quest'],
            reply_markup=form.params[next_state]['keyboard']()
        )
    else:
        data = await state.get_data()
        print(data)


@form_router.message(TeacherForm.choice_online_platforms)
@form_router.message(TeacherForm.online_platforms)
@form_router.message(TeacherForm.subjects)
async def process_checkbox_and_ratio(message: types.Message, state: FSMContext) -> None:
    received_state = await state.get_state()
    curr_state = received_state.split(':')[1]

    if ',' in message.text:
        items = [elem.strip() for elem in message.text.split(",")]
    else:
        items = [elem.strip() for elem in message.text.split()]

    data = await state.get_data()

    if data.get(curr_state):
        new_items = data[curr_state] + items
        await state.update_data({curr_state: new_items})
    else:
        await state.update_data({curr_state: items})

    message_text = 'Вы выбрали:\n'

    data = await state.get_data()

    for number, item in enumerate(data[curr_state], start=1):
        message_text += f'\t{number}. {item}\n'

    await message.answer(
        text=message_text,
        reply_markup=next_kb(),
    )


@form_router.message(TeacherForm.doc)
async def process_document(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()

    if hasattr(message.document, 'file_name'):
        file = types.FSInputFile(message.document.file_name)

        if data.get('doc'):
            if file.path in data['doc']:
                data['doc'].remove(file.path)
                await state.update_data(doc=data['doc'])
            else:
                data['doc'].append(file.path)
                await state.update_data(doc=data['doc'])
        else:
            data['doc'] = [file.path]
            await state.update_data(doc=data['doc'])

        data = await state.get_data()

        message_text = 'Загруженные документы:\n'

        for number, file_path in enumerate(data['doc'], start=1):
            message_text += f'\t{number}. {file_path}\n'

        await message.answer(
            text=message_text,
            reply_markup=next_kb(),
        )
    else:
        await message.answer(
            text='Отправляемое сообщение должно быть документом!',
            reply_markup=cansel_form_kb(),
        )

# ----------------------- <<  Callback >>  -----------------------


@form_router.callback_query(NextCallbackFactory.filter())
async def check_next_button(callback: types.CallbackQuery, callback_data: NextCallbackFactory, state: FSMContext):
    received_state = await state.get_state()
    form_state, curr_state = (el for el in received_state.split(':'))
    form = get_state_form(form_state)

    data = await state.get_data()

    if callback_data.next and data.get(curr_state):
        next_state = form.next_state(curr_state)
        await state.set_state(f'{form_state}:{next_state}')

        await callback.message.answer(
            text=form.params[next_state]['quest'],
            reply_markup=form.params[next_state]['keyboard'](),
        ),
    elif callback_data.next and not data.get(curr_state):
        await callback.message.answer(
            text='Выполните предложенные действия!'
        )

    await callback.answer()


@form_router.callback_query(CheckBoxFactory.filter())
async def check_box_buttons(callback: types.CallbackQuery, callback_data: CheckBoxFactory, state: FSMContext):
    received_state = await state.get_state()
    form_state, curr_state = (el for el in received_state.split(':'))
    form = get_state_form(form_state)

    data = await state.get_data()

    if callback_data.field.lower() == 'другое':
        await callback.message.answer(
            text='Введите свои варианты',
        )
    else:
        if data.get(curr_state):
            if callback_data.field in data[curr_state]:
                data[curr_state].remove(callback_data.field)
                await state.update_data({curr_state: data[curr_state]})
            else:
                data[curr_state].append(callback_data.field)
                await state.update_data({curr_state: data[curr_state]})
        else:
            data[curr_state] = [callback_data.field]
            await state.update_data({curr_state: data[curr_state]})

        await callback.message.edit_reply_markup(
            inline_message_id=callback.id,
            reply_markup=form.params[curr_state]['keyboard'](data=data[curr_state]),
        )

    await callback.answer()


@form_router.callback_query(RadioFactory.filter())
async def check_radio_buttons(callback: types.CallbackQuery, callback_data: RadioFactory, state: FSMContext):
    received_state = await state.get_state()
    form_state, curr_state = (el for el in received_state.split(':'))
    form = get_state_form(form_state)

    data = await state.get_data()

    if data.get(curr_state):
        if callback_data.field in data[curr_state]:
            data[curr_state].remove(callback_data.field)
            await state.update_data({curr_state: data[curr_state]})
        else:
            data[curr_state] = [callback_data.field]
            await state.update_data({curr_state: data[curr_state]})
    else:
        data[curr_state] = [callback_data.field]
        await state.update_data({curr_state: data[curr_state]})

    await callback.message.edit_reply_markup(
        inline_message_id=callback.id,
        reply_markup=form.params[curr_state]['keyboard'](data=data[curr_state])
    )

    await callback.answer()