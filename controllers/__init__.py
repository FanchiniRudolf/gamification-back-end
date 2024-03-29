from controllers.TestController import TestController
from controllers.HealthCheckController import HealthCheckController
from controllers.RoleController import RoleController
from controllers.StatusController import StatusController
from controllers.UserController import UserController
from controllers.NotificationController import NotificationController
from controllers.DeviceController import DeviceController
from controllers.FileLocalController import FileLocalController
from controllers.FileS3Controller import FileS3Controller
from controllers.PasswordRecoveryController import PasswordRecoveryController
from controllers.ConfirmEmailController import ConfirmEmailController
from controllers.SessionController import SessionController
from controllers.PeriodController import PeriodController
from controllers.CourseController import CourseController
from controllers.GroupController import GroupController
from controllers.User_GroupController import User_GroupController
from controllers.MissionTypeController import MissionTypeController
from controllers.MissionController import MissionController
from controllers.Mission_GroupController import Mission_GroupController
from controllers.User_MissionController import User_MissionController


testController = TestController()
healthcheckController = HealthCheckController()
roleController = RoleController()
statusController = StatusController()
userController = UserController()
notificationController = NotificationController()
deviceController = DeviceController()
filelocalController = FileLocalController()
files3Controller = FileS3Controller()
passwordrecoveryController = PasswordRecoveryController()
confirmemailController = ConfirmEmailController()
sessionController = SessionController()
periodController = PeriodController()
courseController = CourseController()
groupController = GroupController()
user_groupController = User_GroupController()
missiontypeController = MissionTypeController()
missionController = MissionController()
missiongroupController = Mission_GroupController()
usermissionController = User_MissionController()