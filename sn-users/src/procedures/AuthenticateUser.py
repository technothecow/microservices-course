from src.db import PostgresDB
from src.crypto import verify_password

from src.proto.sn_users.service_pb2 import AuthResponse


def AuthenticateUser(request, context):
    username = request.username
    db = PostgresDB()

    result = db.query(
        'SELECT id, password_hash FROM users WHERE username = %s',
        (username,),
    )

    if len(result) == 0:
        return AuthResponse(success=False, id='')
    
    password = request.password
    hashed_password = result[0]['password_hash']
    if not verify_password(password, hashed_password):
        return AuthResponse(success=False, id='')

    user_id = result[0]['id']
    return AuthResponse(success=True, id=user_id)
