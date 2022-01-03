from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from QuestionDetection import main

# nltk.download('nps_chat')

chatbot = ChatBot("Bot", read_only=True,logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'None',
            'maximum_similarity_threshold': 0.9
        }])

checkQ = main.IsQuestion()

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.custom.greetings")

while(True):
    received = input("->")
    if len(received) < 2:
        botReply = "Please provide me with more than one charater"
    else:
        botReply = chatbot.get_response(received)
        if botReply.text == 'None':
            if (checkQ.predict_question(received)):
                print("Googling your Question")
                continue
            else:
                print("I am sorry, but I do not understand.")
                continue
    print(botReply)