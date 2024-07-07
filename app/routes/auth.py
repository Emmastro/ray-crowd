from flask import Blueprint, request, jsonify
from app.models import TokenBlocklist, User, db, Role
from app.extensions import bcrypt
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    researcher_role = Role.query.filter_by(name='Researcher').first()

    if not researcher_role:
        return jsonify(message="Researcher role not found"), 400

    new_user = User(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        gender=data.get('gender'),
        date_of_birth=data.get('date_of_birth'),
        country=data.get('country'),
        research_interests=data.get('research_interests'),
        role=researcher_role
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return jsonify(message="User registered", access_token=access_token), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    token = TokenBlocklist(jti=jti)
    db.session.add(token)
    db.session.commit()
    return jsonify(message="Successfully logged out"), 200


@auth_bp.route('/auth_check', methods=['GET'])
@jwt_required()
def auth_check():
    return '', 200
