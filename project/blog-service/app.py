from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://user:password@blog_db/blog_service')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', '038f48cacc0793319d521357220b563ff46632d998fcae135eaae566fd71dc3c')
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

@app.route('/blogs', methods=['POST'])
@jwt_required()
def create_blog():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    blog = Blog(title=data['title'], content=data['content'], author_id=user_id)
    db.session.add(blog)
    db.session.commit()
    return jsonify({'message': 'Blog created successfully'}), 201

@app.route('/blogs', methods=['GET'])
def list_blogs():
    blogs = Blog.query.all()
    return jsonify([{'id': b.id, 'title': b.title, 'content': b.content, 'author_id': b.author_id} for b in blogs])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)
