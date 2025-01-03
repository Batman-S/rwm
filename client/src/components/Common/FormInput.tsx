import classNames from "classnames";

interface FormInputProps {
  type: string;
  id: string;
  label: string;
  value: string | number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  required: boolean;
  className?: string;
  min?: number;
  max?: number;
}

const FormInput = ({
  type,
  value,
  onChange,
  required,
  label,
  id,
  className,
  min,
  max,
}: FormInputProps) => {
  return (
    <div className="flex flex-col gap-2">
      {label && <label htmlFor={id}>{label}</label>}
      <input
        className={classNames(
          "border border-purple-primary h-8 w-48 px-4 py-4 rounded-sm",
          className
        )}
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        min={min}
        max={max}
      />
    </div>
  );
};

export default FormInput;
