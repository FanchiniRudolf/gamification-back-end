from core.Controller import Controller, Utils, Request, Response, json, datetime
from models.MissionType import MissionType, or_


class MissionTypeController(Controller):

    def on_get(self, req: Request, resp: Response, id: int = None):
        # sourcery skip: none-compare
        super().generic_on_get(
            req,
            resp,
            MissionType,
            id,
            or_(
                MissionType.teacher_id == None,
                MissionType.teacher_id == req.context.session.user.id,
            ),
        )


    def on_post(self, req: Request, resp: Response, id: int = None):
        extra_data = {"teacher_id": req.context.session.user.id}
        super().generic_on_post(
            req, 
            resp,
            MissionType,
            "mission-type",
            id,
            extra_data=extra_data
            )
    
    def on_put(self, req: Request, resp: Response, id: int = None):
        super().generic_on_put(req, resp, MissionType, id)

    def on_delete(self, req: Request, resp: Response, id: int = None):
        super().generic_on_delete(req, resp, MissionType, id, True)
    
