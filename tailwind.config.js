/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './marketing/templates/**/*.html',
    './marketing/static/**/*.js',
    './static/js/**/*.js',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    fontFamily: {
      heading: ['"Poppins"', 'Segoe UI', 'Calibri', 'Helvetica Neue', 'Arial', 'sans-serif'],
      sans: ['"Open Sans"', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'sans-serif']
    },
    extend: {
      colors: {
        'todde-blue': '#009196',
        'todde-blue-dark': '#007A7C',
        'todde-blue-light': '#33B8B3',
        'todde-dark': '#383838',
        'todde-jet': '#383838',
        'todde-neutral': '#F3F7F8',
        'todde-muted': '#6E7A7B',
        'todde-success': '#25C7B4',
        'todde-orange': '#383838',
        'todde-orange-dark': '#383838',
        'todde-amber': '#F9B067',
        'todde-caramel': '#B85B11',
        'todde-caramel-soft': '#8C3C05',
        'todde-cream': '#FFF0E1'
      },
      boxShadow: {
        subtle: '0 10px 30px -12px rgba(12, 46, 138, 0.2)',
        card: '0 20px 45px -20px rgba(12, 46, 138, 0.35)'
      },
      borderRadius: {
        none: '0',
        sm: '0',
        DEFAULT: '0',
        md: '0',
        lg: '0',
        xl: '0',
        '2xl': '0',
        '3xl': '0',
        full: '0'
      }
    },
    container: {
      center: true,
      padding: {
        DEFAULT: '1rem',
        sm: '1.5rem',
        lg: '2rem',
        xl: '3rem',
        '2xl': '4rem'
      },
      screens: {
        sm: '640px',
        md: '768px',
        lg: '1024px',
        xl: '1280px',
        '2xl': '1366px'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('flowbite/plugin')
  ]
}
