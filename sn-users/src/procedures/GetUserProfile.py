import grpc
from src.db import PostgresDB

from src.proto.sn_users.service_pb2 import UserProfileResponse

def GetUserProfile(request, context):
    user_id = request.id
    db = PostgresDB()
    result = UserProfileResponse()

    fetch_users = db.query("SELECT * FROM users WHERE id = %s", (user_id,))

    if len(fetch_users) != 1:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("User not found")
        return

    user = fetch_users[0]

    result.id = user_id
    result.username = user['username']
    result.email = user['email']
    if user['full_name'] is not None:
        result.name = user['full_name'].split(' ')[0]
        result.surname = ' '.join(user['full_name'].split(' ')[1:])
    if user['phone_number'] is not None:
        result.phone_number = user['phone_number']
    result.created_at = user['created_at']
    result.updated_at = user['updated_at']

    fetch_user_profile = db.query("SELECT * FROM user_profiles WHERE user_id = %s", (user_id,))
    if len(fetch_user_profile) != 1:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("User profile not found")
        return
    
    user_profile = fetch_user_profile[0]

    if user_profile['birth_date'] is not None:
        result.date_of_birth = user_profile['birth_date']

    return result
