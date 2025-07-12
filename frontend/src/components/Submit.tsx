import { useFormStatus } from "react-dom";

export default function Submit() {
  // Use the useFormStatus hook to get the pending state
  const { pending } = useFormStatus();

  return (
    <p>
      <button type="submit" disabled={pending}>
        {pending ? "Submitting..." : "Submit"}
      </button>
    </p>
  );
}
