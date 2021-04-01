import json
from django.views.generic.base import TemplateView
# from django.views.generic import View
# from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
# from chatterbot import ChatBot
# from .api import chatbot
# from chatterbot.ext.django_chatterbot import settings

# import spacy
# from spacy.lang.ru.examples import sentences 
# nlp = spacy.load("ru_core_news_sm")
# doc = nlp(sentences[0])
# print(doc.text)
# for token in doc:
#     print(token.text, token.pos_, token.dep_)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class ChatterBotAppView(TemplateView):
    template_name = 'bot/app.html'


# class ChatterBotApiView(View):
#     """
#     Provide an API endpoint to interact with ChatterBot.
#     """
#     # chatterbot = ChatBot(**settings.CHATTERBOT)
#     chatterbot = chatbot

#     def post(self, request, *args, **kwargs):
#         """
#         Return a response to the statement in the posted data.
#         * The JSON data should contain a 'text' attribute.
#         """
#         input_data = json.loads(request.body.decode('utf-8'))
#         if 'text' not in input_data:
#             return JsonResponse({
#                 'text': [
#                     'The attribute "text" is required.'
#                 ]
#             }, status=400)
#         response = self.chatterbot.get_response(input_data)
#         response_data = response.serialize()
#         return JsonResponse(response_data, status=200)

#     def get(self, request, *args, **kwargs):
#         """
#         Return data corresponding to the current conversation.
#         """
#         return JsonResponse({
#             'name': self.chatterbot.name
#         })