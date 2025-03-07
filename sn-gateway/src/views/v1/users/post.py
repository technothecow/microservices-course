from fastapi import APIRouter, Response
import grpc
import logging

from src.utils.auth import generate_token

from src.models.api import UserRegistration, Error
from src.proto.sn_users import service_pb2 as user_pb2
from src.proto.sn_users import service_pb2_grpc as user_pb2_grpc


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/v1/users')

USER_SERVICE_ADDRESS = 'sn-users:50002'  # TODO: Use service discovery


@router.post('')
async def post_v1_users(auth: UserRegistration, response: Response) -> None | Error:
    try:
        async with grpc.aio.insecure_channel(USER_SERVICE_ADDRESS) as channel:  # TODO: move to secure_channel
            stub = user_pb2_grpc.UserServiceStub(channel)
            
            request = user_pb2.RegisterUserRequest(
                username=auth.login,
                password=auth.password,
                email=str(auth.email)
            )

            response = await stub.RegisterUser(request)
            token = generate_token(response.id)
            
            response.set_cookie(
                key='auth_token', 
                value=token,
                httponly=True,
                secure=True,
                samesite='strict',
                path='/',
                max_age=3600  # 1 hour
            )
            
            return
    except grpc.RpcError as rpc_error:
        error_code = 500
        if rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
            error_code = 503
        elif rpc_error.code() == grpc.StatusCode.UNAUTHENTICATED:
            error_code = 401
        elif rpc_error.code() == grpc.StatusCode.ALREADY_EXISTS:
            error_code = 409
            
        logger.error(f'Authentication error: {rpc_error.details()}')
        response.status_code = error_code
        return Error(
            code=error_code,
            message=f'Authentication error'
        )
    except Exception as e:
        logger.error(f'Internal server error: {e}')
        return Error(code=500, message=f'Internal server error')
