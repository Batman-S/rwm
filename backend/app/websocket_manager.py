from typing import Dict, List
import logging

logger = logging.getLogger("WebSocketManager")

class WebSocketManager:
    def __init__(self):
        self.user_connections: Dict[str, List[str]] = {} # Stores list of SIDs

    async def save_user_connection(self, sio, sid: str, user_id: str):
        """
        Save a new connection for the given user.
        """
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(sid)
        logger.info(f"User {user_id} connected with SID={sid}")

    async def remove_user_connection(self, sio, sid: str):
        """
        Remove a connection for a given user.
        """
        for user_id, sids in self.user_connections.items():
            if sid in sids:
                sids.remove(sid)
                if not sids:
                    del self.user_connections[user_id]
                logger.info(f"Removed SID={sid} for user {user_id}")
                break

    async def send_to_user(self, sio, user_id: str, message: dict):
        """
        Send a message to all connections of the given user.
        """
        if user_id in self.user_connections:
            for sid in self.user_connections[user_id]:
                try:
                    await sio.emit("user_message", message, room=sid)
                    logger.info(f"Message sent to user {user_id}: {message}")
                except Exception as e:
                    logger.error(f"Failed to send message to user {user_id}: {e}")

websocket_manager = WebSocketManager()
