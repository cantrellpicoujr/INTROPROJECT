import { render, screen } from "@testing-library/react";
import { CatFactContext } from "../src/store/cat-facts-context.tsx";
import CatFacts from "../src/components/CatFacts.tsx";
import type { CatFactType } from "../src/components/CatFacts.tsx";

// Mock CatFacts component
jest.mock("../src/components/CatFact.tsx", () => (props: { fact: string }) => (
  <div data-testid="cat-fact">{props.fact}</div>
));

describe("CatFacts component", () => {
  it("Renders a list of cat facts.", () => {
    const facts: CatFactType[] = [
      { id: 1, fact: "Cats purr to communicate.", created_at: "2024-07-13" },
      { id: 2, fact: "Cats sleep a lot.", created_at: "2024-07-13" },
    ];

    const ctxValue = {
      facts,
      addFact: jest.fn(),
      getRandomFact: jest.fn(),
    };

    render(
      <CatFactContext.Provider value={ctxValue}>
        <CatFacts />
      </CatFactContext.Provider>
    );

    expect(screen.getByText("Cat Facts")).toBeInTheDocument();
    expect(screen.getAllByTestId("cat-fact")).toHaveLength(2);
    expect(screen.getByText("Cats purr to communicate.")).toBeInTheDocument();
    expect(screen.getByText("Cats sleep a lot.")).toBeInTheDocument();
  });

  it("Renders message when no facts are available.", () => {
    const ctxValue = {
      facts: [],
      addFact: jest.fn(),
      getRandomFact: jest.fn(),
    };

    render(
      <CatFactContext.Provider value={ctxValue}>
        <CatFacts />
      </CatFactContext.Provider>
    );

    expect(screen.getByText("No cat facts available yet.")).toBeInTheDocument();
  });
});
