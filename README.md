# TimeEstim
To avoid a recent incompatibility between ChaterBot and spaCy, I went to /myvenv/lib/python3.7/site-packages/chatterbot/tagging.py
and replaced
```
      self.nlp = spacy.load(self.language.ISO_639_1.lower())
```
with
```
       if self.language.ISO_639_1.lower() == 'en':
           self.nlp = spacy.load('en_core_web_sm')
       elif self.language.ISO_639_1.lower() == 'ru':
           self.nlp = spacy.load('ru_core_news_sm')
       else:
           self.nlp = spacy.load(self.language.ISO_639_1.lower())
```

You can find below a list of requirements I have in my project locally, but please note that I abandoned some of these during development.
asgiref==3.3.1
blis==0.7.4
catalogue==2.0.1
certifi==2020.12.5
cffi==1.14.5
chardet==4.0.0
ChatterBot==1.0.8
chatterbot-corpus==1.2.0
click==7.1.2
cryptography==3.4.5
cymem==2.0.5
DAWG-Python==0.7.2
defusedxml==0.6.0
Django==3.1.4
django-allauth==0.44.0
django-bulma-widget==1.1
django-rest-auth==0.9.5
djangorestframework==3.12.2
docopt==0.6.2
en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0-py3-none-any.whl
idna==2.10
importlib-metadata==3.8.0
Jinja2==2.11.3
joblib==1.0.1
MarkupSafe==1.1.1
mathparse==0.1.2
murmurhash==1.0.5
nltk==3.5
numpy==1.20.1
oauthlib==3.1.0
packaging==20.9
pathy==0.4.0
Pillow==8.1.0
preshed==3.0.5
pycparser==2.20
pydantic==1.7.3
PyJWT==2.0.1
pymorphy2==0.9.1
pymorphy2-dicts-ru==2.4.417127.4579844
pyparsing==2.4.7
python-dateutil==2.8.1
python3-openid==3.2.0
pytz==2020.4
PyYAML==3.13
regex==2021.3.17
requests==2.25.1
requests-oauthlib==1.3.0
ru-core-news-sm @ https://github.com/explosion/spacy-models/releases/download/ru_core_news_sm-3.0.0/ru_core_news_sm-3.0.0-py3-none-any.whl
six==1.15.0
smart-open==3.0.0
spacy==3.0.5
spacy-legacy==3.0.1
SQLAlchemy==1.3.23
sqlparse==0.4.1
srsly==2.4.0
thinc==8.0.2
tqdm==4.59.0
typer==0.3.2
typing-extensions==3.7.4.3
urllib3==1.26.3
wasabi==0.8.2
zipp==3.4.1
