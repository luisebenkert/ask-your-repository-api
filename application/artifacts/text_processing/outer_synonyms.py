from consecution import Node
from textblob import Word
from itertools import permutations 
import re
import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
from application.artifacts.text_processing.utils import get_word
from application.artifacts.text_processing.variables import INVALID_CHARACTERS, SYNONYMS_MIN_SIMILARITY, SYNONYMS_PRIORITY_FUNCTION

class OuterSynonyms(Node): 
  def _get_lemma_names(self, synsets):
    lemmas = []
    for synset in synsets:
      lemma = synset.lemma_names()
      lemmas.extend(lemma)
    return lemmas

  def _is_invalid(self, word):
    return any(char in word for char in INVALID_CHARACTERS)

  def get_exact_synset(self, word):
    synsets = Word(word).synsets
    for item in synsets:      
      string = item.name()      
      result = string[string.find("'")+1:string.find(".")]
      if result == word:
        return item
    return None

  def get_best_synonyms(self, word, synonyms):
    result = []
    original_set = self.get_exact_synset(word)
    if original_set is None:
      return result
    for element in synonyms:        
      new_set = self.get_exact_synset(element)
      if new_set is None:
        continue
      similarity = original_set.path_similarity(new_set)
      if similarity and similarity >= SYNONYMS_MIN_SIMILARITY:
        result.append([element, similarity])
    return result

  def _get_outer_synonyms(self, synsets):
    all_sets = []
    for synset in synsets:
      hypernyms = synset.hypernyms()
      hyponyms = synset.hyponyms()
      holonyms = synset.member_holonyms()
      meronyms = synset.part_meronyms()
      all_sets.extend(hypernyms)
      all_sets.extend(hyponyms)
      all_sets.extend(holonyms)
      all_sets.extend(meronyms)

    return all_sets

  def process(self, item):
    words = get_word(item)
    all_synonyms = []

    for word in words:    
      synsets = word.synsets

      outer_synonyms = self._get_outer_synonyms(synsets)

      lemmas = self._get_lemma_names(outer_synonyms)
      lemmas = list(dict.fromkeys(lemmas))

      filtered = [i for i in lemmas if not self._is_invalid(i)]

      synonyms = self.get_best_synonyms(word, filtered)
      all_synonyms.extend(synonyms)

    for element in all_synonyms:
      word = element[0]
      similarity = element[1]
      if word in item:
        item[word]['amount'] += 1
      else:
        item[word] = {
          'priority': SYNONYMS_PRIORITY_FUNCTION(similarity), 
          'amount': 1
        }

    self.push(item)