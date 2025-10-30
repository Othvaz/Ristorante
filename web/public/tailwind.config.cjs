module.exports = {
    content: ["./public/**/*.html"],
    theme: { extend: {
      backgroundImage: {
        'radial-gradient-circle': 'radial-gradient(circle, var(--tw-gradient-stops))',
        'radial-gradient-ellipse': 'radial-gradient(ellipse at center, var(--tw-gradient-stops))',
        'radial-at-tl': 'radial-gradient(at top left, var(--tw-gradient-stops))',
      }
    } },
    plugins: [],
  };