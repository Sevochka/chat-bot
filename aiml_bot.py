import os
import aiml

BRAIN_FILE="brain.dump"

k = aiml.Kernel()

# Для увеличения скорости запуска бота необходимо
# можно сохранить разобранные файлы аимл как
# свалка. Этот код проверяет, существует ли дамп и
# в противном случае загружает аимл из файлов xml
# и сохраняет дамп мозга.
if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)


def getAimlResponse(message):
    response = k.respond(message)
    return response