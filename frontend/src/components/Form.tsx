import { CatFactContext } from "../store/cat-facts-context.tsx";
import { useActionState, use } from "react";

import Submit from "./Submit.tsx";

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
    // Extract the fact from the form data
    const fact = formData.get("fact") as string;

    // Initialize an array to hold any errors
    let errors: string[] = [];

    // Validate the fact input
    if (!fact || fact.trim().length < 5) {
      errors.push("Fact must be at least 5 characters long.");
    }

    // If there are errors, return them along with the entered values
    const response = await addFact(fact);

    // If the response contains errors, add them to the errors array
    if (response.errors) {
      errors = [...errors, ...response.errors];
    }

    // If there are errors, return them
    if (errors.length > 0) {
      return {
        errors,
        enteredValues: { fact: fact ?? "" },
      };
    }

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
      <img className="cat-image" src="/cat.png" alt="Cat" />
    </form>
  );
}
