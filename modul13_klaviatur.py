from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio



api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text = 'Информация')
button2 = KeyboardButton(text = 'Рассчитать')
start_kb.row(button, button2)



inline_kb = InlineKeyboardMarkup()
inline_button1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
inline_button2 = InlineKeyboardButton(text="Формула расчета", callback_data='formulas')
inline_kb.row(inline_button1, inline_button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я бот помогающий твоему здоровью', reply_markup = start_kb)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберете опцию', reply_markup = inline_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора для женщин: 10*вес (кг) +6,25*рост (см) -5*возраст (г) +5')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first1 = message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(first2 = message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(first3 = message.text)
    data = await state.get_data()
    calories = 10*int(data['first3'])+6.5*int(data['first2'])-5*int(data['first1'])+5
    await message.answer(f'Ваша норма калорий:{calories}')
    await state.finish()

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Чтобы узнать калории, надо было нажать кнопку "Рассчитать')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
