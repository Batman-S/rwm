import { useRecoilValueLoadable } from "recoil";
import { partyStatusSelector } from "../recoil/store";

const Waitlist = () => {
  const statusLoadable = useRecoilValueLoadable(partyStatusSelector);

  if (statusLoadable.state === "loading") {
    return <div>Loading...</div>;
  }

  const status = statusLoadable.contents;

  return (
    <div className="flex flex-col gap-6 items-center text-center">
      <h2 className="text-3xl font-bold">Thank you for your patience!</h2>
      <div className="text-lg">
        <p>
          You will be notified to check in as soon as a seat becomes available.
        </p>
        {status?.party && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <p className="font-semibold">Your Party Details:</p>
            <p>Name: {status.party.name}</p>
            <p>Party Size: {status.party.party_size} people</p>
            <p>Status: {status.status}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Waitlist;
