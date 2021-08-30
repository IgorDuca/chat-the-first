from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

bot = ChatBot('Chatbot')

conversa = [
    'oi', 
    'oiee', 
    'tudo bem?', 
    'tô bem, e você?', 
    'também tô bem',
    'que bom'
    'tá fazendo o que de bom', 
    'por enquanto nada'
]

bot.set_trainer(ListTrainer)
bot.train(conversa)

while True:
    pergunta = input("Usuário: ")
    resposta = bot.get_response(pergunta)
    if float(resposta.confidence) > 0.5:
        print('Chatbot: ', resposta)
    else:
        print('Chatbot: eita, nem sei como te responder')
