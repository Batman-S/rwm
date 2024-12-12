import { apiClient } from "../components/api/apiClient";
export interface WaitlistParty {
  _id?: string;
  userId: string;
  name: string;
  partySize: number;
  status: string;
  timestamp: string;
}

class WaitlistService {
  async getWaitlist(): Promise<WaitlistParty[]> {
    try {
      const response = await apiClient.get<WaitlistParty[]>("/waitlist");
      return response.data;
    } catch (error) {
      console.error("Failed to fetch waitlist:", error);
      throw new Error("Could not fetch waitlist");
    }
  }

  async addToWaitlist(name: string, partySize: number): Promise<WaitlistParty> {
    try {
      const payload = { name, partySize };
      const response = await apiClient.post<WaitlistParty>(
        "/waitlist",
        payload
      );
      return response.data;
    } catch (error) {
      console.error("Failed to add party to waitlist:", error);
      throw new Error("Could not add to waitlist");
    }
  }

  async checkInParty(userId: string): Promise<void> {
    try {
      await apiClient.post(`/waitlist/${userId}/check-in`);
    } catch (error) {
      console.error("Failed to check in party:", error);
      throw new Error("Could not check in party");
    }
  }
}

export const waitlistService = new WaitlistService();
