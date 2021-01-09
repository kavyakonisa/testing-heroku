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


@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['DELETE'])
def delete_task(dish_id):
  dish = [dish for dish in dishes if dish['id'] == dish_id]
  if len(dish) == 0:
    abort(404)
  dishes.remove(dish[0])
  return jsonify({'dish_id':dish[0]['id']})  

@app.route('/app/v1/resources/dishes', methods=['DELETE'])
def api_delete_all():
 if len(dishes) == 0:
  abort(404)
 while(len(dishes)!=0): 
  for dish in dishes:
   dishes.remove(dish) 
 return jsonify({'result': True}) 


if __name__ == "__main__":
 app.run()