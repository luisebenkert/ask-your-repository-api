from consecution import Node
from textblob import Word
from application.artifacts.text_processing.variables import PRIORITY_FILTER_FUNCTION, PRIORITY_FILTER_MIN_PRIORITY, PRIORITY_FILTER_MIN_AMOUNT

class PriorityFilter(Node):
  def _get_best_results(self, item):
    prios = []
    for word in item:
      prio = item.get(word).get('priority')
      prios.append([word, prio])
    prios.sort(key=lambda element: element[1])
    best_results = list(filter(lambda element: element[1] >= PRIORITY_FILTER_MIN_PRIORITY, prios))
    if len(best_results) < PRIORITY_FILTER_MIN_AMOUNT:      
      best_results = prios[-PRIORITY_FILTER_MIN_AMOUNT:]
    words = [x[0] for x in best_results]
    return words

  def process(self, item):
    words = self._get_best_results(item)
    result = {}

    for key in words:
      result[key] = item.pop(key)

    self.push(result)