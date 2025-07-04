import { use } from "react";
import { CatFactContext } from "../store/cat-facts-context";
import { CatFact as CatFactComponent } from "./CatFact";

// Define the CatFact type
export type CatFactType = {
  id: number;
  fact: string;
  created_at: string;
};

export function CatFacts() {
  const { facts } = use(CatFactContext) as { facts: CatFactType[] };
  const sortedFacts = [...facts].sort((a, b) => a.id - b.id);

  return (
    <div className="cat-facts-section">
      <h2>Cat Facts</h2>

      {sortedFacts && sortedFacts.length > 0 ? (
        <ul>
          {sortedFacts.map((fact) => (
            <li key={fact.id}>
              <CatFactComponent fact={fact.fact} />
            </li>
          ))}
        </ul>
      ) : (
        <p>No cat facts available yet.</p>
      )}
    </div>
  );
}
