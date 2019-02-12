from flask_restful import Resource, reqparse
from flask import jsonify, request
from app.core.schemas.views.grab_and_save import GrabAndSaveRequest


reqparse.RequestParser()


class GrabAndSaveResource(Resource):
    def post(self):
        # TODO: Make as a task in celery
        from app.core.use_cases.grab_and_save import GrabAndSaveUC

        kwargs, err = GrabAndSaveRequest().load(request.json)
        if err:
            pass
            # logger.errror
            # return validation request response
        GrabAndSaveUC().grab_and_save(**kwargs)

        return jsonify({"status": "OK"})
