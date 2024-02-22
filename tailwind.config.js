/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./shop/templates/shop/**/*.html",
    "./node_modules/flowbite/**/*.js",
    "./shop/templates/shop/components/**/*.html",
  ],
  theme: {
    extend: {},
  },

  plugins: [require("flowbite/plugin")],
};
