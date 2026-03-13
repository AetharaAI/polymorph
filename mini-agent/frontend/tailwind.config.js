/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0F1117',
        foreground: '#E2E8F0',
        card: '#1A1D2E',
        'card-foreground': '#E2E8F0',
        primary: '#8B5CF6',
        'primary-foreground': '#FFFFFF',
        secondary: '#1E293B',
        'secondary-foreground': '#E2E8F0',
        muted: '#1E293B',
        'muted-foreground': '#94A3B8',
        accent: '#06B6D4',
        'accent-foreground': '#FFFFFF',
        destructive: '#EF4444',
        border: '#334155',
        ring: '#8B5CF6',
        thinking: '#F59E0B',
      },
    },
  },
  plugins: [],
}
