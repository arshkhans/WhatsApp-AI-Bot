from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot("Bot", read_only=True,logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        }])

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.custom.english")

while(True):
    reply = chatbot.get_response(input("->"))
    print(reply.get_tags())