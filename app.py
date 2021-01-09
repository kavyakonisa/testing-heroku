from flask import Flask
from flask import request, jsonify, make_response
app = Flask(__name__)
dishes = [
    {'id': 0,
     'title': 'Chicken Biryani',
     'cost': '250',
     },
    {'id': 1,
     'title': 'Prawns Biryani',
     'cost': '450'},
    {'id': 2,
     'title': 'Mutton Biryani',
     'cost': '350'},
    {'id': 3,
     'title': 'Chicken Biryani',
     'cost': '250',
      },
    {'id': 4,
     'title': 'Prawns Biryani',
     'cost': '450'},
    {'id': 5,
     'title': 'Mutton Biryani',
     'cost': '350'}
]
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/app/v1/resources/dishes/all', methods=['GET'])
def api_all():
 return jsonify(dishes)

@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
   
  results = []
       
  for dish in dishes:
    if dish['id'] == dish_id:
      results.append(dish)

  return jsonify(results)

if __name__ == "__main__":
 app.run()