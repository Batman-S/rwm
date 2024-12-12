import { useEffect } from "react";
import { io } from "socket.io-client";
import { partyStatus, userIdState } from "../recoil/store";
import { useRecoilValue, useSetRecoilState } from "recoil";
import { API_BASE_WS_URL } from "../config/config";

export interface Party {
  _id: string;
  name: string;
  user_id: string;
  party_size: number;
  status: string;
  created_at: string;
}
export interface Message {
  status: string;
  party: Party;
}

export const WebSocketHandler = () => {
  const userId = useRecoilValue(userIdState);
  const setPartyStatus = useSetRecoilState(partyStatus);
  useEffect(() => {
    const socketInstance = io(`${API_BASE_WS_URL}`, {
      query: { userId },
      transports: ["websocket"],
      path: "/ws/socket.io/",
    });

    socketInstance.on("connect", () => {
      console.log(`Socket.IO connected with userId: ${userId}`);
    });

    socketInstance.on("disconnect", (reason) => {
      console.log("Socket.IO disconnected:", reason);
    });

    socketInstance.on("user_message", (message: Message) => {
      console.log("Message received:", message);
      if (message.party._id === userId) {
        setPartyStatus(message.party.status);
        console.log("Setting party status", message.party.status);
      }
    });

    socketInstance.on("connect_error", (error) => {
      console.error("Socket.IO connection error:", error);
    });

    return () => {
      socketInstance.disconnect();
    };
  }, [userId, setPartyStatus]);

  return null;
};
