import { render, screen, fireEvent } from "@testing-library/react";
import { RecoilRoot } from "recoil";
import { userIdState } from "../recoil/store";
import { waitlistService } from "../services/waitlistService";
import CheckIn from "../components/CheckIn";
import { vi, describe, it, expect } from "vitest";
vi.mock("../services/waitlistService", () => ({
  waitlistService: {
    checkInParty: vi.fn(),
  },
}));

describe("CheckIn Component", () => {
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

  it("renders the component with correct text and button", () => {
    renderWithRecoil(<CheckIn />);

    expect(screen.getByText("You're ready to be seated!")).toBeInTheDocument();
    expect(screen.getByText("Check in!")).toBeInTheDocument();
  });

  it("calls checkInParty with correct userId when button is clicked", async () => {
    const mockCheckInParty = vi.fn();
    waitlistService.checkInParty = mockCheckInParty;
    renderWithRecoil(<CheckIn />);
    const button = screen.getByText("Check in!");
    fireEvent.click(button);

    expect(mockCheckInParty).toHaveBeenCalledWith(mockUserId);
  });
});
