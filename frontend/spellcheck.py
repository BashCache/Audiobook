# importing preliminaries
import re
import math
import string
import nltk
from enchant.checker import SpellChecker
from urllib.parse import urlparse
import os

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

# remove punctuation
def basicRemoval(text):
  # punc = '\<>#$%_~()[]{}'
  # for ele in text: 
  #   if ele in punc:  
  #     text = text.replace(ele, " ") 
  # print('BASIC REMOVAL: ', text)
  # return text
  reqd_punc = '@&*()[]{}/.;:\,\'"-'
  for ele in text:
    if ele == ' ' or ele == '\n' or (ele >='a' and ele <= 'z') or (ele >= 'A' and ele <='Z') or (ele >='0' and ele <= '9'):
      print()
    elif ele not in reqd_punc :
      text = text.replace(ele, " ")
  # text1 = re.sub("[^a-zA-Z0-9@&*+-?.,;\n'\":/\\ ]", "", text)
  print(text)
  return text

# cleanup text
def cleanupText(text):
  rep = { '\n': ' ', '\\': ' ', '\"': '"', '-': ' ', '"': ' " ', 
        '"': ' " ', '"': ' " ', ',':' , ',  '!':' ! ', 
        '?':' ? ', "n't": " not" , "'ll": " will", '*':' * ', 
        '(': ' ( ', ')': ' ) ', "s'": "s '", '“': ' “ ', '”': ' ” ', '’': ' ’ '}
  rep = dict((re.escape(k), v) for k, v in rep.items()) 
  pattern = re.compile("|".join(rep.keys()))
  text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
  print('CLEANUP TEXT: ', text)
  return text

# Get each word
# If word starts with capital letter, or is entirely in CAPS do not consider that as wrong word
# Check for mail ID
def wordSplit(text):
  words = text.split()
  # print('WORD SPLIT: ', len(words), words)
  return words

# Consider all words starting in capital letter as proper noun
def getProperNoun(words):
  propernoun = []
  for i in range(len(words)):
    # print(len(words[i]))
    if (len(words[i])>0 and words[i][0].isupper() == True):
      propernoun.append(words[i])
  print('PROPER NOUN: ', propernoun)
  return propernoun

# Check for email ids
def getEmail(words):
  EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
  email = []
  for i in range(len(words)):
    if EMAIL_REGEX.match(words[i]):
      email.append(words[i])
  print('EMAIL: ', email)
  return email

# Check for URLs ( This will be mostly applicable for academic papers)
def getURL(words):
  url = []
  for i in range(len(words)):
    o = urlparse(words[i])
    if (o.scheme != "" and o.netloc !="" and o.path!=""):
      url.append(words[i])
  print('URL: ', url)
  return url

# using enchant.checker.SpellChecker, identify basic incorrect words and get basic suggested replacements
def basicSpellCheck(propernoun, email, url, words):
  ignorewords = propernoun + email + url + ["!", "\"", '(', ')', '*', '\'', '[', ']', '{', '}', '”', '“', '’' ,'‘' ,'¥' ,'©' ]
  d = SpellChecker("en_US")
  incorrectwords = [w for w in words if len(w)>0 and not d.check(w) and w not in ignorewords]
  suggestedwords = [d.suggest(w) for w in incorrectwords]
  print('INCORRECT WORDS: ', len(incorrectwords), incorrectwords)
  print('CORRECT WORDS: ', len(suggestedwords), suggestedwords)
  return (incorrectwords, suggestedwords)

# Get the final list of incorrect and suggeste words
def finalIncorrectAndSuggested(incorrectwords, suggestedwords):
  final_incorrectwords = []
  final_suggestedwords = []
  for i in range(len(suggestedwords)):
    if (len(suggestedwords[i]) <= 0):
        print()
    else :
      final_incorrectwords.append(incorrectwords[i])
      final_suggestedwords.append(suggestedwords[i])
  print('FINAL INCORRECT WORDS: ', len(final_incorrectwords), final_incorrectwords)
  print('FINAL CORRECT WORDS: ', len(final_suggestedwords), final_suggestedwords)
  return (final_incorrectwords, final_suggestedwords)

# replace incorrect words with [MASK]
def replaceMASK(text, text_original, final_incorrectwords):
  text_words = text.split()
  for i in range(len(text_words)):      # Doing this to remove 1 letter word
    if (len(text_words[i]) == 1 and (text_words[i]!='a' or text_words[i]!='A' or text_words[i]!=',' or text_words[i]!='.' or text_words[i]!='\'')):
      text_words[i] = ''
  # print('BEFORE: ', text_words)

  c=0
  for i in range(len(text_words)):
    for w in final_incorrectwords:
      if w == text_words[i]:
        text_words[i] = '[MASK]'
        c+=1
  print('AFTER: ', c)

  text_replaced = ""
  print(len(text_words))
  for i in range(len(text_words)):
    text_replaced += text_words[i] + " "

  text_original_replaced = text_replaced
  print('FINAL TEXT REPLACED WITH ERRORS: ', text_original_replaced)
  return (text_replaced, text_original_replaced)

def predict_word(text_original_replaced, final_suggestedwords):
  words_final = text_original_replaced.split()
  j = 0
  text_final = ""
  for i in range(len(words_final)):
    if words_final[i] == '[MASK]' :
      words_final[i] = final_suggestedwords[j][0]
      j += 1
    text_final += words_final[i] + " "
  return text_final
  # for i in range(len(final_suggestedwords)):
  #   predicted_token=''
  #   print(final_suggestedwords[i])
  #   if (len(final_suggestedwords[i])==0):
  #     return text_original_replaced
  #   predicted_token = final_suggestedwords[i][0]
  #   text_original_replaced = text_original_replaced.replace('[MASK]', predicted_token, 1)
  # return text_original_replaced

# file_ptr = open(os.path.join("./static/cleaned-images", "Paper", "Paper1") + ".txt", "r")
# text = file_ptr.read()
# text_original = text
# text = basicRemoval(text)
# text = cleanupText(text)
# words = wordSplit(text)
# propernoun = getProperNoun(words)
# email = getEmail(words)
# url = getURL(words)
# incorrectwords, suggestedwords = basicSpellCheck(propernoun, email, url, words)
# final_incorrectwords, final_suggestedwords = finalIncorrectAndSuggested(incorrectwords, suggestedwords)
# text_replaced, text_original_replaced = replaceMASK(text, text_original, final_incorrectwords)
# text_original_final = predict_word(text_original_replaced, final_suggestedwords)

# file_ptr_masked = open(os.path.join("./static/cleaned-images", "Paper", "Paper" + "-masked1") + ".txt", "a")
# file_ptr_masked.write(text_replaced)

# file_ptr_corrected = open(os.path.join("./static/cleaned-images", "Paper", "Paper" + "-corrected1") + ".txt", "a")
# file_ptr_corrected.write(text_original_final)
