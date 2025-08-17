// SwarmUI Random Image Button Enhancement
// Add this to SwarmUI's custom JavaScript to get a "Random Image" button

// Function to select a random image and set it as init image
async function selectRandomInitImage() {
    try {
        const button = document.getElementById('random-image-btn');
        const originalText = button.textContent;
        button.textContent = 'Selecting...';
        button.disabled = true;

        // Call the API to select random image
        const response = await fetch('/API/SelectRandomImage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                folder: 'random_init_images',
                seed: -1 // Random selection
            })
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                // Set the selected image as init image
                const initImageInput = document.querySelector('input[data-param-id="initimage"]');
                if (initImageInput) {
                    initImageInput.value = result.imagePath;
                    initImageInput.dispatchEvent(new Event('change', { bubbles: true }));
                    
                    // Show success message
                    showNotification(`Random image selected: ${result.filename}`, 'success');
                } else {
                    showNotification('Could not find init image input field', 'error');
                }
            } else {
                showNotification(result.error || 'Failed to select random image', 'error');
            }
        } else {
            showNotification('Failed to call random image API', 'error');
        }
    } catch (error) {
        console.error('Random image selection error:', error);
        showNotification('Error selecting random image: ' + error.message, 'error');
    } finally {
        const button = document.getElementById('random-image-btn');
        button.textContent = originalText;
        button.disabled = false;
    }
}

// Function to show notifications
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    const container = document.querySelector('.container-fluid') || document.body;
    container.insertBefore(notification, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Function to add the Random Image button to the interface
function addRandomImageButton() {
    // Look for the init image section
    const initImageSection = document.querySelector('[data-param-id="initimage"]')?.closest('.param-box') || 
                            document.querySelector('.init-image-group') ||
                            document.querySelector('#init_image_group');
    
    if (initImageSection) {
        // Check if button already exists
        if (document.getElementById('random-image-btn')) {
            return;
        }

        // Create the button
        const randomButton = document.createElement('button');
        randomButton.id = 'random-image-btn';
        randomButton.type = 'button';
        randomButton.className = 'btn btn-sm btn-secondary ms-2';
        randomButton.innerHTML = '🎲 Random Image';
        randomButton.title = 'Select a random image from random_init_images folder';
        randomButton.onclick = selectRandomInitImage;

        // Find the best place to insert the button
        const initImageInput = initImageSection.querySelector('input[type="text"]') || 
                              initImageSection.querySelector('input[data-param-id="initimage"]');
        
        if (initImageInput && initImageInput.parentNode) {
            // Add button next to the input
            initImageInput.parentNode.appendChild(randomButton);
        } else {
            // Add button at the end of the section
            initImageSection.appendChild(randomButton);
        }

        console.log('Random Image button added to SwarmUI interface');
    } else {
        console.log('Init image section not found, will retry...');
        // Retry in 2 seconds if not found (page might still be loading)
        setTimeout(addRandomImageButton, 2000);
    }
}

// Add button when page loads
document.addEventListener('DOMContentLoaded', addRandomImageButton);

// Also try when the page changes (for SPAs)
window.addEventListener('load', addRandomImageButton);

// For SwarmUI's dynamic loading, also try periodically
setTimeout(addRandomImageButton, 1000);
setTimeout(addRandomImageButton, 3000);
setTimeout(addRandomImageButton, 5000);

console.log('SwarmUI Random Image Button script loaded');
