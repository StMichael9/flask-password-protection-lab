#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')

class Signup(Resource):

    def post(self):

        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
       
        if user:
            return {"error": "User already exists"}, 400
        
        new_user = User(username=username)
        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        return UserSchema().dump(new_user), 201
    

class Login(Resource):
    def post(self):

        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200

        return {'Error': "Unauthorized"}, 401



class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return UserSchema().dump(user), 200
        
        return {}, 401
    
class Logout(Resource):
    def delete(self):
        
        session.clear()
        return {}, 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)