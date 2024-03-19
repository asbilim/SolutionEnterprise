/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./shop/templates/shop/**/*.html",
    "./shop/templates/blog/**/*.html",
    "./node_modules/flowbite/**/*.js",
    "./shop/templates/shop/components/**/*.html",
    "./shop/templates/blog/components/**/*.html",
  ],
  theme: {
    extend: {},
  },

  plugins: [require("flowbite/plugin"),require('@tailwindcss/typography')],
};
