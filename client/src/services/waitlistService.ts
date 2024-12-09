// /src/services/waitlistService.ts
import { apiClient } from "../components/api/apiClient";

export interface WaitlistParty {
  _id?: string;
  name: string;
  partySize: number;
  timestamp: string;
}

class WaitlistService {
  private pollingIntervalId: NodeJS.Timeout | null = null;

  startPolling(
    interval: number,
    onDataReceived: (data: WaitlistParty[]) => void,
    onError: (error: Error) => void
  ) {
    if (this.pollingIntervalId) {
      // If polling is already active, clear the previous interval
      clearInterval(this.pollingIntervalId);
    }

    const fetchData = async () => {
      try {
        const waitlistData = await this.getWaitlist();
        onDataReceived(waitlistData);
      } catch (error) {
        onError(error as Error);
      }
    };

    fetchData();
    this.pollingIntervalId = setInterval(fetchData, interval);
  }

  stopPolling() {
    if (this.pollingIntervalId) {
      clearInterval(this.pollingIntervalId);
      this.pollingIntervalId = null;
    }
  }

  async getWaitlist(): Promise<WaitlistParty[]> {
    try {
      const response = await apiClient.get<WaitlistParty[]>("/waitlist");
      const sortedData = response.data.sort(
        (a, b) =>
          new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      );
      return sortedData;
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

  async removeFromWaitlist(id: string): Promise<WaitlistParty> {
    try {
      const response = await apiClient.delete<WaitlistParty>(`/waitlist/${id}`);
      return response.data;
    } catch (error) {
      console.error("Failed to remove party from waitlist:", error);
      throw new Error("Could not remove from waitlist");
    }
  }
}

export const waitlistService = new WaitlistService();
