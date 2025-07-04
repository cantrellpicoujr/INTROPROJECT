import "./App.css";
import Form from "./components/Form";
import { CatFacts } from "./components/CatFacts";
import { CatFactsContextProvider } from "./store/cat-facts-context.jsx";

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
