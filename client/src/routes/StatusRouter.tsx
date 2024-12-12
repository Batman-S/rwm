import { Outlet, useNavigate } from "react-router-dom";
import { partyStatus } from "../recoil/store";
import { useRecoilValue } from "recoil";
import { useEffect } from "react";

const StatusRouter = () => {
  const status = useRecoilValue(partyStatus);
  const navigate = useNavigate();
  const getRouteForStatus = (status: string | null) => {
    switch (status) {
      case "na":
        return "/";
      case "waiting":
        return "/waitlist";
      case "ready":
        return "/check-in";
      case "completed":
      case "checked_in":
        return "/completed";
      default:
        return "/";
    }
  };

  useEffect(() => {
    const route = getRouteForStatus(status);
    console.log("status", status);
    console.log("route", route);
    if (route !== window.location.pathname) {
      navigate(route);
      return;
    }
  }, [status]);

  return <Outlet />;
};

export default StatusRouter;
