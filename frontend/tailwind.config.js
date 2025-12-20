/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx,md,mdx}',
    './docs/**/*.{md,mdx}',
    './pages/**/*.{js,jsx,ts,tsx,md,mdx}',
    './*.{js,jsx,ts,tsx,md,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'cyber-black': '#000000',
        'cyber-neon-green': '#39FF14',
        'cyber-neon-blue': '#00FFFF',
        'cyber-neon-purple': '#8A2BE2',
        'cyber-red': '#FF0000',
      },
      fontFamily: {
        'orbitron': ['"Orbitron"', 'sans-serif'],
        'jetbrains-mono': ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'neon': '0 0 5px #39FF14, 0 0 10px #39FF14, 0 0 20px #39FF14',
        'neon-blue': '0 0 5px #00FFFF, 0 0 10px #00FFFF, 0 0 20px #00FFFF',
      }
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false // Disable to prevent conflict with Docusaurus Infima styles
  }
}