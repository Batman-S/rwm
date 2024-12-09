interface FormSubmitProps {
  label: string;
}

const FormSubmit = ({ label }: FormSubmitProps) => {
  return <button type="submit">{label}</button>;
};

export default FormSubmit;
