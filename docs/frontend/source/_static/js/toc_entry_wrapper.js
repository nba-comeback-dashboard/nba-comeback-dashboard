document.addEventListener('DOMContentLoaded', function() {
    // Find all toc-entry-container elements that are not already in a toc-entries-wrapper
    const tocEntries = Array.from(document.querySelectorAll('.toc-entry-container')).filter(entry => {
        return !entry.closest('.toc-entries-wrapper');
    });
    
    // If there are multiple entries, wrap them in a container
    if (tocEntries.length > 1) {
        // Create a wrapper element
        const wrapper = document.createElement('div');
        wrapper.className = 'toc-entries-wrapper';
        
        // Get the parent of the first entry
        const parent = tocEntries[0].parentNode;
        
        // Insert the wrapper before the first entry
        parent.insertBefore(wrapper, tocEntries[0]);
        
        // Move all entries into the wrapper
        tocEntries.forEach(entry => {
            wrapper.appendChild(entry);
        });
    }
});