from flask import Flask
from flask import request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
#added the basic authentication using flask_httpauth
auth=HTTPBasicAuth()
#This callback function will use to obtain the password for a given user.
@auth.get_password
def get_password(username):
  if username=='kavya':
    return 'python'
  return None 

#error-handler callback is used when it needs to send an unauthorized error
@auth.error_handler
def unauthorized():
    response = jsonify({'error':'Unauthorized access'})
    return response, 404

#create some test data for our website in the form of a list of dictionaries
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

# A route to return all of the available dishes in our catalog
@app.route('/app/v1/resources/dishes/all', methods=['GET'])
@auth.login_required
def api_all():
 return jsonify(dishes)

# A route to return the details of the matched id dish in our catalog 
@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['GET'])
@auth.login_required
def get_dish(dish_id):
#create an empty list for our results   
  results = []
#loop through to find the dish that matches the dish id       
  for dish in dishes:
    if dish['id'] == dish_id:
      results.append(dish)
#Use the jsnify function from flask to convert our dishes dictionary in JSON format
  return jsonify(results)


# A route to add new dish to the dishes in our catalog 
@app.route('/app/v1/resources/dishes', methods=['POST'])
@auth.login_required
def add_dish():
#Add the contents of the new dish with increasing the id with 1 and other entities in json format
  new_dish = {
        'id': dishes[-1]['id'] + 1,
        'title': request.json.get('title', ""),
        'cost': request.json.get('cost', ""),
         }
  dishes.append(new_dish)
  return jsonify({'new_dish_id': new_dish['id']}), 201
 
#This error handler is used to display the   
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



# A route to modify the existing dishes in our catalog
@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['PUT'])
@auth.login_required
#Update the matched dish with the given id to its respective contents
def update_dish(dish_id):
    dish = [dish for dish in dishes if dish['id'] == dish_id]
    if len(dish) == 0:
        return make_response(jsonify({'error': 'No dish'}), 400)
    if not request.json:
        return make_response(jsonify({'error': 'Not in json'}), 400)
    dish[0]['title'] = request.json.get('title', dish[0]['title'])
    dish[0]['cost'] = request.json.get('cost', dish[0]['cost'])
    return jsonify({'dish_id': dish[0]['id']})

# A route to delete a dish of the matched id in the dishes in our catalog
@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['DELETE'])
@auth.login_required
def delete_task(dish_id):
  dish = [dish for dish in dishes if dish['id'] == dish_id]
  if len(dish) == 0:
    return make_response(jsonify({'error': 'No dish'}), 400)
  dishes.remove(dish[0])
  return jsonify({'dish_id':dish[0]['id']})  

# A route to delete all dishes in our catalog
@app.route('/app/v1/resources/dishes', methods=['DELETE'])
@auth.login_required
def api_delete_all():
 if len(dishes) == 0:
  return make_response(jsonify({'error': 'No dish'}), 400)
 while(len(dishes)!=0): 
  for dish in dishes:
   dishes.remove(dish) 
 return jsonify({'result': True}) 


if __name__ == "__main__":
 app.run()