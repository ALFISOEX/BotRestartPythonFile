from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import subprocess
import threading as th

token = 'TOKEN'
file = 'PATH_TO_FILE'

bot = Bot(token=token)

dp = Dispatcher(bot)

processRun = False
shell_process = None

@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    await msg.answer('Доступные функции:\n'+
                     '1. /restart - перезапуск программы.\n'+
                     '2. /run - запуск программы.\n'+
                     '3. /close - закрытие программы.')

@dp.message_handler(commands=['restart'])
async def cmd_restart(msg: types.Message):
    if closePython() is False:
        await msg.answer('Процесс не запущен.')
    else:
        execPython()
        await msg.answer('Процесс перезапущен успешно.')
    

@dp.message_handler(commands=['run'])
async def cmd_run(msg: types.Message):
    if execPython() is True:
        await msg.answer('Процесс запущен.')
    else: 
        await msg.answer('Ошибка. Процесс уже был запущен.')

@dp.message_handler(commands=['close'])
async def cmd_close(msg: types.Message):
    if closePython() is False:
        await msg.answer('Процесс не запущен.')
    else:
        await msg.answer('Процесс закрыт.')

def closePython():
    global processRun
    global shell_process

    if processRun is False:
        return False
    else:
        shell_process.kill()
        processRun = False
        return True

def execPython():
    global processRun
    
    if processRun is True:
        return False
    else: 
        th.Thread(target=runPython()).start()
        processRun = True
        return True

def runPython():
    global shell_process
    shell_process = subprocess.Popen(['python', file], stdout=subprocess.PIPE)

if __name__ == '__main__':
    executor.start_polling(dp)
