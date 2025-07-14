import Submit from "../src/components/Submit";
import { render, screen } from "@testing-library/react";

let pendingValue = false;

// Mock useFormStatus to control the pending state
jest.mock("react-dom", () => ({
  ...jest.requireActual("react-dom"),
  useFormStatus: () => ({ pending: pendingValue }),
}));

afterEach(() => {
  pendingValue = false; // Reset mocked modules
  jest.clearAllMocks(); // Reset mock function call history
});

describe("Submit component", () => {
  it("Renders Submit button with correct text when not pending.", () => {
    pendingValue = false;
    render(<Submit />);
    const button = screen.getByRole("button", { name: /Submit/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent("Submit");
    expect(button).not.toBeDisabled();
  });

  it("Renders Submit button as disabled and shows 'Submitting...' when pending.", () => {
    // Remock useFormStatus to return pending: true
    pendingValue = true;
    render(<Submit />);
    const button = screen.getByRole("button", { name: /Submitting.../i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent("Submitting...");
    expect(button).toBeDisabled();
  });
});
