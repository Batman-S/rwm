import classNames from "classnames";
interface ButtonProps {
  label: string;
  className?: string;
  onClick?: () => void;
  disabled: boolean;
}

const Button = ({ label, onClick, className, disabled }: ButtonProps) => {
  return (
    <button
      disabled={disabled}
      onClick={onClick}
      className={classNames(
        "bg-purple-primary text-white font-semibold px-2 py-2 text-xl rounded-sm hover:bg-purple-secondary",
        className
      )}
      type="submit"
    >
      {label}
    </button>
  );
};

export default Button;
