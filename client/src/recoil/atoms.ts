import { atom } from "recoil";

enum QueueStatus {
  Waiting = "waiting",
  Ready = "ready",
  Serving = "serving",
  Completed = "completed",
}

export const queueState = atom({
  key: "queueState",
  default: [] as {
    id: string;
    name: string;
    partySize: number;
    status: QueueStatus.Waiting;
  }[],
});
