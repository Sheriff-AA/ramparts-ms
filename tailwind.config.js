/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/preline//**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: ['preline/plugin'],
}

