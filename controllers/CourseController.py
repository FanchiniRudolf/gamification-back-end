from core.Controller import Controller, Utils, Request, Response, json, datetime
from models.Course import Course


class CourseController(Controller):

    def on_get(self, req: Request, resp: Response, id: int = None):
        filter = Course.teacher_id == req.context.session.user.id
        super().generic_on_get(req, resp, Course, id, filters=filter)

    def on_post(self, req: Request, resp: Response, id: int = None):
        data = {"teacher_id": req.context.session.user.id}
        super().generic_on_post(req, resp, Course, "courses", id, extra_data=data)

    def on_put(self, req: Request, resp: Response, id: int = None):
        super().generic_on_put(req, resp, Course, id)

    def on_delete(self, req: Request, resp: Response, id: int = None):
        super().generic_on_delete(req, resp, Course, id)