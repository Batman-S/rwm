import Button from "./Common/Button";
import { useRecoilValue } from "recoil";
import { userIdState } from "../recoil/atoms";
import { waitlistService } from "../services/waitlistService";
import { useNavigate } from "react-router-dom";
const CheckIn = () => {
  const userId = useRecoilValue(userIdState);
  const navigate = useNavigate()
  const handleCheckIn = async () => {
    try {
      await waitlistService.checkInParty(userId);
      navigate('/completed')
    } catch (error) {
      console.error("Failed to check in party:", error);
      throw new Error("Could not check in party");
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
