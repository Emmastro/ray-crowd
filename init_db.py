import json

import bcrypt
from app import create_app, db
from app.models import Project, Role, Permission, RolePermission, User


def load_data():
    with open('data.json') as f:
        data = json.load(f)

    permissions = {}
    for permission_name in data['permissions']:
        permission = Permission(name=permission_name)
        db.session.add(permission)
        permissions[permission_name] = permission
    db.session.commit()

    roles = {}
    for role_data in data['roles']:
        role = Role(name=role_data['name'])
        db.session.add(role)
        roles[role_data['name']] = role
    db.session.commit()

    for role_data in data['roles']:
        role = roles[role_data['name']]
        for permission_name in role_data['permissions']:
            role_permission = RolePermission(role=role, permission=permissions[permission_name])
            db.session.add(role_permission)
    db.session.commit()

    users = {}
    for user_data in data['users']:
        print(user_data)
        user_data['role_id'] = roles[user_data.pop('role')].id
        user = User(**user_data)
        user.set_password(user_data['password'])
        db.session.add(user)
        users[user.username] = user
    db.session.commit()

    for project_data in data['projects']:
        project_data['owner_id'] = users[project_data.pop('owner')].id
        project = Project(**project_data)
        db.session.add(project)

    db.session.commit()


if __name__ == '__main__':
    app = create_app()

    
    with app.app_context():
        db.drop_all()
        db.create_all()
        load_data()