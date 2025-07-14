import { defineConfig, loadEnv } from "vite";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";

import react from "@vitejs/plugin-react";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, resolve(__dirname, ".."), "");

  return {
    plugins: [react()],
    root: "./",
    define: {
      "process.env.HOST": JSON.stringify(env.HOST),
      "process.env.BACKEND_PORT": JSON.stringify(env.BACKEND_PORT),
    },
    server: {
      host: "0.0.0.0",
      port: parseInt(env.FRONTEND_PORT),
    },
  };
});
