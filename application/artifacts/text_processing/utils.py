from textblob import TextBlob, Word

def get_word(list):
  result = []
  for item in list:
    word = Word(item)
    result.append(word)
  return result

def get_string(list):
  keys = []
  for key in list:
    keys.append(key)
  return ' '.join(keys) 

def get_blob(list):
  string = get_string(list)
  return TextBlob(string)

def combine_priorities(old_prio, new_prio):
  print(old_prio)
  print(new_prio)