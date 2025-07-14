import { render, screen, fireEvent } from "@testing-library/react";
import { CatFactContext } from "../src/store/cat-facts-context";
import Form from "../src/components/Form.tsx";
import type { CatFactType } from "../src/components/CatFacts.tsx";
// Mock Submit button
jest.mock("../src/components/Submit.tsx", () => () => (
  <button type="submit">Submit</button>
));

describe("CatFactForm component", () => {
  it("renders input, label, submit button, and cat image", () => {
    const facts: CatFactType[] = [
      { id: 1, fact: "Cats purr to communicate.", created_at: "2024-07-13" },
      { id: 2, fact: "Cats sleep a lot.", created_at: "2024-07-13" },
    ];

    const ctxValue = {
      facts,
      addFact: jest.fn().mockResolvedValue({ errors: null }),
      getRandomFact: jest.fn(),
    };

    render(
      <CatFactContext.Provider value={ctxValue}>
        <Form />
      </CatFactContext.Provider>
    );

    expect(screen.getByLabelText("New Cat Fact")).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: /new cat fact/i })
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /submit/i })).toBeInTheDocument();
    expect(screen.getByAltText("Cat")).toBeInTheDocument();
  });

  it("shows error if fact is too short", async () => {
    const facts: CatFactType[] = [
      { id: 1, fact: "Cats purr to communicate.", created_at: "2024-07-13" },
      { id: 2, fact: "Cats sleep a lot.", created_at: "2024-07-13" },
    ];

    const ctxValue = {
      facts,
      addFact: jest.fn().mockResolvedValue({ errors: null }),
      getRandomFact: jest.fn(),
    };

    render(
      <CatFactContext.Provider value={ctxValue}>
        <Form />
      </CatFactContext.Provider>
    );

    fireEvent.change(screen.getByLabelText("New Cat Fact"), {
      target: { value: "cat" },
    });
    fireEvent.click(screen.getByRole("button", { name: /submit/i }));

    expect(
      await screen.findByText("Fact must be at least 5 characters long.")
    ).toBeInTheDocument();
  });

  it("shows errors returned from addFact", async () => {
    const facts: CatFactType[] = [
      { id: 1, fact: "Cats purr to communicate.", created_at: "2024-07-13" },
      { id: 2, fact: "Cats sleep a lot.", created_at: "2024-07-13" },
    ];

    const ctxValue = {
      facts,
      addFact: jest.fn().mockResolvedValue({ errors: ["Duplicate fact."] }),
      getRandomFact: jest.fn(),
    };

    render(
      <CatFactContext.Provider value={ctxValue}>
        <Form />
      </CatFactContext.Provider>
    );

    fireEvent.change(screen.getByLabelText("New Cat Fact"), {
      target: { value: "Cats are cool." },
    });
    fireEvent.click(screen.getByRole("button", { name: /submit/i }));

    expect(await screen.findByText("Duplicate fact.")).toBeInTheDocument();
  });
});
