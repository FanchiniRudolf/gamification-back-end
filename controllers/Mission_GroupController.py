from core.Controller import Controller, Utils, Request, Response, json, datetime
from models.Mission_Group import Mission_Group, Mission, and_, Group
from models.User_Group import User_Group, User
from models.User_Mission import User_Mission
from models.Role import Role


class Mission_GroupController(Controller):

    # ---------------------- Mission to Group --------------------

    def get_query_string(self, req: Request, resp: Response, data: dict, group_id: int):
        filters=[Mission_Group.group_id == group_id]
        if data.get("mission_id"):
            filters.append(Mission_Group.mission_id == int(data["mission_id"]))

        mission_group = self.get_mission_group_info(Mission_Group.get(and_(*filters)))
        self.response(resp, 200, mission_group)


    def get_mission_group_info(self, mission_group: Mission_Group):
        data = Utils.serialize_model(mission_group, recursive=True, recursiveLimit=3, blacklist=["group", "teacher"] )
        user_groups = User_Group.getAll(User_Group.group_id == mission_group.group_id)
        user_groups = Utils.serialize_model(user_groups, recursive=True, recursiveLimit=2, blacklist=["group"])
        for user in user_groups:
            user_mission = User_Mission.get(User_Mission.enrollment_id == user.get("id"))
            user["mission_grade"] = user_mission.grade if user_mission else None
        
        data["students"] = user_groups
        return data

    def on_get(self, req: Request, resp: Response, id: int = None):
        query_strings = req.params
        if query_strings:
            return self.get_query_string(req, resp, query_strings, id)

        user: User = req.context.session.user
        # Si el usuario es un profesor llevar todas las misiones
        # Si es alumno solo las que ya empezo su start_date
        if user.role.id == Role.STUDENT:
            today = datetime.utcnow()
            mission_group = Mission_Group.getAll(and_(Mission_Group.group_id == id, Mission_Group.start_date <= today))
        else:
            mission_group = Mission_Group.getAll(Mission_Group.group_id == id)
        
        
        data = self.check_if_user_already_did_the_missions(id, user, mission_group)

        self.response(resp, 200, data)

    def check_if_user_already_did_the_missions(self, group_id: int, user: User, mission_group):
        # Si el usuario es un estudiante, poner banderas si ya entrego la misión
        if not mission_group: return []
        if user.role.id == Role.STUDENT:
            enrollment = User_Group.get(and_(User_Group.group_id == group_id, User_Group.student_id == user.id))
            return self.check_if_user_already_did_the_missions_helper(enrollment, mission_group)
        
        return Utils.serialize_model(mission_group, recursive=True, recursiveLimit=3, blacklist=["group", "teacher"])
            
    def check_if_user_already_did_the_missions_helper(self, enrollment: User_Group, mission_group):
        if isinstance(mission_group, list):
            data = []
            for mission in mission_group:
                data.append(self.check_if_user_already_did_the_missions_helper(enrollment, mission))
                return data

        elif isinstance(mission_group, Mission_Group):
            data = Utils.serialize_model(mission_group, recursive=True, recursiveLimit=2)
            user_mission = User_Mission.get(and_(User_Mission.enrollment_id == enrollment.id, User_Mission.mission_id == mission_group.mission_id))
            data["done"] = 1 if user_mission else 0
            return data

    def on_post(self, req: Request, resp: Response, id: int = None):
        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
            return

        extra_data = {
            "start_date": Utils.change_datetime_timezone_to_utc0(data.get('start_date')),
            "delivery_date":  Utils.change_datetime_timezone_to_utc0(data.get('delivery_date'))
            }

        super().generic_on_post(
            req,
            resp,
            Mission_Group,
            id=id,
            data=data, 
            extra_data=extra_data
        )
    
    def on_delete(self, req: Request, resp: Response, id: int = None):
        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
            return
        
        mission_group = Mission_Group.get(and_(
            Mission_Group.group_id == int(data.get("group_id")),
            Mission_Group.mission_id == int(data.get("mission_id"))
        ))
        if not mission_group:
            self.response(resp, 404, error="No se encontro ese registro")
            return
        
        mission_group_data = Utils.serialize_model(mission_group)
        if not mission_group.delete():
            self.response(resp, 500, error=self.PROBLEM_SAVING_TO_DB)
            return
        
        self.response(resp, 200, mission_group_data)
