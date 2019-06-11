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
    eval_name = data["name"]

    for item in eval_set:
      date = datetime.datetime.now().strftime('%m%d_%H%M')      
      name = item["searchterms"]
      filename = eval_type + '_' + date + '_' + '_'.join(name)
      path = './.__data/' + eval_name + '/' + filename + '.json'

      try:
        with open(path, 'w') as outfile:
          json.dump(item, outfile)
      except FileNotFoundError:
        print('File could not be found.')
      except:
        print('An error occured. File was not created.')
      else:
        print('File was successfully created.')
    