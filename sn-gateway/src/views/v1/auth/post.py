from fastapi import APIRouter, Response
import grpc
import logging

from src.utils.auth import generate_token

from src.models.api import Authentication, Error
from src.proto.sn_users import service_pb2 as user_pb2
from src.proto.sn_users import service_pb2_grpc as user_pb2_grpc


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/v1/auth')

USER_SERVICE_ADDRESS = 'sn-users:50002'  # TODO: Use service discovery


@router.post('')
async def post_auth(auth: Authentication, response: Response) -> None | Error:
    try:
        async with grpc.aio.insecure_channel(USER_SERVICE_ADDRESS) as channel:  # TODO: move to secure_channel
            stub = user_pb2_grpc.UserServiceStub(channel)
            
            auth_request = user_pb2.AuthenticateUserRequest(
                username=auth.login,
                password=auth.password
            )
            
            auth_response = await stub.AuthenticateUser(auth_request)
            if not auth_response.success:
                return Error(
                    code=401,
                    message='Authentication failed: Invalid credentials'
                )
            
            token = generate_token(auth_response.id)
            
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
            
        logger.error(f'Authentication error: {rpc_error.details()}')
        response.status_code = error_code
        return Error(
            code=error_code,
            message=f'Authentication error'
        )
    except Exception as e:
        raise
        logger.error(f'Internal server error: {e}')
        return Error(code=500, message=f'Internal server error')
