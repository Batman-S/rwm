import { apiClient } from "../components/api/apiClient";
import { waitlistService } from "../services/waitlistService";
import { vi, describe, it, expect, Mock, afterEach } from "vitest";

vi.mock("../config/config.ts", () => ({
  apiBaseUrl: "http://localhost:8000/api/v1",
  wsBaseUrl: "ws://localhost:8000",
}));

vi.mock("../components/api/apiClient", () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe("WaitlistService", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("should fetch the list of waitlist parties", async () => {
    const mockResponse = [
      {
        _id: "1",
        userId: "user_1",
        name: "Test Party 1",
        partySize: 4,
        status: "waiting",
        timestamp: "2024-12-13T00:00:00",
      },
      {
        _id: "2",
        userId: "user_2",
        name: "Test Party 2",
        partySize: 2,
        status: "waiting",
        timestamp: "2024-12-13T01:00:00",
      },
    ];

    (apiClient.get as Mock).mockResolvedValueOnce({ data: mockResponse });

    const result = await waitlistService.getWaitlist();

    expect(result).toEqual(mockResponse);
    expect(apiClient.get).toHaveBeenCalledWith("/waitlist");
    expect(apiClient.get).toHaveBeenCalledTimes(1);
  });

  it("should add a party to the waitlist", async () => {
    const payload = { name: "Test Party 3", party_size: 3, user_id: "user_3" };
    const mockResponse = {
      _id: "3",
      user_id: "user_3",
      name: "Test Party 3",
      party_size: 3,
      status: "waiting",
      timestamp: "2024-12-13T02:00:00",
    };

    (apiClient.post as Mock).mockResolvedValueOnce({ data: mockResponse });

    const result = await waitlistService.addToWaitlist(
      payload.name,
      payload.party_size,
      payload.user_id
    );

    expect(result).toEqual(mockResponse);
    expect(apiClient.post).toHaveBeenCalledWith("/waitlist", payload);
    expect(apiClient.post).toHaveBeenCalledTimes(1);
  });

  it("should check in a party", async () => {
    const userId = "user_1";

    (apiClient.post as jest.Mock).mockResolvedValueOnce({});
    await waitlistService.checkInParty(userId);

    expect(apiClient.post).toHaveBeenCalledWith(`/waitlist/${userId}/check-in`);
    expect(apiClient.post).toHaveBeenCalledTimes(1);
  });

  it("should get the status of a party", async () => {
    const userId = "user_1";
    const mockStatusResponse = {
      party: {
        _id: "user_1",
        name: "Test Party 1",
        partySize: 4,
        status: "waiting",
      },
    };

    (apiClient.get as jest.Mock).mockResolvedValueOnce({
      data: mockStatusResponse,
    });

    const result = await waitlistService.getStatus(userId);

    expect(result).toEqual(mockStatusResponse);
    expect(apiClient.get).toHaveBeenCalledWith(`/waitlist/${userId}/status`);
    expect(apiClient.get).toHaveBeenCalledTimes(1);
  });
});
