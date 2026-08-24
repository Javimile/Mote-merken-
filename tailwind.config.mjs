/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,ts,jsx,tsx,vue,svelte}'],
  theme: {
    extend: {
      colors: {
        ink: '#070b0d', panel: '#0d1215', line: '#232a2e', sand: '#b98a48',
        'sand-light': '#d7b77d', ivory: '#f3eee5', mist: '#a9adb0', chile: '#d52b1e'
      },
      fontFamily: { serif: ['Georgia','Times New Roman','serif'], sans: ['Inter','Arial','sans-serif'] },
      boxShadow: { glow: '0 18px 60px rgba(0,0,0,.35)' }
    }
  }, plugins: []
};
