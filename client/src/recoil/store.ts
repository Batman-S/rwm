import { atom, selector } from "recoil";
import { v4 as uuidv4 } from "uuid";
import { waitlistService } from "../services/waitlistService";

export enum PartyStatus {
  NotAvailable = "na",
  Waiting = "waiting",
  Ready = "ready",
  Completed = "completed",
}

// TODO: Add more robust user session management
const getOrCreateUserId = (): string => {
  const storedUserId = localStorage.getItem("userWaitlistId");
  if (storedUserId) {
    const parsedUserId = JSON.parse(storedUserId);
    if (parsedUserId.expiry > Date.now()) {
      return parsedUserId.id;
    }
  }
  const newUserId = {
    id: uuidv4(),
    expiry: Date.now() + 2 * 60 * 60 * 1000, // 2 hours
  };

  localStorage.setItem("userWaitlistId", JSON.stringify(newUserId));
  return newUserId.id;
};
export const partyStatus = atom<string | null>({
  key: "partyStatusAtom",
  default: null,
});

export const partyStatusSelector = selector<Promise<PartyStatus | null>>({
  key: "partyStatusSelector",
  get: async ({ get }) => {
    const userId = get(userIdState);
    if (!userId) {
      return null;
    }
    try {
      const status = await waitlistService.getStatus(userId);
      return status;
    } catch (error) {
      console.error("Failed to fetch party status:", error);
      return null;
    }
  },
});
export const userIdState = atom<string>({
  key: "userIdState",
  default: getOrCreateUserId(),
});
