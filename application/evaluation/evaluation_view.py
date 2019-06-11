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
    data = json.loads(json.loads(request.data)['evaluationSet'])
    eval_type = data["type"]
    eval_set = data["set"]

    for item in eval_set:
      date = datetime.datetime.now().strftime('%m%d_%H%M')
      if eval_type == 'ranking':
        name = item["searchterms"]
        filename = date + '_'.join(name)
      elif eval_type == 'search_terms':        
        name = item["image"]
        filename = date + '_' + name
      else:
        return False
      
      path = './.__data/user_input/' + eval_type + '/' + filename + '.json'

      try:
        with open(path, 'w') as outfile:
          json.dump(item, outfile)
      except FileNotFoundError:
        print('File could not be found.')
      except:
        print('An error occured. File was not created.')
      else:
        print('File was successfully created.')
    