import tableCheckLogo from "../../ui/assets/tablecheck.svg";
import iconLogo from "../../ui/assets/iconlogo.svg";
const Header = () => {
  return (
    <header className="flex items-center w-full h-16 px-24 border-b-2 shadow-md">
      <div className="flex gap-2 items-center">
        <img height="100%" src={iconLogo} />
        <img height="100%" src={tableCheckLogo} />
      </div>
    </header>
  );
};

export default Header;
