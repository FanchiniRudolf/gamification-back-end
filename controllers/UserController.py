from core.Controller import Controller, Utils, Request, Response, json, datetime
from models.Role import Role, and_
from models.User_Group import User_Group, User, Group
from core.classes.SmtpClient import SmtpClient, EmailTemplate
from core.classes.Authenticator import Authenticator


class UserController(Controller):

    # ---------------------- create user for a group --------------------

    def on_post_user_group(self, req: Request, resp: Response):
        """
            Un profesor puede dar de alta usuarios y ligarlos a su grupo
            se les envía su información por correo
            Si el usuario ya existe solo se liga
        """

        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))
        
        if not data.get("email") or not data.get("group_id"):
            self.response(resp, 400, error="Se necesita el 'email' y el 'group_id'")
            return
        
        group = Group.get(int(data.get("group_id")))
        if not group: 
            self.response(resp, 404, error="No se encontro ningun grupo con ese id")
            return
        
        return_data = []
        client = SmtpClient.get_instance()
        for email in data.get("email"):
            valid = Utils.check_if_valid_email(email)
            if not valid:
                return_data.append({email: "No es un email valido"})
                continue

            user = User.get(User.email == email)
            if not user:
                user_data = {"email": email, "username": email, "password": Utils.generate_otp(5)}
                user = self.create_user(req, resp, user_data, True)
                if not user: 
                    return_data.append({email: "Error guardando usuario"})
                    continue
                client.send_email_to_pool(email, user_data, EmailTemplate.NEW_USER)
            
            user_already_in_group = User_Group.get(
                and_(
                    User_Group.group_id == group.id,
                    User_Group.student_id == user.id
                )
            )
            if user_already_in_group:
                return_data.append({email: "Ya esta en el grupo"})
                continue

            user_group = User_Group(
                group_id = group.id,
                student_id = user.id
            )
            if not user_group.save():
                return_data.append({email: "Error guardando user_group en la base de datos"})
            else:
                return_data.append(Utils.serialize_model(user_group, recursive=True, recursiveLimit=2))
            
        self.response(resp, 201, return_data)

    def on_get(self, req: Request, resp: Response, id: int = None):
        super().generic_on_get(req, resp, User, id)

    def on_post(self, req: Request, resp: Response, id=None):
        if id:
            self.response(resp, 405)
            return

        try:
            data: dict = json.loads(req.stream.read())
        except Exception as exc:
            print(exc)
            self.response(resp, 400, error=str(exc))

        if data.get("username") and data.get("password") and data.get("email"):
            return self.create_user(req, resp, data)
        
        self.response(resp, 400, error="Se necesita el 'username', 'password' y 'email' para crear a un nuevo usuario")
        
    def on_put(self, req: Request, resp: Response, id: int = None):
        super().generic_on_put(req, resp, User, id)

    def on_delete(self, req: Request, resp: Response, id: int = None):
        super().generic_on_delete(req, resp, User, id)

    # ------------------------------- Utils -------------------------------

    def create_user(self, req: Request, resp: Response, data: dict, return_user=False):
        exists, message = User.check_if_user_exists(
            data.get("username"), data.get("email")
        )
        if exists:
            self.response(resp, 409, error=message)
            print(message)
            return

        user, error_message, code = self.create_user_helper(data)
        if user is None:
            self.response(resp, code, error=error_message)
            print(error_message)
            return
        
        if return_user: return user

        session = Authenticator.login(
            user.email, data.get("password"), data.get("device_uuid", "unknown")
        )
        
        data = {
            "session": Utils.serialize_model(
                session, recursive=True, recursiveLimit=3, blacklist=["device"]
            )
        }

        self.response(resp, 201, data, message="Usuario creado exitosamente")
        resp.append_header("content_location", f"/users/{user.id}")

    def create_user_helper(self, data: dict):
        role = Role.TEACHER if data.get("is_teacher") == 1 else Role.STUDENT
        password_encrypted = Utils.get_hashed_string(data.get("password"))
        user = User(
            username=data.get("username"),
            password=password_encrypted,
            email=data.get("email"),
            role_id = role,
            name=data.get("name"),
            last_name=data.get("last_name"),
            school_id=data.get("school_id")
        )
        if not user.save():
            return None, self.PROBLEM_SAVING_TO_DB, 500

        return user, None, None
