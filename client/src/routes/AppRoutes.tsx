import { Routes, Route } from "react-router-dom";
import StatusRouter from "./StatusRouter";
import Waitlist from "../components/Waitlist";
import WaitlistForm from "../components/WaitlistForm";
import CheckIn from "../components/CheckIn";
import Completed from "../components/Completed";
import { useRecoilValueLoadable, useSetRecoilState } from "recoil";
import { partyStatusSelector, partyStatus } from "../recoil/store";
import { useEffect } from "react";

const AppRoutes = () => {
  const setPartyStatus = useSetRecoilState(partyStatus);
  const status = useRecoilValueLoadable(partyStatusSelector);

  useEffect(() => {
    if (status.contents) {
      setPartyStatus(status.contents.status);
    }
  }, [setPartyStatus, status]);

  if (status.state === "loading") return <div>Loading...</div>;
  return (
    <Routes>
      <Route element={<StatusRouter />}>
        <Route path="/" element={<WaitlistForm />} />
        <Route path="/waitlist" element={<Waitlist />} />
        <Route path="/check-in" element={<CheckIn />} />
        <Route path="/completed" element={<Completed />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
