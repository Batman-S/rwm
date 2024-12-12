/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "purple-primary": "#5C11A6",
        "purple-secondary": "#7935D2",
      },
    },
  },
  plugins: [],
};
