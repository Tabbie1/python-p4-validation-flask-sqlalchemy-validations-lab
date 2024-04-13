from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Input the name: Mandatory Required.")
        author = db.session.query(Author.id).filter_by(name = name).first()
        if author is not None:
            raise ValueError("The name already taken: Enter another name")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("The phone number should be 10 digits.")
        return phone_number
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

   

    @validates('content', 'summary')
    def validate_length(self, key, string):
        if( key == 'content'):
            if len(string) < 250:
                raise ValueError("The post content should be at least 250 characters.")
        if( key == 'summary'):
            if len(string) > 250:
                raise ValueError("The post summary should not exceed 250 characters.")
        return string

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category


    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Please provide a title.")
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("The title should include engaging keywords.")
        return title

    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'