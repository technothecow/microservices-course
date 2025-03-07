from fastapi import APIRouter, Response, Request
import grpc
import logging
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

from src.utils.auth import decode_token

from src.models.api import UserProfile, Error
from src.proto.sn_users import service_pb2 as user_pb2
from src.proto.sn_users import service_pb2_grpc as user_pb2_grpc


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/v1/users/me')

USER_SERVICE_ADDRESS = 'sn-users:50002'  # TODO: Use service discovery

def timestamp_to_iso8601(timestamp):
    """Convert protobuf Timestamp to ISO 8601 string format for OpenAPI."""
    if not timestamp or isinstance(timestamp, Timestamp) and timestamp == Timestamp():
        return None
    
    # Convert timestamp to datetime
    dt = datetime.fromtimestamp(timestamp.seconds + timestamp.nanos/1e9)
    
    # Format as ISO 8601 string
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


@router.get('')
async def get_v1_users_me(request: Request, response: Response) -> UserProfile | Error:
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        response.status_code = 401
        return Error(
            code=401,
            message='Unauthorized'
        )

    try:
        jwt_decoded = decode_token(auth_token)
        user_id = jwt_decoded['user_id']
    except Exception as e:
        logger.error(f'JWT decoding error: {e}')
        response.status_code = 401
        return Error(
            code=401,
            message='Unauthorized'
        )
        
    try:
        async with grpc.aio.insecure_channel(USER_SERVICE_ADDRESS) as channel:  # TODO: move to secure_channel
            stub = user_pb2_grpc.UserServiceStub(channel)
            
            request = user_pb2.GetUserProfileRequest(
                id=user_id
            )

            response = await stub.GetUserProfile(request)
            
            return UserProfile(
                id=response.id,
                login=response.username,
                email=response.email,
                name=response.name,
                surname=response.surname,
                dateOfBirth=response.date_of_birth if response.date_of_birth else None,
                phoneNumber=response.phone_number if response.phone_number else None,
                createdAt=timestamp_to_iso8601(response.created_at),
                updatedAt=timestamp_to_iso8601(response.updated_at)
            )
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
