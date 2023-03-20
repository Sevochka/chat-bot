import json
import random
import nltk
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

from get_additional_data import add_additional_data_to_answer_by_intent


def convert_structure(data):
    intents = {}
    for intent in data["intents"]:
        examples = []
        for pattern in intent["patterns"]:
            examples.append(pattern)
        intents[intent["tag"]] = {
            "examples": examples,
            "responses": intent["responses"]
        }
    return {
        "intents": intents,
        "failure_phrases": data["failure_phrases"]
    }


with open('data/intents.json', encoding='utf-8') as file:
    BOT_CONFIG = convert_structure(json.load(file))

X_text = []
y = []

for intent, intent_data in BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        X_text.append(example)
        y.append(intent)

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3))
X = vectorizer.fit_transform(X_text)
clf = LinearSVC()
clf.fit(X, y)


def clear_phrase(phrase):
    phrase = phrase.lower()

    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- '
    result = ''.join(symbol for symbol in phrase if symbol in alphabet)

    return result.strip()


def classify_intent(replica):
    replica = clear_phrase(replica)

    intent = clf.predict(vectorizer.transform([replica]))[0]

    for example in BOT_CONFIG['intents'][intent]['examples']:
        example = clear_phrase(example)
        distance = nltk.edit_distance(replica, example)
        if example and distance / len(example) <= 0.5:
            return intent


def get_answer_by_intent(intent):
    if intent in BOT_CONFIG['intents']:
        responses = BOT_CONFIG['intents'][intent]['responses']
        if responses:
            return random.choice(responses)


with open('data/chan_dialogues.txt') as f:
    content = f.read()

dialogues_str = content.split('\n\n')
dialogues = [dialogue_str.split('\n')[:2] for dialogue_str in dialogues_str]

dialogues_filtered = []
questions = set()

for dialogue in dialogues:
    if len(dialogue) != 2:
        continue

    question, answer = dialogue
    question = clear_phrase(question[2:])
    answer = answer[2:]

    if question != '' and question not in questions:
        questions.add(question)
        dialogues_filtered.append([question, answer])

dialogues_structured = {}  # {'word': [['...word...', 'answer'], ...], ...}

for question, answer in dialogues_filtered:
    words = set(question.split(' '))
    for word in words:
        if word not in dialogues_structured:
            dialogues_structured[word] = []
        dialogues_structured[word].append([question, answer])

dialogues_structured_cut = {}
for word, pairs in dialogues_structured.items():
    pairs.sort(key=lambda pair: len(pair[0]))
    dialogues_structured_cut[word] = pairs[:1000]


# replica -> word1, word2, word3, ... -> dialogues_structured[word1] + dialogues_structured[word2] + ... -> mini_dataset

def generate_answer(replica):
    replica = clear_phrase(replica)
    words = set(replica.split(' '))
    mini_dataset = []
    for word in words:
        if word in dialogues_structured_cut:
            mini_dataset += dialogues_structured_cut[word]

    answers = []  # [[distance_weighted, question, answer]]

    for question, answer in mini_dataset:
        if abs(len(replica) - len(question)) / len(question) < 0.2:
            distance = nltk.edit_distance(replica, question)
            distance_weighted = distance / len(question)
            if distance_weighted < 0.2:
                answers.append([distance_weighted, question, answer])

    if answers:
        return min(answers, key=lambda three: three[0])[2]


def get_failure_phrase():
    failure_phrases = BOT_CONFIG['failure_phrases']
    return random.choice(failure_phrases)


stats = {'intent': 0, 'generate': 0, 'failure': 0}


def getResponse(replica):
    # NLU
    intent = classify_intent(replica)

    # выбор заготовленной реплики
    if intent:
        answer = get_answer_by_intent(intent)

        if answer:
            stats['intent'] += 1
            answer = add_additional_data_to_answer_by_intent(answer, intent)
            return [
                answer, intent
            ]
    # вызов генеративной модели
    answer = generate_answer(replica)
    if answer:
        stats['generate'] += 1
        return [
            answer
        ]

    # берем заглушку
    stats['failure'] += 1
    return [get_failure_phrase()]


print('Chatbot: Done')
# start_chatbot()
