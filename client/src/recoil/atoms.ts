import { atom } from "recoil";
import { v4 as uuidv4 } from "uuid";

export enum QueueStatus {
  Waiting = "waiting",
  Ready = "ready",
  Serving = "serving",
  Completed = "completed",
}

const getOrCreateUserId = (): string => {
  const storedUserId = localStorage.getItem("userId");
  if (storedUserId) {
    return storedUserId;
  }
  const newUserId = uuidv4();
  localStorage.setItem("userId", newUserId);
  return newUserId;
};

export const queueState = atom({
  key: "queueState",
  default: [] as {
    id: string;
    name: string;
    partySize: number;
    status: QueueStatus.Waiting;
  }[],
});

export const userIdState = atom<string>({
  key: "userIdState",
  default: getOrCreateUserId(),
});
