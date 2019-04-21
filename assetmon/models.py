from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role {self.name}'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

    def __repr__(self):
        return f'User {self.username}'

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String, unique=True)
    subdomain_search_ran = db.Column(db.Boolean(), nullable=False)
    #subdomains = db.relationship('Subdomain', secondary='subdomain',
                            #backref=db.backref('subdomain', lazy='dynamic'))


    def __repr__(self):
        return f'<Domain {self.domain}>'

class Subdomain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subdomain = db.Column(db.String, unique=True, nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), nullable=False)


