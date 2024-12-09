import React, { useState } from "react";
import FormInput from "./Common/FormInput";
import FormSubmit from "./Common/FormSubmit";

const WaitlistForm = () => {
  const [name, setName] = useState<string>("");
  const [partySize, setPartySize] = useState<number>(2);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formData = { name, party_size: partySize };
    try {
      const response = await fetch("http://localhost:8000/api/v1/waitlist", {
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
