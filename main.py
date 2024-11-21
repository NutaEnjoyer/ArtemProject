from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.types import Message, InputFile, CallbackQuery
import asyncio
import config
from models import User
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# Токен бота
API_TOKEN = 'ТВОЙ_ТОКЕН_ЗДЕСЬ'
BOT_TOKEN = "7711412652:AAGidxb29rfpdbi0lDDhHPdbLsf2PZJJ35Y"  # Bot Token


# Создаем объект бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class PhotoForm(StatesGroup):
    waiting_for_photo = State()


class MailForm(StatesGroup):
    waiting_for_mail_message = State()

# Хендлер для обработки текстовых сообщений
@dp.message(Command('start'))
async def echo_handler(message: Message):
    spl = message.text.split()
    if len(spl) == 2:
        cmd = spl[1]
        print(cmd)
        tariff_index = int(config.TARIFF_NAMES.index(cmd.lower()))

        await message.answer_photo(config.PHOTO_URL, caption=config.tariff_text(config.TARIFFS[tariff_index]), reply_markup=config.tariff_keyboard(tariff_index))

        return

    user = User.get_or_none(user_id=message.from_user.id)
    if not user:
        user = User.create(user_id=message.from_user.id)
        user.save()
    await message.answer(config.GREETING_TEXT)
    await message.answer(config.SEMI_MESSAGE, reply_markup=config.tariffs_menu_keyboard())

@dp.message(Command('stat'))
async def stat_handler(message: Message):

    if message.from_user.id in config.ADMINS_ID:
        await message.answer(config.STAT_TEXT())

@dp.message(Command('mail'))
async def stat_handler(message: Message, state: FSMContext):
    if message.from_user.id in config.ADMINS_ID:
        await message.answer(config.MAIL_TEXT(), reply_markup=config.cancel_keyboard())
        await state.set_state(MailForm.waiting_for_mail_message)

@dp.callback_query(lambda c: c.data and c.data == 'cancel')
async def cancel_process_callback_tariff(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()

@dp.message(StateFilter(MailForm.waiting_for_mail_message))
async def cancel_process_callback_tariff(message: Message, state: FSMContext):
    if message.text and config.is_valid_keyboard_format(message.text):
        markup = config.parse_keyboard(message.text)
        await state.update_data(markup=markup)
        await message.answer("Вот клава", reply_markup=markup)
        return

    users = User.select()
    suc = 0
    err = 0

    data = await state.get_data()
    await state.clear()

    for user in users:
        try:
            await message.copy_to(user.user_id) if not data.get('markup') else await message.copy_to(user.user_id, reply_markup=data.get('markup'))
            suc += 1
        except Exception as e:
            err += 1

    await message.answer(config.MAIL_STAT_MESSAGE(suc, err))


# Хендлер для отлавливания callback_data
@dp.callback_query(lambda c: c.data and c.data.startswith('tariff_'))
async def process_callback_tariff(call: CallbackQuery):
    tariff_index = int(call.data.split('_')[1])

    await call.message.answer_photo(config.PHOTO_URL, caption=config.tariff_text(config.TARIFFS[tariff_index]), reply_markup=config.tariff_keyboard(tariff_index))

    await call.message.delete()


@dp.callback_query(lambda c: c.data and c.data == 'back')
async def back_process_callback_tariff(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(config.SEMI_MESSAGE, reply_markup=config.tariffs_menu_keyboard())


@dp.callback_query(lambda c: c.data and c.data.startswith('pay_'))
async def pay_process_callback_tariff(call: CallbackQuery):
    tariff_index = int(call.data.split('_')[1])

    await call.message.answer_photo(config.PHOTO_URL, caption=config.tariff_pay_text(config.TARIFFS[tariff_index]), reply_markup=config.tariff_pay_keyboard(tariff_index))

    await call.message.delete()


@dp.callback_query(lambda c: c.data and c.data.startswith('back_to_tariff_'))
async def back_to_tariff_process_callback_tariff(call: CallbackQuery):
    tariff_index = int(call.data.split('_')[3])

    await call.message.answer_photo(config.PHOTO_URL, caption=config.tariff_text(config.TARIFFS[tariff_index]), reply_markup=config.tariff_keyboard(tariff_index))

    await call.message.delete()


@dp.callback_query(lambda c: c.data and c.data.startswith('back_to_pay_tariff_'))
async def back_to_pay_tariff_process_callback_tariff(call: CallbackQuery):
    tariff_index = int(call.data.split('_')[4])

    await call.message.answer_photo(config.PHOTO_URL, caption=config.tariff_pay_text(config.TARIFFS[tariff_index]), reply_markup=config.tariff_pay_keyboard(tariff_index))

    await call.message.delete()


@dp.callback_query(lambda c: c.data and c.data.startswith('crypto_pay_'))
async def crypto_pay_process_callback_tariff(call: CallbackQuery):
    tariff_index = int(call.data.split('_')[2])

    await call.message.answer_photo(config.PHOTO_URL, caption=config.crypto_pay_text(config.TARIFFS[tariff_index], call.from_user.id), reply_markup=config.pay_keyboard(tariff_index))

    await call.message.delete()


@dp.callback_query(lambda c: c.data and c.data.startswith('card_pay_'))
async def crypto_pay_process_callback_tariff(call: CallbackQuery):
    tariff_index = int(call.data.split('_')[2])

    await call.message.answer_photo(config.PHOTO_URL, caption=config.card_pay_text(config.TARIFFS[tariff_index], call.from_user.id), reply_markup=config.pay_keyboard(tariff_index))

    await call.message.delete()

@dp.callback_query(lambda c: c.data and c.data.startswith('i_pay_'))
async def crypto_pay_process_callback_tariff(call: CallbackQuery, state: FSMContext):
    tariff_index = int(call.data.split('_')[2])

    await call.message.answer(config.requests_photo())
    await state.set_state(PhotoForm.waiting_for_photo)
    await state.update_data(tariff_index=tariff_index)

    await call.message.delete()


@dp.message(F.photo, StateFilter(PhotoForm.waiting_for_photo))
async def handle_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    tariff_index = data['tariff_index']

    photo = message.photo[-1]  # Получаем фото в наивысшем качестве
    photo_file_id = photo.file_id

    # Отправляем подтверждение и фото обратно
    await message.answer(config.get_photo())

    for ADMIN_ID in config.ADMINS_ID:
        await bot.send_photo(ADMIN_ID, photo_file_id, caption=config.admin_text(tariff_id = tariff_index, username=message.from_user.username, user_id=message.from_user.id, user_first_name=message.from_user.first_name))

    await state.clear()


async def main():
    # Запускаем бота и диспетчер
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
