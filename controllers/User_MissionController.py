from core.Controller import Controller, Utils, Request, Response, json
from models.User_Mission import User_Mission, Mission, User_Group, and_
from models.Group import Group


class User_MissionController(Controller):

    def on_post_100_to_all(self, req: Request, resp: Response, id: int = None):
        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
            return
        
        group = Group.get(int(data.get('group_id')))
        mission = Mission.get(int(data.get("mission_id")))
        if not group:
            error_message = "No se encontro ese grupo"
            self.response(resp, 404, error=error_message)
            return
        if not mission:
            error_message = "No se encontro la misión"
            self.response(resp, 404, error=error_message)
            return
        
        enrollments = User_Group.getAll(User_Group.group_id == group.id)
        users_missions = []
        for enrollment in enrollments:
            enrollment: User_Group = enrollment
            # Si el alumno no tiene un registro aún se lo creamos, si no actualizamos el existente
            user_mission = User_Mission.get(and_(
                User_Mission.enrollment_id == enrollment.id,
                User_Mission.mission_id == mission.id
                )
            )
            
            if not user_mission:
                user_mission = self.create_user_mission(
                    100,
                    mission,
                    enrollment
                )
                
            else:
                user_mission.grade = 100
                user_mission.xp = mission.xp
                self.xp_or_coins_change(user_mission, 100)
            
            users_missions.append(user_mission)
        
        self.response(resp, 200, Utils.serialize_model(users_missions))

    def get_query_string(self, req: Request, resp: Response, data: dict):
        filters = []
        if data.get('enrollment_id'):
            filters.append(User_Mission.enrollment_id == int(data.get('enrollment_id')))
        
        if data.get('mission_id'):
            filters.append(User_Mission.mission_id == int(data.get('mission_id')))

        user_mission = User_Mission.get(and_(*filters))
        self.response(resp, 200, Utils.serialize_model(user_mission))

    def on_get(self, req: Request, resp: Response, id:int = None):
        query_strings = req.params
        if query_strings:
            return self.get_query_string(req, resp, query_strings)
        
    
    def create_user_mission(self, grade: int, mission: Mission, enrollment: User_Group, coins: int = 0, comment: str =None):
        xp = (grade * mission.xp)/100

        user_mission = User_Mission(
            enrollment_id=enrollment.id,
            mission_id=mission.id,
            grade=grade,
            coins=coins,
            xp=xp,
            comments=comment
        )

        if not user_mission.save():
            return
        
        # Le sumamos al estudiante el xp que le dieron y las monedas
        enrollment.xp = enrollment.xp + xp
        enrollment.coins = enrollment.coins + user_mission .coins 
        if not enrollment.save():
            return
        
        return user_mission
    
    def on_post(self, req: Request, resp: Response, id: int=None):
        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
            return
        
        grade = int(data.get('grade'))
        mission = Mission.get(int(data.get("mission_id")))
        if not mission:
            self.response(resp, 404, error="No se encontro esa misión")
            return

        enrollment = User_Group.get(int(data.get("enrollment_id")))
        if not enrollment:
            self.response(resp, 404, error="No se encontro ese enrollment")
            return
        
        user_mission = self.create_user_mission(
            grade,
            mission,
            enrollment,
            int(data.get("coins")),
            data.get("comments")
        )

        if not user_mission:
            self.response(resp, 500, error=self.PROBLEM_SAVING_TO_DB)
            return
        
        self.response(resp, 201, Utils.serialize_model(user_mission))

    
    def on_put(self, req: Request, resp: Response, id: int = None):
        query_string = req.params
        user_mission = User_Mission.get(and_(
            User_Mission.enrollment_id == int(query_string.get("enrollment_id")),
            User_Mission.mission_id == int(query_string.get("mission_id"))
            )
        )
        if not user_mission:
            self.response(resp, 404, error =self.ID_NOT_FOUND)
            return
        
        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
            return
            
        past_coins = user_mission.coins

        if (
            not self.set_values(user_mission, data)
            or not self.xp_or_coins_change(user_mission, int(data.get("grade")), int(data.get("coins")), past_coins)
        ):
            self.response(resp, 500, error= self.PROBLEM_SAVING_TO_DB)
            return
            
        self.response(resp, 200, Utils.serialize_model(user_mission, recursive=True, recursiveLimit=2))

    
    def xp_or_coins_change(self, user_mission: User_Mission, grade: int = None, new_coins: int = None, past_coins: int = 0):
        # Si se cambio la calificación, actualizamos el xp del usuario
        if grade:
            mission = user_mission.mission
            xp = (grade * mission.xp)/100
            previous_xp = user_mission.xp
            user_mission.xp = xp
            
            # actualizamos el xp del student
            student = user_mission.enrollment
            student.xp = student.xp - previous_xp + xp
            if not student.save() or not user_mission.save():
                return False
        
        # si actualizan las monedas, se las cambiamos al enrollment
        if new_coins:
            student = user_mission.enrollment
            student.coins = student.coins - past_coins + new_coins
            if not student.save():
                return False
        
        return True
