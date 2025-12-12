/*
 * Theme switch logic for Just-the-Docs.
 * This script runs after the DOM is loaded and uses the theme's jtd functions.
 */
window.addEventListener("DOMContentLoaded", function() {
  // Ensure the jtd object is available before proceeding
  if (typeof jtd === 'undefined' || typeof jtd.setTheme !== 'function') {
    console.error("Just-the-Docs JS object (jtd) not found. Theme toggle aborted.");
    return;
  }

  const toggleDarkMode = document.getElementById("theme-toggle");

  if (!toggleDarkMode) {
    console.warn("Theme toggle button with id 'theme-toggle' not found.");
    return;
  }

  // Gets theme from localStorage, or system preference, or defaults to 'light'
  function getPreferredTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  // Updates the button icon based on the current theme
  function setButtonIcon(theme) {
    // If we're in dark mode, the button should show the sun (to switch to light)
    if (theme === 'dark') {
      // #svg-sun and #svg-moon are theme-provided SVG icons
      toggleDarkMode.innerHTML = `<svg width='18px' height='18px'><use href="#svg-sun"></use></svg>`;
      toggleDarkMode.setAttribute('aria-label', 'Switch to light theme');
    } else { // light mode
      // If we're in light mode, the button should show the moon (to switch to dark)
      toggleDarkMode.innerHTML = `<svg width='18px' height='18px'><use href="#svg-moon"></use></svg>`;
      toggleDarkMode.setAttribute('aria-label', 'Switch to dark theme');
    }
  }
  
  // Set initial theme on page load
  const initialTheme = getPreferredTheme();
  jtd.setTheme(initialTheme);
  setButtonIcon(initialTheme);
  
  // Save preference even on initial load to prevent theme mismatch if user changes OS theme later
  localStorage.setItem('theme', initialTheme);

  // Add event listener to toggle the theme on click
  jtd.addEvent(toggleDarkMode, 'click', function() {
    const currentTheme = jtd.getTheme(); 
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    jtd.setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    setButtonIcon(newTheme);
  });
});