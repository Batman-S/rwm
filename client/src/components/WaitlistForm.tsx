import { useState } from "react";
import FormInput from "./Common/FormInput";
import Button from "./Common/Button";
import { useRecoilValue } from "recoil";
import { userIdState } from "../recoil/store";
import { waitlistService } from "../services/waitlistService";
const WaitlistForm = () => {
  const [name, setName] = useState<string>("");
  const [partySize, setPartySize] = useState<number>(2);
  const userId = useRecoilValue(userIdState);

  const handleSubmit = async () => {
    await waitlistService.addToWaitlist(name, partySize, userId);
  };

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-3xl font-bold">Join our Waitlist!</h2>
      <form onSubmit={handleSubmit}>
        <div className="flex flex-col gap-2">
          <FormInput
            id="name"
            type="text"
            label="Name"
            className="w-64"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <div className="flex gap-4 items-end justify-between">
            <FormInput
              id="partySize"
              type="number"
              label="Party Size"
              className="w-20"
              required
              value={partySize}
              min={1}
              max={10}
              onChange={(e) => setPartySize(e.target.valueAsNumber)}
            />
            <div className="pt-4">
              <Button label="Submit" />
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};

export default WaitlistForm;
