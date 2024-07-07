import json
from app import create_app, db
from app.models import Role, Permission, RolePermission

def initialize_roles_and_permissions():
    app = create_app()
    with app.app_context():
        db.create_all()

        with open('initial_data.json') as f:
            data = json.load(f)

        # Create permissions
        permissions = {name: Permission(name=name) for name in data['permissions']}
        db.session.add_all(permissions.values())
        db.session.commit()

        roles = {}
        for role_data in data['roles']:
            role = Role(name=role_data['name'])
            db.session.add(role)
            db.session.commit()  # Commit to generate ID
            roles[role.name] = role
            for perm_name in role_data['permissions']:
                permission = permissions[perm_name]
                role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
                db.session.add(role_permission)

        db.session.commit()

        print("Roles and permissions initialized successfully.")

if __name__ == "__main__":
    initialize_roles_and_permissions()
