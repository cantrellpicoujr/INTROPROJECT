import { createContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

// Construct the base URL from environment variables.
const BASE_URL = `http://${import.meta.env.HOST}:${
  import.meta.env.BACKEND_PORT
}`;

// Define the structure of a single cat fact returned by the backend.
export type CatFactType = {
  id: number;
  fact: string;
  created_at: string;
};

// Define the shape of the context value that will be shared with components.
type CatFactContextType = {
  facts: CatFactType[] | null;

  // Function to add a new fact (returns errors or success details).
  addFact: (
    enteredFactData: string
  ) => Promise<{ errors: string[] | null; enteredValues: any }>;

  // Function to get a single random fact from the backend.
  getRandomFact: () => Promise<{ fact?: string; error?: string }>;
};

// Create a new React context with default placeholder values.
export const CatFactContext = createContext<CatFactContextType>({
  facts: [],
  addFact: async () => ({ errors: null, enteredValues: {} }),
  getRandomFact: async () => ({ fact: "" }),
});

// Define the props expected by the provider component (children elements).
type CatFactsContextProviderProps = {
  children: ReactNode;
};

// This component provides the context to any components that need cat facts.
export function CatFactsContextProvider({
  children,
}: CatFactsContextProviderProps) {
  // State to store the list of cat facts, initially empty.
  const [facts, setFacts] = useState<CatFactType[] | null>([]);

  // Fetch all cat facts from the backend when this component first mounts.
  useEffect(() => {
    async function loadFacts() {
      try {
        // Make a GET request to the backend to retrieve all cat facts.
        const response = await fetch(`${BASE_URL}/catfacts`);

        // Convert JSON to JS object
        const factsList = await response.json();

        // Update the state with the list of facts.
        setFacts(factsList);
      } catch (error) {
        console.error("Failed to load facts:", error);
      }
    }

    // Call the async function.
    loadFacts();
  }, []);

  // Function to add a new cat fact to the backend.
  async function addFact(
    enteredFactData: string
  ): Promise<{ errors: string[] | null; enteredValues: any }> {
    const errors: string[] = [];

    // Format the new fact as URL-encoded form data.
    const formData = new URLSearchParams();
    formData.append("fact", enteredFactData);

    try {
      // Send POST request to add the fact.
      const response = await fetch(`${BASE_URL}/catfacts`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!response.ok) {
        // Backend returned an error — parse it and add to our local error list.
        const data = await response.json();
        errors.push(data.detail || "Failed to add fact.");
        return { errors, enteredValues: enteredFactData };
      }

      // Success! Parse the response to get the saved fact.
      const savedFact = await response.json();

      // Add the new fact to the beginning of the state array.
      setFacts((prevFacts) =>
        prevFacts ? [savedFact, ...prevFacts] : [savedFact]
      );

      // Return success result.
      return { errors: null, enteredValues: {} };
    } catch (error) {
      console.error("Error submitting new fact:", error);

      // Network or unexpected failure.
      return {
        errors: ["Something went wrong while submitting."],
        enteredValues: enteredFactData,
      };
    }
  }

  // Function to fetch a single random cat fact.
  async function getRandomFact(): Promise<{ fact?: string; error?: string }> {
    try {
      const response = await fetch(`${BASE_URL}/catfacts/random`);

      // If the backend couldn't return a random fact.
      if (!response.ok) {
        throw new Error("Failed to fetch random fact.");
      }

      const data = await response.json();
      return { fact: data.fact };
    } catch (error) {
      console.error("Error fetching random fact:", error);
      return { error: "Could not fetch random fact." };
    }
  }

  // Combine the data and functions into one object to provide to components.
  const contextValue: CatFactContextType = {
    facts,
    addFact,
    getRandomFact,
  };

  // Provide the context value to all children wrapped in this component.
  return (
    <CatFactContext.Provider value={contextValue}>
      {children}
    </CatFactContext.Provider>
  );
}
