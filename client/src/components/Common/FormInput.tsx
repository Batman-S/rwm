interface FormInputProps {
  type: string;
  id: string;
  label: string;
  value: string | number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  required: boolean;
}

const FormInput = ({
  type,
  value,
  onChange,
  required,
  label,
  id,
}: FormInputProps) => {
  return (
    <div className="flex flex-col gap-2">
      {label && <label htmlFor={id}>{label}</label>}
      <input
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        required={required}
      />
    </div>
  );
};

export default FormInput;
