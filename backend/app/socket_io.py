from app.websocket_manager import websocket_manager
from urllib.parse import parse_qs
import logging

logger = logging.getLogger("SocketIO")

async def setup_socketio_events(sio):
    """
    Register Socket.IO events with the given Socket.IO server instance.
    """

    @sio.event
    async def connect(sid, environ):
        query_string = environ.get("QUERY_STRING", "")
        query_params = parse_qs(query_string) 
        user_id = None
        user_id = query_params.get("userId", [None])[0]

        if not user_id:
            logger.error("Connection rejected: Missing user_id in query params.")
            return False

        logger.info(f"Socket.IO client connected: SID={sid}, User ID={user_id}")
        await websocket_manager.save_user_connection(sio, sid, user_id)

    @sio.event
    async def disconnect(sid):
        logger.info(f"Socket.IO client disconnected: SID={sid}")
        await websocket_manager.remove_user_connection(sio, sid)

    @sio.event
    async def user_message(sid, data):
        logger.info(f"Message from SID={sid}: {data}")
    
