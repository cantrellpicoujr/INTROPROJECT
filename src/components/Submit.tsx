import { useFormStatus } from "react-dom";

export default function Submit() {
  const { pending } = useFormStatus();

  return (
    <p>
      <button type="submit" disabled={pending}>
        {pending ? "Submitting..." : "Submit"}
      </button>
    </p>
  );
}
