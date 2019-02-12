from flask_restful import Resource
from flask import request

from app.core.schemas.views.last import LastRequest
from app.core.use_cases.last import LastUC


class LastResource(Resource):
    def get(self):
        request_data = request.args.to_dict(flat=True)

        kwargs, err = LastRequest().load(request_data)
        if err:
            pass
            # logger.errror
            # return validation request response
        cached, saved = LastUC().last(**kwargs)
        return [[o.created_at.isoformat() for o in saved], cached]
