import { useState } from "react";
import Button from "./Common/Button";
import { useRecoilValue } from "recoil";
import { userIdState } from "../recoil/store";
import { waitlistService } from "../services/waitlistService";

const CheckIn = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const userId = useRecoilValue(userIdState);

  const handleCheckIn = async () => {
    setIsLoading(true);
    setError(null);

    try {
      await waitlistService.checkInParty(userId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to check in");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-3xl font-bold">You're ready to be seated!</h2>
      {error && (
        <div className="text-red-500 bg-red-100 p-2 rounded">{error}</div>
      )}
      <Button
        onClick={handleCheckIn}
        label={isLoading ? "Checking in..." : "Check in!"}
        disabled={isLoading}
      />
    </div>
  );
};

export default CheckIn;
