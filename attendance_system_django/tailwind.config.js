// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    // Add any other paths where you use Tailwind classes
  ],
  theme: {
    extend: {
      colors: {
        // Your existing custom colors
        primary: 'hsl(var(--primary))', // Use HSL format for CSS variables
        'primary-foreground': 'hsl(var(--primary-foreground))',
        secondary: 'hsl(var(--secondary))',
        'secondary-foreground': 'hsl(var(--secondary-foreground))',
        muted: 'hsl(var(--muted))',
        'muted-foreground': 'hsl(var(--muted-foreground))',
        accent: 'hsl(var(--accent))',
        'accent-foreground': 'hsl(var(--accent-foreground))',
        destructive: 'hsl(var(--destructive))',
        'destructive-foreground': 'hsl(var(--destructive-foreground))',
        card: 'hsl(var(--card))',
        'card-foreground': 'hsl(var(--card-foreground))',
        popover: 'hsl(var(--popover))',
        'popover-foreground': 'hsl(var(--popover-foreground))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        // Add border color mapping here
        border: 'hsl(var(--border))', // <--- Add this line for your custom border color
        background: 'hsl(var(--background))', // Make sure these are also defined
        foreground: 'hsl(var(--foreground))', // if you want to use them directly as classes
      },
      // You also have a 'radius' variable, for this you extend 'borderRadius'
      borderRadius: {
        lg: 'var(--radius)', // or whatever size you map it to
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      // And potentially for fonts if you named them
      fontFamily: {
        // If you define 'Inter' as a custom font in Tailwind
        sans: ['Inter', ...require('tailwindcss/defaultTheme').fontFamily.sans],
      }
    },
  },
  plugins: [],
}