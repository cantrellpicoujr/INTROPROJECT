import { CatFactContext } from "../store/cat-facts-context.tsx";
import CatFact from "./CatFact.tsx";
import { use } from "react";

// Define the CatFact type
export type CatFactType = {
  id: number;
  fact: string;
  created_at: string;
};

export default function CatFacts() {
  // Use the CatFactContext to access the facts
  const { facts } = use(CatFactContext) as { facts: CatFactType[] };

  // Sort the facts by id in ascending order
  const sortedFacts = [...facts].sort((a, b) => a.id - b.id);

  return (
    <div className="cat-facts-section">
      <h2>Cat Facts</h2>

      {sortedFacts && sortedFacts.length > 0 ? (
        <ul>
          {sortedFacts.map((fact) => (
            <li key={fact.id}>
              <CatFact fact={fact.fact} />
            </li>
          ))}
        </ul>
      ) : (
        <p>No cat facts available yet.</p>
      )}
    </div>
  );
}
