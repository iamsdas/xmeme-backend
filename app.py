from flask import Flask, jsonify, Response
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Meme(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(80), nullable=False)
    url: str = db.Column(db.String(80), nullable=False)
    caption: str = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return str(id)

    def asdict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "caption": self.caption
        }


@app.route("/meme", methods=["GET"])
def getMemes():
    res = []
    memes = Meme.query.all()
    for meme in memes:
        res.append(meme.asdict())
    return jsonify(res)


@app.route("/meme", methods=["POST"])
def addMeme():
    if(request.is_json):
        response = (request.get_json())
    else:
        response = (request.form)

    for args in ["name", "url", "caption"]:
        if not response[args]:
            return Response(status=400)

    meme = Meme(name=response["name"],
                url=response["url"],
                caption=response["caption"])

    db.session.add(meme)
    db.session.commit()

    return jsonify(meme.id)


@app.route("/meme/<id>", methods=["GET"])
def getMemeById(id):
    meme = Meme.query.filter_by(id=id).first()
    if meme is None:
        return Response(status=404)
    return jsonify(meme.asdict())


if __name__ == '__main__':
    app.run(debug=True)
