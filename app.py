from flask import Flask ,jsonify,make_response,request
from flask_migrate import Migrate
from models import db,User
from flask_restful import Api,Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

migrate= Migrate(app, db)
db.init_app(app)
api=Api(app)

class Index(Resource):
    def get(self):
        response_dict= {
            "Index":"Welcome"
        }
        response = make_response(
            jsonify(response_dict),
            200
        )
        return response

api.add_resource(Index,'/')

class Users(Resource):
    def get(self):
        names_list= [n.to_dict() for n in User.query.all()]

        response = make_response(
            jsonify(names_list),
            200,
        )

        return response
    def post(self):
        new_name = User(
            name=request.form['name']
        )
        db.session.add(new_name)
        db.session.commit()

        new_dict = new_name.to_dict()

        response= make_response(
            jsonify(new_dict),
            200
        )

        return response


api.add_resource(Users,'/users')

class UserByID(Resource):
    def get(self,id):
        name = User.query.filter_by(id=id).first.to_dict()

        name_dict = name.to_dict()
        response = make_response(
            jsonify(name_dict),
            200
        )
        return response
    
    def patch (self,id):
        name = User.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(name,attr,request.form[attr])
        db.session.add(name)
        db.session.commit()

        new_name=name.to_dict()
        response = make_response(
            jsonify(new_name),
            200,
        )
        return response
    
    def delete(self,id):
        name = User.query.filter_by(id=id).first()
        db.session.delete(name)
        db.session.commit()

        message_dict = {"message":"User has been successfully deleted"}

        response = make_response(jsonify(message_dict),204,)
        return response

api.add_resource(UserByID,'/users/<int:id>')

if __name__=="__main__":
    app.run(port=5050)