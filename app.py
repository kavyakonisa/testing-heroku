from flask import Flask
from flask import request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db=SQLAlchemy(app)


class Dishes(db.Model):

    __tablename__ = 'dishes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    dish_name = db.Column(
        db.String(100),
        index=True,
        unique=True,
        nullable=False
    )

    dish_cost = db.Column(
        db.String(100),
        index=True,
        nullable=False
    )

    dish_image=db.Column(
        db.String(100),
        index=True,
        nullable=False)

    def __init__(self,dish_name,dish_cost,dish_image):
      self.dish_name=dish_name
      self.dish_cost=dish_cost
      self.dish_image=dish_image

db.create_all()


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


#This error handler is used to display the   
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/")
def hello():
    return "Hello World!"


#create some test data for our website in the form of a list of dictionaries
def menu(dish):
  return {"dishID":dish.id,
      "dishName":dish.dish_name,
      "dishCost":dish.dish_cost,
      "dishImage":dish.dish_image

      }



# A route to return all of the available dishes in our catalog
@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['GET','PUT','DELETE'])
@app.route('/app/v1/resources/dishes', methods=['GET','POST','PUT','DELETE'])
@auth.login_required
def dish_actions(dish_id=None):
  
  if request.method=="GET" and dish_id==None :
    all_dishes=Dishes.query.all()
    all_dishes=list(map(menu,all_dishes))
    return jsonify(all_dishes)
 
# A route to add new dish to the dishes in our catalog 
  if request.method=="POST":
    dishName = request.form["dishName"]
    dishCost = request.form["dishCost"]
    if request.files:
        dishImage = request.files["dishImage"]
        dishImage.save(os.path.join(dishImage.filename))
        print("Image saved")
    dish=Dishes(dishName,dishCost,dishImage.filename)
    db.session.add(dish)
    db.session.commit()
    return jsonify(dish.id)    


# A route to delete all dishes in our catalog
  if request.method=="DELETE" and dish_id==None :
    dishes=Dishes.query.all()
    if dishes == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    del_list=[]
    for dish in dishes:
      del_list.append(dish.id)
      db.session.delete(dish)
    db.session.commit()
    return jsonify(del_list)


  if request.method==  "GET" and dish_id!=None:   
    dish=Dishes.query.filter_by(id=dish_id).first()
    if dish == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    else:
      return jsonify(menu(dish))





  if request.method=="PUT" and dish_id!=None:
    dish=Dishes.query.filter_by(id=dish_id).first()
    if dish == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    else:
      dishName = request.form["dishName"]
      dish.dish_name=dishName
      dishCost = request.form["dishCost"]
      dish.dish_cost=dishCost
      dish.dish_image=dishName
      db.session.commit()
      return jsonify(dish_id)

  if request.method=="DELETE" and dish_id!=None: 
    dish=Dishes.query.filter_by(id=dish_id).first()
    if dish == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    else:
      dish_id=dish.id
      db.session.delete(dish)
      db.session.commit()
      return jsonify(dish_id)



  


if __name__ == "__main__":
 app.run()