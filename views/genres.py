from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from service.decorators import auth_requered, admin_requered

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_requered
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_requered
    def post(self):
        reg_json = request.json
        new_genre = genre_service.create(reg_json)
        return "", 201, {"location": f"/{genre_ns.name}/{new_genre.id}"}



@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_requered
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_requered
    def put(self, rid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        genre_service.update(req_json)
        return "", 204

    @admin_requered
    def delete(self, rid):
        genre_service.delete(rid)
        return "", 204

