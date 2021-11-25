from core.Controller import Controller, Utils, Request, Response, json, datetime
from models.Group import Group, Course, Period, and_
from models.User_Group import User_Group, User


class GroupController(Controller):
    def get_query_string(self, req: Request, resp: Response, data: dict):
        filters = [Course.teacher_id == req.context.session.user.id]
        if data.get("period_id"):
            filters.append(Group.period_id == int(data.get("period_id")))

        if data.get("course_id"):
            filters.append(Group.course_id == int(data.get("course_id")))

        deleted = data.get("finished") == "True"

        #TODO Query string para jalar toda la info del grupo/os

        groups = Group.getAll(and_(*filters), deleted=deleted, join=Course)
        self.response(resp, 200, Utils.serialize_model(groups, recursive=True, recursiveLimit=2))
    
    def get_group_info(self, group):
        data = Utils.serialize_model(group, recursive=True, recursiveLimit=2)
        users_of_the_group = User_Group.getAll(User_Group.group_id == group.id, orderBy=User_Group.xp.desc())
        data["students"] = Utils.serialize_model(users_of_the_group, recursive=True, recursiveLimit=2, blacklist=["group"])
        return data

    def on_get(self, req: Request, resp: Response, id: int = None):
        query_strings = req.params
        if query_strings:
            return self.get_query_string(req, resp, query_strings)
        
        if id:
            group = Group.get(id)
            if not group:
                self.response(resp, 404, error=self.ID_NOT_FOUND)
                return
            
            self.response(resp, 200, self.get_group_info(group))
            return

        super().generic_on_get(
            req,
            resp,
            Group,
            id,
            filters=Course.teacher_id == req.context.session.user.id,
            join=Course
        )
    
    def on_get_otp(self, req: Request, resp: Response, id: int = None):
        if not id:
            self.response(resp, 405)
            return
        
        group = Group.get(id)
        if not group:
            self.response(resp, 404, error=self.ID_NOT_FOUND)
            return

        if not group.otp or not Utils.validate_otp(group.otp_time):
            group.otp = Utils.generate_otp(6)
            group.otp_time = datetime.utcnow()
            if not group.save():
                self.response(resp, 500, error=self.PROBLEM_SAVING_TO_DB)
                return
        
        self.response(resp, 200, Utils.serialize_model(group))


    def on_post(self, req: Request, resp: Response, id: int = None):
        super().generic_on_post(req, resp, Group, "groups", id)

    def on_put(self, req: Request, resp: Response, id: int = None):
        super().generic_on_put(req, resp, Group, id)

    def on_delete(self, req: Request, resp: Response, id: int = None):
        super().generic_on_delete(req, resp, Group, id)
