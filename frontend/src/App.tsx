import CatFacts from "./components/CatFacts.tsx";
import Form from "./components/Form.tsx";

import { CatFactsContextProvider } from "./store/cat-facts-context.tsx";

import "./App.css";

function App() {
  return (
    <main>
      <CatFactsContextProvider>
        <Form />
        <CatFacts />
      </CatFactsContextProvider>
    </main>
  );
}

export default App;
