import logging

from src.procedures import *

from src.proto.sn_users import service_pb2_grpc as user_pb2_grpc

logger = logging.getLogger(__name__)


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    """
    Implementation of UserService service
    Add your method and run make-gen to generate templates in src/procedures
    """

    def RegisterUser(self, request, context):
        return RegisterUser(request, context)

    def AuthenticateUser(self, request, context):
        return AuthenticateUser(request, context)

    def GetUserProfile(self, request, context):
        return GetUserProfile(request, context)

    def UpdateUserProfile(self, request, context):
        return UpdateUserProfile(request, context)
