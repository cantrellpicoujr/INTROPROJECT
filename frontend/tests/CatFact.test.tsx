import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { test, expect } from "@jest/globals";

import CatFact from "../src/components/CatFact.tsx";

test("Renders CatFact component with given text.", () => {
  render(<CatFact fact="Cat Facts" />);
  expect(screen.getByText("Cat Facts")).toBeInTheDocument();
});
