import { atom, selector } from "recoil";
import { v4 as uuidv4 } from "uuid";
import { waitlistService } from "../services/waitlistService";

export enum PartyStatus {
  NotAvailable = "na",
  Waiting = "waiting",
  Ready = "ready",
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
  set: ({ set }, newValue) => {
    if (typeof newValue === "string" || newValue === null) {
      set(partyStatus, newValue);
    }
  },
});

export const userIdState = atom<string>({
  key: "userIdState",
  default: getOrCreateUserId(),
});
