import { render, screen, fireEvent } from "@testing-library/react";
import { RecoilRoot } from "recoil";
import { userIdState } from "../recoil/store";
import WaitlistForm from "../components/WaitlistForm";
import { API_BASE_URL } from "../config/config";
import { vi, describe, it, expect, Mock, beforeEach, afterEach } from "vitest";

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn());
});

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("WaitlistForm Component", () => {
  const mockUserId = "mock-user-id";
  const renderWithRecoil = (ui: React.ReactElement) => {
    return render(
      <RecoilRoot
        initializeState={(snap) => {
          snap.set(userIdState, mockUserId);
        }}
      >
        {ui}
      </RecoilRoot>
    );
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders form with default values", () => {
    renderWithRecoil(<WaitlistForm />);

    expect(screen.getByText("Join our Waitlist!")).toBeInTheDocument();
    expect(screen.getByLabelText("Name")).toHaveValue("");
    expect(screen.getByLabelText("Party Size")).toHaveValue(2);
    expect(screen.getByText("Submit")).toBeInTheDocument();
  });

  it("allows the user to input name and party size", async () => {
    renderWithRecoil(<WaitlistForm />);

    const nameInput = screen.getByLabelText("Name");
    const partySizeInput = screen.getByLabelText("Party Size");

    fireEvent.change(nameInput, {target: {value: "Tokugawa"}})
    fireEvent.change(partySizeInput, { target: { valueAsNumber: 4 } });

    expect(nameInput).toHaveValue("Tokugawa");
    expect(partySizeInput).toHaveValue(4);
  });

  it("submits the form and calls the API with correct data", async () => {
    const mockFetch = fetch as Mock;
    mockFetch.mockResolvedValueOnce({
      json: async () => ({ success: true, message: "Added to waitlist" }),
    } as Response);

    renderWithRecoil(<WaitlistForm />);

    const nameInput = screen.getByLabelText("Name");
    const partySizeInput = screen.getByLabelText("Party Size");
    const submitButton = screen.getByText("Submit");

    fireEvent.change(nameInput, {target: {value: "Tokugawa"}})
    fireEvent.change(partySizeInput, { target: { valueAsNumber: 5 } });
    fireEvent.click(submitButton);

    expect(mockFetch).toHaveBeenCalledWith(`${API_BASE_URL}/waitlist`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: "Tokugawa",
        party_size: 5,
        user_id: mockUserId,
      }),
    });
  });
});
