from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from django.conf import settings
import os


chatbot = ChatBot(**settings.CHATTERBOT)

# Training With Own Questions 
trainer = ListTrainer(chatbot)
base_dir = settings.BASE_DIR    
qa = os.path.join(base_dir, 'static/training_data/ques_ans.txt')
pq = os.path.join(base_dir, 'static/training_data/personal_ques.txt')
training_data_quesans = open(qa).read().splitlines()
training_data_personal = open(pq).read().splitlines()
training_data = training_data_quesans + training_data_personal
trainer.train(training_data)

# Training With Corpus
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train(
    'chatterbot.corpus.russian'
)

class ChatterBotView(View):

    def get(self, request, *args, **kwargs):
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }
        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def post(self, request, *args, **kwargs):
        input_statement = request.POST.get('text')
        # print('40', input_statement)
        response_data = {
            'text': chatbot.get_response(input_statement).text
        }
        # print('45', response_data)
        return JsonResponse(response_data)