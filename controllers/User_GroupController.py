from core.Controller import Controller, Utils, Request, Response, json, datetime
from models.User_Group import User_Group, User, Group, and_


class User_GroupController(Controller):

    def on_get(self, req: Request, resp: Response, id: int = None):
        student = req.context.session.user
        groups = Group.getAll(
            User_Group.student_id == student.id
            ,join=User_Group
        )
        self.response(resp, 200, Utils.serialize_model(groups, recursive=True, recursiveLimit=3))

    def on_post(self, req: Request, resp: Response, id: int = None):
        if id:
            self.response(resp, 405)
            return
        
        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
            return
        
        # Mover estas validaciones a su propio metodo
        if not data.get("otp"):
            self.response(resp, 400, error="Se necesita el otp del grupo")
            return
        
        group = Group.get(Group.otp == data.get("otp"))
        if not group:
            self.response(resp, 404, error="No hay ningun grupo con ese otp")
            return
        
        if not Utils.validate_otp(group.otp_time):
            self.response(resp, 409, error="Este otp ya expiró")
            return

        user_group = User_Group(
            group_id=group.id,
            student_id=req.context.session.user.id
        )
        if not user_group.save():
            self.response(resp, 500, error=self.PROBLEM_SAVING_TO_DB)
            return
        
        self.response(resp, 201, Utils.serialize_model(user_group, recursive=True, recursiveLimit=2))
        resp.append_header("content_location", f"/users_groups/{user_group.id}")

    def on_put(self, req: Request, resp: Response, id: int = None):
        super().generic_on_put(req, resp, User_Group, id)

    def on_delete(self, req: Request, resp: Response, id: int = None):
        super().generic_on_delete(req, resp, User_Group, id)