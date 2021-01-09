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

@app.route('/app/v1/resources/dishes', methods=['POST'])
@auth.login_required
def add_dish():
  new_dish = {
        'id': dishes[-1]['id'] + 1,
        'title': request.json.get('title', ""),
        'cost': request.json.get('cost', ""),
         }
  dishes.append(new_dish)
  return jsonify({'new_dish_id': new_dish['id']}), 201
  
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)




@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['PUT'])
@auth.login_required
def update_dish(dish_id):
    dish = [dish for dish in dishes if dish['id'] == dish_id]
    if len(dish) == 0:
        return make_response(jsonify({'error': 'No dish'}), 400)
    if not request.json:
        return make_response(jsonify({'error': 'Not in json'}), 404)
    dish[0]['title'] = request.json.get('title', dish[0]['title'])
    dish[0]['cost'] = request.json.get('cost', dish[0]['cost'])
    return jsonify({'dish_id': dish[0]['id']})


@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['DELETE'])
def delete_task(dish_id):
  dish = [dish for dish in dishes if dish['id'] == dish_id]
  if len(dish) == 0:
    return make_response(jsonify({'error': 'No dish'}), 400))
  dishes.remove(dish[0])
  return jsonify({'dish_id':dish[0]['id']})  

@app.route('/app/v1/resources/dishes', methods=['DELETE'])
def api_delete_all():
 if len(dishes) == 0:
  return make_response(jsonify({'error': 'No dish'}), 400)
 while(len(dishes)!=0): 
  for dish in dishes:
   dishes.remove(dish) 
 return jsonify({'result': True}) 


if __name__ == "__main__":
 app.run()