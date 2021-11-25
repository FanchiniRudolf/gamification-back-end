from controllers import *
import configparser
from core.classes.Authenticator import Authenticator
from falcon import API
from core.Utils import Utils

class RouteLoader():

    def __init__(self, server, authorization_middleware):
        self.server:API = server
        self.authorization_middleware:Authenticator = authorization_middleware
        self.config = configparser.ConfigParser()
        self.config.read(Utils.get_config_ini_file_path())
        self.context_from_config = self.config.get('ROUTES', 'context')
        self.context_prefix = '/'+self.context_from_config if self.context_from_config != '' else ''

    def loadExceptionRoutes(self):
        self.authorization_middleware.add_exception_route(self.context_prefix + '/health-check/ping')
        self.authorization_middleware.add_exception_route(self.context_prefix + '/password-recovery/request')
        self.authorization_middleware.add_exception_route(self.context_prefix + '/password-recovery/validate-code')
        self.authorization_middleware.add_exception_route(self.context_prefix + '/sessions/login')
        self.authorization_middleware.add_exception_route(self.context_prefix + '/test')
        self.authorization_middleware.add_exception_route(self.context_prefix + '/users')
        

    def loadRoutes(self):
        self.server.add_route(self.context_prefix + '/periods', periodController)
        self.server.add_route(self.context_prefix + '/periods/{id:int}', periodController)
        self.server.add_route(self.context_prefix + '/courses', courseController)
        self.server.add_route(self.context_prefix + '/courses/{id:int}', courseController)
        self.server.add_route(self.context_prefix + '/groups', groupController)
        self.server.add_route(self.context_prefix + '/groups/{id:int}', groupController)
        self.server.add_route(self.context_prefix + '/groups/acces_code/{id:int}', groupController, suffix="otp")
        self.server.add_route(self.context_prefix + '/users_groups', user_groupController)
        self.server.add_route(self.context_prefix + '/users_groups/{id:int}', user_groupController)
        self.server.add_route(self.context_prefix + '/users_groups/student-info', user_groupController, suffix='user_info')
        self.server.add_route(self.context_prefix + '/missions-type', missiontypeController)
        self.server.add_route(self.context_prefix + '/missions-type/{id:int}', missiontypeController)
        self.server.add_route(self.context_prefix + '/missions', missionController)
        self.server.add_route(self.context_prefix + '/missions/{id:int}', missionController)
        self.server.add_route(self.context_prefix + '/missions-to-groups', missiongroupController)
        self.server.add_route(self.context_prefix + '/missions-to-groups/{id:int}', missiongroupController)
        self.server.add_route(self.context_prefix + '/user-mission', usermissionController)
        self.server.add_route(self.context_prefix + '/user-mission/{id:int}', usermissionController)
        self.server.add_route(self.context_prefix + '/user-mission/100-to-all', usermissionController, suffix='100_to_all')

        self.server.add_route(self.context_prefix + '/test', testController)
        self.server.add_route(self.context_prefix + '/health-check/{action}', healthcheckController) #ping
        self.server.add_route(self.context_prefix + '/sessions/{action}', sessionController) #login, logout
        self.server.add_route(self.context_prefix + '/sessions', sessionController)
        self.server.add_route(self.context_prefix + '/password-recovery/{action}', passwordrecoveryController) #request, validate-code, change-password
        self.server.add_route(self.context_prefix + '/confirm-email/{action}', confirmemailController) #request, validate-code
        self.server.add_route(self.context_prefix + '/status', statusController)
        self.server.add_route(self.context_prefix + '/status/{id:int}', statusController)
        self.server.add_route(self.context_prefix + '/files/local', filelocalController)
        self.server.add_route(self.context_prefix + '/files/local/{id:int}', filelocalController)
        self.server.add_route(self.context_prefix + '/files/local/base64', filelocalController, suffix='base64')
        self.server.add_route(self.context_prefix + '/files/local/base64/{id:int}', filelocalController, suffix='base64')
        self.server.add_route(self.context_prefix + '/files/s3', files3Controller)
        self.server.add_route(self.context_prefix + '/files/s3/{id:int}', files3Controller)
        self.server.add_route(self.context_prefix + '/files/s3/base64', files3Controller, suffix='base64')
        self.server.add_route(self.context_prefix + '/files/s3/base64/{id:int}', files3Controller, suffix='base64')
        self.server.add_route(self.context_prefix + '/notifications', notificationController)
        self.server.add_route(self.context_prefix + '/notifications/{id:int}', notificationController)

        #BackOffice
        self.server.add_route(self.context_prefix + '/users', userController)
        self.server.add_route(self.context_prefix + '/users/{id:int}', userController)
        self.server.add_route(self.context_prefix + '/users/group', userController, suffix="user_group")
        self.server.add_route(self.context_prefix + '/roles', roleController)
        self.server.add_route(self.context_prefix + '/roles/{id:int}', roleController)
        self.server.add_route(self.context_prefix + '/devices', deviceController)
        self.server.add_route(self.context_prefix + '/devices/{id:int}', deviceController)
        self.server.add_route(self.context_prefix + '/devices/token', deviceController, suffix='token')