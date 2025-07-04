import { createContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

// Type for a single cat fact
export type CatFactType = {
  id: number;
  fact: string;
  created_at: string;
};

// Type for context value
type CatFactContextType = {
  facts: CatFactType[] | null;
  addFact: (
    enteredFactData: string
  ) => Promise<{ errors: string[] | null; enteredValues: any }>;
  getRandomFact: () => Promise<{ fact?: string; error?: string }>;
};

// Create context with default values
export const CatFactContext = createContext<CatFactContextType>({
  facts: [],
  addFact: async () => ({ errors: null, enteredValues: {} }),
  getRandomFact: async () => ({ fact: "" }),
});

type CatFactsContextProviderProps = {
  children: ReactNode;
};

export function CatFactsContextProvider({
  children,
}: CatFactsContextProviderProps) {
  const [facts, setFacts] = useState<CatFactType[] | null>([]);

  useEffect(() => {
    async function loadFacts() {
      const response = await fetch("http://127.0.0.1:8000/catfacts");
      const factsList = await response.json();
      console.log(factsList);
      setFacts(factsList);
    }

    loadFacts();
  }, []);

  async function addFact(
    enteredFactData: string
  ): Promise<{ errors: string[] | null; enteredValues: any }> {
    const errors: string[] = [];

    const formData = new URLSearchParams();
    formData.append("fact", enteredFactData);

    try {
      const response = await fetch("http://127.0.0.1:8000/catfacts", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!response.ok) {
        const data = await response.json();
        errors.push(data.detail || "Failed to add fact.");
        return { errors, enteredValues: enteredFactData };
      }

      const savedFact = await response.json();
      setFacts((prevFacts) =>
        prevFacts ? [savedFact, ...prevFacts] : [savedFact]
      );
      return { errors: null, enteredValues: {} };
    } catch (error) {
      return {
        errors: ["Something went wrong while submitting."],
        enteredValues: enteredFactData,
      };
    }
  }

  async function getRandomFact(): Promise<{ fact?: string; error?: string }> {
    try {
      const response = await fetch("http://127.0.0.1:8000/catfacts/random");

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

  const contextValue: CatFactContextType = {
    facts,
    addFact,
    getRandomFact,
  };

  return (
    <CatFactContext.Provider value={contextValue}>
      {children}
    </CatFactContext.Provider>
  );
}
