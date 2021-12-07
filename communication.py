from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db_work import DBWork
from ceker import money_chek, date_check


class FSMTest(StatesGroup):
    name = State()
    description = State()


class Communication:

    def __init__(self, token):
        storage = MemoryStorage()
        bot = Bot(token=token)
        self.dp = Dispatcher(bot, storage=storage)

    @staticmethod
    def create_rkm(*args):
        if not all(isinstance(x, str) for x in args):
            raise TypeError
        markup = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for i in args:
            markup.insert(types.KeyboardButton(i))
        return markup

    def main(self):
        self.dp.register_message_handler(self.send_welcome, commands=['start'])
        self.dp.register_message_handler(self.menu, commands=['menu'])
        self.dp.register_message_handler(self.create_new_wallet, commands=['create_new_wallet'], state=None)
        self.dp.register_message_handler(self.choose_wallet, commands=['choose_wallet'])
        self.dp.register_message_handler(self.statistics, commands=['statistics'])
        self.dp.register_message_handler(self.stop, state="*", commands='stop')
        if __name__ == 'communication':
            executor.start_polling(self.dp, skip_updates=True)

    async def send_welcome(self, message: types.Message):
        markup = self.create_rkm('/create_new_wallet', '/menu')
        await message.answer('Start', reply_markup=markup)

    async def menu(self, message: types.Message):
        markup = self.create_rkm('/create_new_wallet', '/choose_wallet', '/statistics')
        await message.answer('Menu', reply_markup=markup)

    async def create_new_wallet(self, message: types.Message, state=FSMTest):
        await message.answer('create_new_wallet')
        await FSMTest.first()
        await message.answer('enter name', reply_markup=self.create_rkm('/stop'))
        self.dp.register_message_handler(self.name, content_types=['text'], state=FSMTest.name)
        self.dp.register_message_handler(self.description, content_types=['text'], state=FSMTest.description)
        self.dp.register_message_handler(self.final, state="*", commands='Ok')
        self.dp.register_message_handler(self.stop, state="*", commands='stop')

    async def name(self, message: types.Message, state=FSMTest):
        markup = self.create_rkm('/stop')
        try:
            async with state.proxy() as data:
                data['name'] = message.text
            await message.answer('enter description', reply_markup=markup)
            await FSMTest.next()
        except TypeError:
            await message.answer('Wrong entering', reply_markup=markup)

    async def description(self, message: types.Message, state=FSMTest):
        markup = self.create_rkm('/stop')
        try:
            async with state.proxy() as data:
                data['description'] = message.text

            async with state.proxy() as data:
                await message.answer(f'Wallet {data["name"]}, {data["description"]}',
                                     reply_markup=self.create_rkm('/stop', '/Ok'))
            await FSMTest.next()
        except TypeError:
            await message.answer('Wrong entering', reply_markup=markup)

    async def final(self, message: types.Message, state=FSMTest):
        async with state.proxy() as data:
            db = DBWork(f'{message.from_user.id}')
            db.insert('wallet', (data["name"], data["description"]))
            res = db.select('wallet')
            await message.answer(f'{res}\nadded to database',
                                 reply_markup=self.create_rkm('/menu'))
        await state.finish()

    async def stop(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            await message.answer('Okk', reply_markup=self.create_rkm('/menu'))
            return
        await state.finish()
        await message.answer('Ok', reply_markup=self.create_rkm('/menu'))

    async def choose_wallet(self, message: types.Message):
        await message.answer('Doing nothing', reply_markup=self.create_rkm('/menu'))

    async def statistics(self, message: types.Message):
        await message.answer('Doing nothing', reply_markup=self.create_rkm('/menu'))
