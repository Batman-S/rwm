from app.websocket_manager import websocket_manager
from typing import Dict

import logging

logger = logging.getLogger("WebSocketService")


class WebSocketService:
    """
    Service layer for WebSocket interactions.
    """
    @staticmethod
    async def notify_party_status(user_id: str, party: Dict, status: str):
        """
        Notify a specific party of their waitlist status.
        """
        try:
            message = {"status": status, "party": party}
            logger.info(f"Notifying party {user_id}. Status: {status}")
            
            from app.main import sio
            await websocket_manager.send_to_user(sio=sio, user_id=user_id, message=message)
            
        except Exception as e:
            logger.error(f"Failed to notify party {user_id}: {e}")
