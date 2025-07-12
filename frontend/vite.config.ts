import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, resolve(__dirname, ".."), "");

  return {
    plugins: [react()],
    root: "./",
    define: {
      "import.meta.env.HOST": JSON.stringify(env.HOST),
      "import.meta.env.BACKEND_PORT": JSON.stringify(env.BACKEND_PORT),
    },
  };
});
