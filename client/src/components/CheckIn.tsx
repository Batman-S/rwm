import Button from "./Common/Button";
import { useRecoilValue } from "recoil";
import { userIdState } from "../recoil/store";
import { waitlistService } from "../services/waitlistService";
const CheckIn = () => {
  const userId = useRecoilValue(userIdState);
  const handleCheckIn = async () => {
    try {
      await waitlistService.checkInParty(userId);
    } catch (error) {
      console.error("Failed to check in party:", error);
    }
  };
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-3xl font-bold">You're ready to be seated!</h2>
      <Button onClick={handleCheckIn} label="Check in!" />
    </div>
  );
};

export default CheckIn;
