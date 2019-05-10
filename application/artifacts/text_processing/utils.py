from textblob import TextBlob, Word

def getWord(list):
  result = []
  for item in list:
    word = Word(item)
    result.append(word)
  return result

def getString(list):
  keys = []
  for key in list:
    keys.append(key)
  return ' '.join(keys) 

def getBlob(list):
  string = getString(list)
  return TextBlob(string)