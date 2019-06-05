"""
Handles all logic of the evaluation api
"""

from flask_apispec.views import MethodResource
from flask import request

import json
import datetime

class EvaluationView(MethodResource):  # pylint:disable=too-few-public-methods
  """Defines Routes on collection"""

  def post(self, **params):
    """Logic for updating an evaluation result"""
    evaluation_set = json.loads(json.loads(request.data)["evaluationSet"])
    for item in evaluation_set:
      date = datetime.datetime.now().strftime('%m%d_%H%M')
      search_terms = item["searchterms"]
      filename = date + '_'.join(search_terms)
      path = './.__data/ranking/' + filename + '.json'

      try:
        with open(path, 'w') as outfile:
          json.dump(item, outfile)
      except FileNotFoundError:
        print('File could not be found.')
      except:
        print('An error occured. File was not created.')
      else:
        print('File was successfully created.')
    