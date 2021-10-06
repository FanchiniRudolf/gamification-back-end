from core.Controller import Controller, Utils, Request, Response, json, datetime
from models.Period import Period, User


class PeriodController(Controller):

    def on_get(self, req: Request, resp: Response, id: int=None):
        filter = Period.teacher_id == req.context.session.user.id
        super().generic_on_get(req, resp, Period, id, filters=filter)
    
    def on_post(self, req: Request, resp: Response, id: int = None):
        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
            return
        

        data_formatted = {
            "teacher_id": req.context.session.user.id,
            "start_date": Utils.string_to_datetime(data.get("start_date")).date(),
            "end_date": Utils.string_to_datetime(data.get("end_date")).date()
        }
        super().generic_on_post(req, resp, Period, "periods", id, data=data, extra_data=data_formatted)

    def on_put(self, req: Request, resp: Response, id: int = None):
        super().generic_on_put(req, resp, Period, id)

    def on_delete(self, req: Request, resp: Response, id: int = None):
        super().generic_on_delete(req, resp, Period, id)


