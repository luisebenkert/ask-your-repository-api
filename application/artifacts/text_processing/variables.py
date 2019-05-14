import math
import inspect
from nltk.stem import PorterStemmer, SnowballStemmer

#### JSON EXPORT ####
FILE_PATH = './.__data'

#### SPELLCHECK ####
SPELLCHECK_MIN_CONFIDENCE = 0.01
SPELLCHECK_PRIORITY_FACTOR = 0.25
SPELLCHECK_PRIORITY_FUNCTION = lambda c: math.pow(c, SPELLCHECK_PRIORITY_FACTOR)

#### PART OF SPEECH FILTERING ####
PART_OF_SPEECH_CATEGORIES = {
    'nouns': {
        'pos': ['NN', 'NNS', 'NNP', 'NNPS'],
        'value': 1,
    },
    'verbs': {
        'pos': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
        'value': 1,
    },
    'ad_words': {
        'pos': ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'],
        'value': .9,
    },
    'wh_words': {
        'pos': ['WDT', 'WP', 'WPS', 'WRB'],
        'value': .6,
    },
    'pronouns': {
        'pos': ['PRP', 'PRPS'],
        'value': .7,
    },
    'foreign': {
        'pos': ['FW'],
        'value': 1,
    },
    'number': {
        'pos': ['CD'],
        'value': .8,
    },
    'others': {
        'pos': ['CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'RP', 'TO', 'UH'],
        'value': .2,
    },
}

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

def _get_lambda_string(func):
    funcString = str(inspect.getsourcelines(func)[0])
    return funcString.strip("['\\n']").split(" = ")[1]

#### EXPORT ####
ALL_VARIABLES = {
    'Spellcheck': {
        'min confidence': SPELLCHECK_MIN_CONFIDENCE,
        'priority factor': SPELLCHECK_PRIORITY_FACTOR,
        'priority function': _get_lambda_string(SPELLCHECK_PRIORITY_FUNCTION),
    },
    'Part of Speech Filter': {
        'categories': PART_OF_SPEECH_CATEGORIES,
        'priority function': _get_lambda_string(PART_OF_SPEECH_PRIORITY_FUNCTION),
    },
    'Priority Filter': {
        'min priority': PRIORITY_FILTER_MIN_PRIORITY,
        'min amount': PRIORITY_FILTER_MIN_AMOUNT,
        'function': _get_lambda_string(PRIORITY_FILTER_FUNCTION),
    },
    'Stemming': {
        'stemmer': STEMMER,
    },
    'Lemmatization': {
        'function': _get_lambda_string(LEMMATIZATION_FUNCTION),
    },
    'Synonyms': {
        'invalid characters': INVALID_CHARACTERS,
        'min similarity': SYNONYMS_MIN_SIMILARITY,
        'priority function': _get_lambda_string(SYNONYMS_PRIORITY_FUNCTION),
    },
}