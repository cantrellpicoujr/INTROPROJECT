import { useActionState, use } from "react";
import { CatFactContext } from "../store/cat-facts-context";
import Submit from "./Submit";

type FormState = {
  errors: string[] | null;
  enteredValues: {
    fact?: string;
  };
};

export default function CatFactForm() {
  const { addFact } = use(CatFactContext);

  async function submitCatFact(
    _prevState: FormState,
    formData: FormData
  ): Promise<FormState> {
    const fact = formData.get("fact") as string;

    let errors: string[] = [];

    if (!fact || fact.trim().length < 5) {
      errors.push("Fact must be at least 5 characters long.");
    }

    if (errors.length > 0) {
      return {
        errors,
        enteredValues: { fact: fact ?? "" },
      };
    }
    await addFact(fact);
    return { errors: null, enteredValues: {} };
  }

  const [formState, formAction] = useActionState<FormState, FormData>(
    submitCatFact,
    {
      errors: null,
      enteredValues: {},
    }
  );

  return (
    <form action={formAction}>
      <p>
        <label htmlFor="fact">New Cat Fact</label>
        <input
          type="text"
          id="fact"
          name="fact"
          defaultValue={formState.enteredValues?.fact}
        />
      </p>

      {formState.errors && (
        <ul style={{ color: "red" }}>
          {formState.errors.map((error) => (
            <li key={error}>{error}</li>
          ))}
        </ul>
      )}

      <Submit />
    </form>
  );
}
