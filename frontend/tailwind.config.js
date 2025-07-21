/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        // Agricultural-inspired color palette
        primary: {
          50: '#f0f9f0',
          100: '#dcf2dc',
          200: '#bce5bc',
          300: '#8fd58f',
          400: '#5cb85c',
          500: '#2e7d32', // Main green
          600: '#256a29',
          700: '#1e5521',
          800: '#1a4419',
          900: '#163a15',
        },
        secondary: {
          50: '#fefdf0',
          100: '#fefadc',
          200: '#fef3b9',
          300: '#fdea86',
          400: '#fbde51',
          500: '#f9d71c', // Golden yellow for harvest theme
          600: '#e4c441',
          700: '#c09621',
          800: '#9c7a1a',
          900: '#81651b',
        },
        earth: {
          50: '#faf9f7',
          100: '#f2f0ec',
          200: '#e6e1d8',
          300: '#d4ccbc',
          400: '#b8aa93',
          500: '#8b7355', // Earth brown
          600: '#786247',
          700: '#65523c',
          800: '#544535',
          900: '#463b2f',
        },
        success: '#22c55e',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#3b82f6',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
      },
      fontSize: {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem',
        '6xl': '3.75rem',
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 40px -4px rgba(0, 0, 0, 0.06)',
        'strong': '0 10px 40px -15px rgba(0, 0, 0, 0.15), 0 20px 60px -6px rgba(0, 0, 0, 0.1)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'bounce-gentle': 'bounceGentle 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}