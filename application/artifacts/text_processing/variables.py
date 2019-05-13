import math

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

#### FILTER ####
FILTER_MIN_PRIORITY = 0.5

FILTER_FUNCTION = lambda p: p < FILTER_MIN_PRIORITY