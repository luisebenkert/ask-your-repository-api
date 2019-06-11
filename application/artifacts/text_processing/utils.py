from textblob import Word, TextBlob, blob
from application.artifacts.text_processing.variables import *
import nltk
import json
import datetime

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

def to_wordnet(tag=None):
  """Converts a Penn corpus tag into a Wordnet tag."""
  _wordnet = blob._wordnet
  if tag in ("NN", "NNS", "NNP", "NNPS"):
    return _wordnet.NOUN
  elif tag in ("JJ", "JJR", "JJS"):
    return _wordnet.ADJ
  elif tag in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"):
    return _wordnet.VERB
  elif tag in ("RB", "RBR", "RBS"):
    return _wordnet.ADV
  else:
    return _wordnet.NOUN

teams = {
  '8d1fbcfe-aae9-4f05-971e-da144b72f699': 'testSet1',
  'ba2340a3-e798-4956-baf2-4ba6c76a074f': 'testSet2',
}

def to_json(pipeline, output, input, team, vars):
  date = datetime.datetime.now().strftime('%m%d_%H%M')
  words = input[0].split()  
  search_terms = ''
  for element in words:
    search_terms += '_' + element
  filename = 'results_' + date + search_terms
  path = FILE_PATH + '/' + teams[str(team)] + '/' + filename + '.json'

  stages = {}
  for item in pipeline:
    item = str(item)
    stage = item[item.find("(")+1:item.find(")")]
    stages[stage] = vars[stage]

  data = {
    'pipeline': stages,
    'original': words,
    'processed': output
  }

  try:
    with open(path, 'w') as outfile:
      json.dump(data, outfile)
  except FileNotFoundError:
    print('File could not be found.')
  except:
    print('An error occured. File was not created.')
  else:
    print('File was successfully created.')

def sort_dict(dict):
  return sorted(dict.items(), key=lambda element: (-element[1]['priority'], -element[1]['amount']))