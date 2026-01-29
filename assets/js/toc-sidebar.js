// Generate table of contents from page headings
(function() {
  function generateTOC() {
    const mainContent = document.querySelector('.main-content');
    if (!mainContent) return;

    const headings = mainContent.querySelectorAll('h1, h2, h3, h4, h5, h6');
    if (headings.length === 0) return;

    // Create TOC container
    const tocContainer = document.createElement('div');
    tocContainer.id = 'toc-sidebar';
    tocContainer.className = 'toc-sidebar';

    const tocTitle = document.createElement('div');
    tocTitle.className = 'toc-title';
    tocTitle.textContent = 'In this article';
    tocContainer.appendChild(tocTitle);

    const tocList = document.createElement('ul');
    tocList.className = 'toc-list';

    headings.forEach((heading, index) => {
      // Skip the first h1 if it's the page title
      if (index === 0 && heading.tagName === 'H1') {
        return;
      }

      // Ensure heading has an ID
      if (!heading.id) {
        heading.id = 'heading-' + index + '-' + heading.textContent.toLowerCase()
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-|-$/g, '');
      }

      const listItem = document.createElement('li');
      listItem.className = 'toc-item toc-' + heading.tagName.toLowerCase();

      const link = document.createElement('a');
      link.href = '#' + heading.id;
      link.textContent = heading.textContent;
      link.className = 'toc-link';

      listItem.appendChild(link);
      tocList.appendChild(listItem);
    });

    if (tocList.children.length > 0) {
      tocContainer.appendChild(tocList);
      
      // Insert TOC after main content wrapper or in a specific location
      const mainWrapper = document.querySelector('.main-content-wrap') || 
                         document.querySelector('.main') ||
                         document.body;
      
      // Try to find the right sidebar area or create one
      let sidebar = document.querySelector('.toc-sidebar-container');
      if (!sidebar) {
        sidebar = document.createElement('div');
        sidebar.className = 'toc-sidebar-container';
        mainWrapper.appendChild(sidebar);
      }
      sidebar.appendChild(tocContainer);

      // Highlight active section on scroll
      highlightActiveSection();
      window.addEventListener('scroll', highlightActiveSection);
    }
  }

  function highlightActiveSection() {
    const headings = document.querySelectorAll('.main-content h1, .main-content h2, .main-content h3, .main-content h4, .main-content h5, .main-content h6');
    const tocLinks = document.querySelectorAll('.toc-link');
    
    let currentSection = '';
    const scrollPosition = window.scrollY + 100; // Offset for header

    headings.forEach((heading) => {
      const top = heading.offsetTop;
      if (scrollPosition >= top) {
        currentSection = heading.id;
      }
    });

    tocLinks.forEach((link) => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + currentSection) {
        link.classList.add('active');
      }
    });
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', generateTOC);
  } else {
    generateTOC();
  }
})();