import enchant

d=enchant.Dict("en-US")
WORDS_5=[]
with open('words.txt') as file:
    words = file.readlines()
    for i in range(len(words)):
        word=words[i]
        if word[-1]=='\n':
            word=word[:-1]
        if d.check(word):
            WORDS_5.append(word)