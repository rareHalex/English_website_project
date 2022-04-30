import re
from searcher import find_content
import random

def clear_text(text:str):
    text = re.sub(r'\s+([\,\.\:\!\?])', r'\1',text)
    text = text.replace('--', '-')
    text = text.replace(';', '.')
    return text

def correct_word_task(word:str):
    correct_text = " ".join([data['content'] for data in find_content.get_content(word)])
    if len(correct_text) > 5000:
        correct_text = correct_text[:5000]
    text = clear_text(correct_text).replace(word, '*'*len(word))
    return text


def build_correct_sentence_task(word:str):
    correct_text = " ".join([data['content'] for data in find_content.get_content(word)])
    task_array = []
    if len(correct_text) > 5000:
        correct_text = correct_text[:5000]
    correct_text = correct_text.split('.')
    sentence_count = 0
    for _ in correct_text:
        sentence_count += 1
        first_sentence = "".join(correct_text[0]).split(' ')
        first_sentence = random.sample(first_sentence, len(first_sentence))
        task_array.append(" ".join(first_sentence))
        if sentence_count == 5:
            return task_array

    return task_array
