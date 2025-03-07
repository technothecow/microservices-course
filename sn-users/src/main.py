import asyncio
import logging
import grpc
from concurrent import futures

from src.proto.sn_users import service_pb2_grpc as users_pb2_grpc
from src.service import UserServiceServicer


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor())

    # Add the servicer to the server
    users_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)

    # Listen on configured port
    server_address = f'[::]:50002'
    server.add_insecure_port(server_address)
    await server.start()

    logging.info(f'Server started on {server_address}')

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
