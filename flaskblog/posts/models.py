from datetime import datetime
from flaskblog import db

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __init__(self, title, content, user_id):
        super().__init__()
        self.title = title
        self.content = content
        self.user_id = user_id
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
