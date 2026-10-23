/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        transit: {
          dark: '#0B0F19',
          card: '#111827',
          cardHover: '#161F30',
          border: '#1F293D',
          muted: '#94A3B8',
          yellow: '#F59E0B',
          yellowLight: '#FDE68A',
          blue: '#38BDF8',
          indigo: '#6366F1',
          emerald: '#10B981',
          rose: '#F43F5E'
        }
      },
      fontFamily: {
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace']
      }
    },
  },
  plugins: [],
}
