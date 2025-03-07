from grpc import StatusCode
import logging

from src.db import PostgresDB
from src.crypto import hash_password

from src.proto.sn_users.service_pb2 import UserProfileResponse

logger = logging.getLogger(__name__)

def register_user_in_db(db, login, password, email) -> str:
    db.execute(
        'INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)',
        (login, password, email),
    )
    user_id = db.query(
        'SELECT id FROM users WHERE username = %s',
        (login,),
    )[0]['id']
    db.execute(
        'INSERT INTO user_profiles (user_id) VALUES (%s)',
        (user_id,),
    )
    return user_id

def RegisterUser(request, context):
    username, password, email = request.username, request.password, request.email
    password = hash_password(password)

    db = PostgresDB()
    result = db.query(
        'SELECT id FROM users WHERE username = %s',
        (username,),
    )

    if len(result) > 0:
        context.abort(StatusCode.ALREADY_EXISTS, 'User with this login already exists')
        return

    user_id = register_user_in_db(db, username, password, email)

    return UserProfileResponse(
        id=user_id,
        username=username,
        email=email
    )
