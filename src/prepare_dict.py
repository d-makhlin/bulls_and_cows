import codecs
import json
import re

with codecs.open('../static/raw_dict.txt', 'r+', encoding='utf-8') as file:
    lines = file.readlines()
    r = re.compile("[а-яА-Я]+")
    lines = [w for w in filter(r.match, lines)]
    word_dict = {4: [], 5: [], 6: []}
    for line in lines:
        line = line[0: len(line)-1]
        if 4 <= len(line) <= 6:
            word_dict[len(line)].append(line)

with codecs.open('../static/dictionary.txt', 'w', encoding='utf-8') as file:
    json.dump(word_dict, file, ensure_ascii=False)
