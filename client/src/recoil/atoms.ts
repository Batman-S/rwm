import { atom } from "recoil";

const TOTAL_SEATS = 10;

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

export const restaurantState = atom({
  key: "restaurantState",
  default: { totalSeats: TOTAL_SEATS, availableSeats: TOTAL_SEATS },
});
