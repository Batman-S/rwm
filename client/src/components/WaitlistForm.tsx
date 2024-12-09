import React, { useState } from "react";
import FormInput from "./Common/FormInput";
import FormSubmit from "./Common/FormSubmit";
interface WaitlistFormProps {
  onSubmit: (party: { name: string; partySize: number }) => void;
}

const WaitlistForm = ({ onSubmit }: WaitlistFormProps) => {
  const [name, setName] = useState<string>("");
  const [partySize, setPartySize] = useState<number>(2);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!name) {
      // handle alert
    }

    onSubmit({ name, partySize });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Join our Waitlist!</h2>
      <div className="flex gap-2">
        <FormInput
          id="name"
          type="text"
          label="Name"
          required
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <FormInput
          id="partySize"
          type="number"
          label="Party Size"
          required
          value={partySize}
          onChange={(e) => setPartySize(e.target.valueAsNumber)}
        />
      </div>
      <div>
        <FormSubmit label="Submit" />
      </div>
    </form>
  );
};

export default WaitlistForm;
