from flask import Flask, jsonify, Response
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restplus import Resource, Api
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',  # production env variables
    'sqlite:///db/db.sqlite')

CORS(app)
db = SQLAlchemy(app)
api = Api(app)


class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return str(id)

    def asdict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'caption': self.caption
        }


@api.route('/memes')
class MemesApi(Resource):

    def get(self):
        memes = Meme.query.order_by(Meme.id.desc()).limit(100).all()
        res = []
        for meme in memes:
            res.append(meme.asdict())
        return jsonify(res)

    def post(self):
        response = request.get_json() if request.is_json else request.form
        for arg in ['name', 'url', 'caption']:
            if not response.get(arg):
                return Response(status=400)

        if Meme.query.filter_by(name=response['name'],
                                url=response['url'],
                                caption=response['caption']).first() is not None:
            return Response(status=409)

        meme = Meme(name=response['name'],
                    url=response['url'],
                    caption=response['caption'])

        db.session.add(meme)
        db.session.commit()
        return jsonify(meme.id)


@api.route('/memes/<int:id>')
class SingleMemeApi(Resource):

    def get(self, id):
        meme = Meme.query.filter_by(id=id).first()
        if meme is None:
            return Response(status=404)

        return jsonify(meme.asdict())

    def patch(self, id):
        meme = Meme.query.filter_by(id=id).first()
        if meme is None:
            return Response(status=404)

        response = request.get_json() if request.is_json else request.form
        print(response)
        print(type(response))
        if response.get('url') is not None:
            meme.url = response['url']
        if response.get('caption') is not None:
            meme.caption = response['caption']
        db.session.commit()
        return Response(status=204)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8081, debug=True)
