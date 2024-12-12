import tableCheckLogo from "../../ui/assets/tablecheck.svg";
import iconLogo from "../../ui/assets/iconlogo.svg";
import { useRecoilValue } from "recoil";
import { partyStatus } from "../../recoil/store";

type StatusKey = string;
const Header = () => {
  const status = useRecoilValue(partyStatus);
  const labelMap: { [key in StatusKey]: string } = {
    waiting: "Waiting",
    ready: "Ready",
    checked_in: "Checked In",
    completed: "Completed",
  };
  return (
    <header className="flex items-center w-full h-16 px-24 border-b-2 shadow-md justify-between">
      <div className="flex gap-2 items-center">
        <img height="100%" src={iconLogo} />
        <img height="100%" src={tableCheckLogo} />
      </div>
      {status && status !== "na" && (
        <div className="flex gap-2 items-center">
          <div className="font-semibold text-sm">Current Status:</div>
          <div className="font-bold text-purple-primary text-xl">
            {labelMap[status]}
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
