// src/contexts/WebSocketContext.tsx
import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { io } from "socket.io-client";
import { userIdState } from "../recoil/atoms";
import { useRecoilValue } from "recoil";
import { API_BASE_WS_URL } from "../config/config";

interface WebSocketContextValue {
  globalUpdates: { status: string } | null;
}

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

const WebSocketContext = createContext<WebSocketContextValue | undefined>(
  undefined
);

export const WebSocketProvider = ({ children }: { children: ReactNode }) => {
  const [globalUpdates, setGlobalUpdates] = useState<{
    status: string;
  } | null>(null);
  const userId = useRecoilValue(userIdState);
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
        setGlobalUpdates({ status: message.status });
      }
    });

    socketInstance.on("connect_error", (error) => {
      console.error("Socket.IO connection error:", error);
    });

    return () => {
      socketInstance.disconnect();
    };
  }, [userId]);

  return (
    <WebSocketContext.Provider value={{ globalUpdates }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error("useWebSocket must be used within a WebSocketProvider");
  }
  return context;
};
