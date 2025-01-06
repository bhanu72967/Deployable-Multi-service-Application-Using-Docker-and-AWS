from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://user:password@comment_db/comment_service')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', '038f48cacc0793319d521357220b563ff46632d998fcae135eaae566fd71dc3c')
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

@app.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    comment = Comment(content=data['content'], blog_id=data['blog_id'], author_id=user_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5003, debug=True)
