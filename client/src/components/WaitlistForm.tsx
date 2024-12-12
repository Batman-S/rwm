import React, { useState } from "react";
import FormInput from "./Common/FormInput";
import Button from "./Common/Button";
import { API_BASE_URL } from "../config/config";
import { useRecoilValue } from "recoil";
import { userIdState } from "../recoil/atoms";
import { useWebSocket } from "../contexts/WebSocketContext";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const WaitlistForm = () => {
  const [name, setName] = useState<string>("");
  const [partySize, setPartySize] = useState<number>(2);
  const userId = useRecoilValue(userIdState);
  const navigate = useNavigate();
  const { globalUpdates } = useWebSocket();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formData = { name, party_size: partySize, user_id: userId };
    try {
      const response = await fetch(`${API_BASE_URL}/waitlist`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      const newEntry = await response.json();
      console.log("newEntry", newEntry);
    } catch (err) {
      console.error("Error submitting form:", err);
    }
  };

  useEffect(() => {
    console.log("globalUpdates", globalUpdates);
    if (!globalUpdates) return;
    if (globalUpdates?.status === "ready") {
      navigate("/check-in");
    }
  }, [globalUpdates]);

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
