// Wait for the window to load all theme assets, including the search index (window.search)
window.addEventListener('load', function() {

  // Ensure Lunr and its language plugins are available
  if (window.lunr && window.search && lunr.hy && lunr.multiLanguage) {
    
    // Check if an index (window.idx) has already been created by the theme.
    // If not, or if we need to ensure multilingual support:
    
    // Re-initialize Lunr using the multiLanguage plugin.
    window.idx = lunr(function () {
      
      // CRITICAL STEP: Use both English ('en') and Armenian ('hy') in the pipeline.
      // 'en' is safe to include for processing the JSON keys (title, content, etc.).
      this.use(lunr.multiLanguage('en', 'hy')); 
      
      // Define the fields Lunr should index (matching the fields used by Just the Docs)
      this.ref('id');
      this.field('title', { boost: 20 });
      this.field('content', { boost: 10 });
      this.field('url');

      // Add all your document data to the new multi-language index
      for (var key in window.search) {
        this.add(window.search[key]);
      }
    });

    console.log("Lunr Index successfully initialized with Armenian (hy) support.");
  }
});