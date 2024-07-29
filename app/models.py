from dataclasses import dataclass

from .extensions import db, bcrypt
from datetime import datetime

@dataclass
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    
    password = db.Column(db.String(150), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    gender = db.Column(db.String(50), nullable=True)
    _date_of_birth = db.Column('date_of_birth', db.Date, nullable=True)
    country = db.Column(db.String(100), nullable=True)
    research_interests = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        if isinstance(value, str) and value == "":
            self._date_of_birth = None
        elif isinstance(value, str):
            self._date_of_birth = datetime.strptime(value, '%Y-%m-%d').date()
        elif isinstance(value, datetime.date):
            self._date_of_birth = value
        else:
            self._date_of_birth = None

@dataclass
class Project(db.Model):
    __tablename__ = 'projects'
    author: str
    project_id: int = db.Column(db.Integer, primary_key=True, )
    title: str = db.Column(db.String(150), nullable=False)
    description: str = db.Column(db.Text, nullable=True)
    topic: str = db.Column(db.String(100), nullable=False)
    is_public: bool = db.Column(db.Boolean, default=False, nullable=False)
    owner_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('projects', lazy=True))
    created_at: datetime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'
    
    @property
    def author(self):
        return self.owner.username

@dataclass
class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Permission {self.name}>'

@dataclass
class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('role_permissions', lazy=True))
    permission = db.relationship('Permission', backref=db.backref('role_permissions', lazy=True))

    def __repr__(self):
        return f'<RolePermission Role: {self.role.name}, Permission: {self.permission.name}>'

@dataclass
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<TokenBlocklist {self.jti}>'


