import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import * as path from "path";


export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // allow "@/foo" → "web_ui/src/foo"
      "@": path.resolve(__dirname, "src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://54.93.100.203:8080",
        changeOrigin: true,
      },
    },
  },
});
