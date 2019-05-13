import math
from nltk.stem import PorterStemmer, SnowballStemmer

#### SPELLCHECK ####
SPELLCHECK_MIN_CONFIDENCE = 0.01
SPELLCHECK_PRIORITY_FACTOR = 0.25
SPELLCHECK_PRIORITY_FUNCTION = lambda c: math.pow(c, SPELLCHECK_PRIORITY_FACTOR)

#### PART OF SPEECH FILTERING ####
nouns = ['NN', 'NNS', 'NNP', 'NNPS']
verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
ad_words = ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']
wh_words = ['WDT', 'WP', 'WPS', 'WRB']
pronouns = ['PRP', 'PRPS']
foreign = ['FW']
number = ['CD']
others = ['CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'RP', 'TO', 'UH']

PART_OF_SPEECH_PRIORITY_FACTOR = [
    [nouns, 1],
    [verbs, 1],
    [ad_words, .9],
    [wh_words, .6],
    [pronouns, .7],
    [foreign, 1],
    [number, .8],
    [others, .2],
]

PART_OF_SPEECH_PRIORITY_FUNCTION = lambda c, p: c * p

#### PRIORITY FILTER ####
PRIORITY_FILTER_MIN_PRIORITY = 0.2
PRIORITY_FILTER_MIN_AMOUNT = 5
PRIORITY_FILTER_FUNCTION = lambda p: p < PRIORITY_FILTER_MIN_PRIORITY

#### STEMMING ####
STEMMERS = {
      'PORTER': PorterStemmer(),
      'SNOWBALL': SnowballStemmer('english'),
    }
STEMMER = 'SNOWBALL' # alternative: 'PORTER'

#### LEMMATIZATION ####
LEMMATIZATION_FUNCTION = lambda o, n: max([o, n])

#### SYNONYMS ####
INVALID_CHARACTERS = ['-', '_']
SYNONYMS_MIN_SIMILARITY = 0
SYNONYMS_PRIORITY_FUNCTION = lambda s: s * 0.8