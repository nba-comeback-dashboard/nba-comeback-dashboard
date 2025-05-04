/**
 * NBA Test Charts JavaScript
 * 
 * This file contains custom functionality specific to the test_charts.html page
 */

// Function to create an NBA chart from JSON data
function createNBAChart(canvasId, chartData) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Use the NBA Dashboard plotter to create the chart
    const chartConfig = {
        type: 'line',
        data: {
            datasets: chartData.data.datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: chartData.title || 'NBA Test Chart',
                    font: { size: 16 }
                },
                subtitle: {
                    display: !!chartData.subtitle,
                    text: chartData.subtitle || '',
                    font: { size: 14 }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    position: 'bottom'
                }
            },
            scales: chartData.options?.scales || {
                x: {
                    title: {
                        display: true,
                        text: chartData.x_axis_title || 'X Axis'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: chartData.y_axis_title || 'Y Axis'
                    }
                }
            }
        }
    };
    
    // Create the chart
    new Chart(ctx, chartConfig);
}

// Function to fetch and process chart data, handling gzipped files
async function fetchChartData(url) {
    try {
        // Try to fetch the URL as is
        const response = await fetch(url);
        
        // If not found, try to fetch with .gz extension
        if (!response.ok && response.status === 404) {
            const gzResponse = await fetch(url + '.gz');
            
            if (!gzResponse.ok) {
                throw new Error(`Failed to fetch chart data: ${gzResponse.status}`);
            }
            
            // Get the gzipped data as an ArrayBuffer
            const gzData = await gzResponse.arrayBuffer();
            
            // Decompress using pako (ensure pako is included in the HTML)
            const decompressed = pako.inflate(new Uint8Array(gzData), { to: 'string' });
            
            // Parse the JSON
            return JSON.parse(decompressed);
        }
        
        // Regular JSON response
        return await response.json();
    } catch (error) {
        console.error('Error fetching chart data:', error);
        return null;
    }
}

// Initialize the test page once DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('NBA Test Charts page initialized');
    
    // Find all chart containers
    const chartContainers = document.querySelectorAll('.chart-container');
    
    // Process each chart container
    chartContainers.forEach(container => {
        const canvas = container.querySelector('canvas');
        if (canvas) {
            const canvasId = canvas.id;
            const dataUrl = container.querySelector('.chart-link').href;
            
            // Use our custom fetch function that handles gzipped data
            fetchChartData(dataUrl)
                .then(data => {
                    if (data) {
                        createNBAChart(canvasId, data);
                    }
                });
        }
    });
});