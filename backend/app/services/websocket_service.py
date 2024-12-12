from app.websocket_manager import websocket_manager
from typing import Dict
import logging

logger = logging.getLogger("WebSocketService")


class WebSocketService:
    """
    Service layer for WebSocket interactions.
    """

    @staticmethod
    async def send_to_user(user_id: str, message: Dict):
        """
        Send a JSON message to a specific user identified by their user ID.
        """
        try:
            logger.info(f"Sending message to user {user_id}: {message}")
            await websocket_manager.send_to_user(user_id, message)
        except Exception as e:
            logger.error(f"Failed to send message to user {user_id}: {e}")

    @staticmethod
    async def notify_ready_party(user_id: str, party: Dict):
        """
        Notify a specific party that they are ready to be seated.
        """
        try:
            message = {"status": "ready", "user_id": user_id}
            logger.info(f"Notifying party ready {user_id} with message: {message}")
            from app.main import sio
            await websocket_manager.send_to_user(sio=sio, user_id=user_id, message=message)
        except Exception as e:
            logger.error(f"Failed to notify party {user_id}: {e}")
