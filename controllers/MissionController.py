from core.Controller import Controller, Utils, Request, Response, json, datetime
from models.Mission import Mission, and_


class MissionController(Controller):

# ------------------------------ Mission ------------------------

    def on_get(self, req: Request, resp: Response, id: int = None):
        super().generic_on_get(
            req,
            resp,
            Mission,
            id,
            Mission.teacher_id == req.context.session.user.id,
            recursive=True,
            recursive_limit=2, 
            blacklist=["teacher"]
        )
    
    def on_post(self, req: Request, resp: Response, id: int = None):
        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
            return

        start_date = Utils.change_datetime_timezone_to_utc0(data.get('start_date'))
        delivery_date = Utils.change_datetime_timezone_to_utc0(data.get('delivery_date'))
        
        extra_data = {
            "teacher_id": req.context.session.user.id,
            "start_date": start_date,
            "delivery_date": delivery_date
            }

        super().generic_on_post(
            req,
            resp,
            Mission,
            "missions",
            id,
            data=data,
            extra_data=extra_data
        )
    
    def on_put(self, req: Request, resp: Response, id: int = None):
        super().generic_on_put(
            req,
            resp,
            Mission,
            id
        )
    
    def on_delete(self, req: Request, resp: Response, id: int = None):
        super().generic_on_delete(
            req,
            resp,
            Mission,
            id,
            False
        )