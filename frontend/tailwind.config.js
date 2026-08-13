/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter Variable", "Inter", "system-ui", "sans-serif"],
      },
      colors: {
        brand: {
          50: "#eef4ff",
          100: "#dbe6fe",
          500: "#3b6fee",
          600: "#2f5bd6",
          700: "#2748ac",
        },
      },
      keyframes: {
        "field-flash": {
          "0%": { backgroundColor: "rgba(59,111,238,0.18)" },
          "100%": { backgroundColor: "transparent" },
        },
      },
      animation: {
        "field-flash": "field-flash 1.2s ease-out",
      },
    },
  },
  plugins: [],
};
