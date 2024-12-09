import WaitlistForm from "./WaitlistForm";
import { useEffect, useState } from "react";
import { WaitlistParty, waitlistService } from "../services/waitlistService";
const Home = () => {
  const [waitlist, setWaitlist] = useState<WaitlistParty[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleDataReceived = (data: WaitlistParty[]) => {
      console.log("data", data);
      setWaitlist(data);
      setError(null);
    };

    const handleError = (error: Error) => {
      setError(error.message);
    };

    waitlistService.startPolling(10000, handleDataReceived, handleError);

    return () => {
      waitlistService.stopPolling();
    };
  }, []);
  return (
    <div className="container mx-auto p-12 flex items-center justify-center ">
      <WaitlistForm />
    </div>
  );
};

export default Home;
