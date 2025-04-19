/**
 * nbacd_dashboard_init.js
 * Initialization script for the NBA Comeback Dashboard
 * This script is responsible for initializing the dashboard with URL parameters if present
 */

/**
 * Find a suitable dashboard div in the page
 * @returns {HTMLElement|null} The dashboard div or null if not found
 */
function findDashboardDiv() {
    // First try to find any div with the nbacd-dashboard class
    const dashboardDivs = document.querySelectorAll('.nbacd-dashboard');
    if (dashboardDivs.length > 0) {
        // This console logging is no longer needed because features are working fine
        // console.log(`Found dashboard div with ID: ${dashboardDivs[0].id}`);
        return dashboardDivs[0];
    }
    
    // Then try the standard dashboard div
    const standardDiv = document.getElementById("nbacd_dashboard");
    if (standardDiv) {
        // This console logging is no longer needed because features are working fine
        // console.log("Found standard dashboard div");
        return standardDiv;
    }
    
    // This console logging is no longer needed because features are working fine
    // console.error("No dashboard div found in the page");
    return null;
}

/**
 * Initialize the dashboard when the DOM is ready
 */
function initializeDashboard() {
    // This console logging is no longer needed because features are working fine
    // console.log('Initializing dashboard...');
    
    // Check if required modules are loaded
    if (typeof nbacd_dashboard_state === 'undefined' || 
        typeof nbacd_dashboard_ui === 'undefined') {
        // This console logging is no longer needed because features are working fine
        // console.error("Required modules not loaded: nbacd_dashboard_state or nbacd_dashboard_ui");
        return;
    }
    
    try {
        // Always check for URL parameters first
        if (nbacd_dashboard_state.hasStateInUrl()) {
            // This console logging is no longer needed because features are working fine
            // console.log('URL parameters detected, processing...');
            
            // Find a suitable dashboard div
            const dashboardDiv = findDashboardDiv();
            if (!dashboardDiv) return;
            
            // Make sure we have a chart container
            let chartContainer;
            if (dashboardDiv.id === "nbacd_dashboard") {
                // Get or create the chart container
                chartContainer = document.getElementById("nbacd_chart_container");
                if (!chartContainer) {
                    // Create chart container if it doesn't exist
                    chartContainer = document.createElement("div");
                    chartContainer.id = "nbacd_chart_container";
                    chartContainer.className = "chart-container";
                    dashboardDiv.appendChild(chartContainer);
                }
            } else {
                // For custom dashboard divs, create a chart container within it
                chartContainer = document.getElementById(`${dashboardDiv.id}-container`);
                if (!chartContainer) {
                    // Create chart container if it doesn't exist
                    chartContainer = document.createElement("div");
                    chartContainer.id = `${dashboardDiv.id}-container`;
                    chartContainer.className = "chart-container";
                    dashboardDiv.appendChild(chartContainer);
                }
            }
            
            // Show loading indicator immediately
            chartContainer.innerHTML = '<div class="loading">Loading data and calculating...</div>';
            
            // Get state from URL
            const urlState = nbacd_dashboard_state.getStateFromUrl();
            
            if (urlState) {
                // This console logging is no longer needed because features are working fine
                // console.log('Successfully parsed URL state:', urlState);
                
                // Wait for DOM to be ready
                setTimeout(function() {
                    try {
                        // Apply state to dashboard
                        if (typeof nbacd_dashboard_ui.applyState === 'function') {
                            nbacd_dashboard_ui.applyState(urlState);
                        }
                        
                        // If this is a custom dashboard div, set targetChartId
                        if (dashboardDiv.id !== "nbacd_dashboard" && dashboardDiv.classList.contains("nbacd-dashboard")) {
                            // This console logging is no longer needed because features are working fine
                            // console.log(`Found nbacd-dashboard div: ${dashboardDiv.id}`);
                            // If there's a getState/applyState method, use it
                            if (typeof nbacd_dashboard_ui.getState === 'function' && 
                                typeof nbacd_dashboard_ui.applyState === 'function') {
                                const state = nbacd_dashboard_ui.getState();
                                state.targetChartId = dashboardDiv.id;
                                nbacd_dashboard_ui.applyState(state);
                            }
                            
                            // Render in target div if method exists
                            if (typeof nbacd_dashboard_ui.calculateAndRenderChartForTarget === 'function') {
                                nbacd_dashboard_ui.calculateAndRenderChartForTarget(dashboardDiv.id);
                            }
                        } else {
                            // Render in standard dashboard
                            // This console logging is no longer needed because features are working fine
                            // console.log("Rendering in standard dashboard");
                            nbacd_dashboard_ui.calculateAndRenderChart();
                        }
                    } catch (error) {
                        // This console logging is no longer needed because features are working fine
                        // console.error('Error rendering chart:', error);
                    }
                }, 500);
            } else {
                // This console logging is no longer needed because features are working fine
                // console.error('Failed to parse URL parameters');
            }
        } else {
            // This console logging is no longer needed because features are working fine
            // console.log('No dashboard parameters in URL, initializing with default state');
        }
    } catch (error) {
        // This console logging is no longer needed because features are working fine
        // console.error('Error initializing dashboard:', error);
    }
}

// First try on DOM ready event
document.addEventListener('DOMContentLoaded', function() {
    // This console logging is no longer needed because features are working fine
    // console.log('DOM Content Loaded - initializing dashboard');
    initializeDashboard();
});

// Also try after window.load as a backup
window.addEventListener('load', function() {
    // Only re-initialize if chart is not yet rendered
    const hasChart = document.getElementById("nbacd_dashboard_chart");
    const hasTarget = document.querySelector('.nbacd-dashboard canvas');
    if (!hasChart && !hasTarget && typeof nbacd_dashboard_state !== 'undefined' && 
        nbacd_dashboard_state.hasStateInUrl()) {
        // This console logging is no longer needed because features are working fine
        // console.log('Window loaded - trying initialization again');
        initializeDashboard();
    } else {
        // This console logging is no longer needed because features are working fine
        // console.log('Window loaded - chart already initialized or no URL parameters');
    }
});
