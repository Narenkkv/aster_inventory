$(function () {
    let isScannerActive = false; // Flag to prevent multiple activations

    function fetchProductDetails(barcode) {
        const csrfToken = getCookie('csrftoken'); // Get CSRF token
        const xhr = new XMLHttpRequest();

        xhr.open('POST', '/scanbarcode/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        xhr.onload = function () {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                console.log(response);
                if (response.success) {
                    const productName = response.product['name'];
                    console.log(productName);

                    // Correct way to access Selectize.js instance
                    const $selectizeControl = $('.delValueFetch')[0].selectize;

                    if ($selectizeControl) {
                        // Clear existing options and add the new one
                        $selectizeControl.clearOptions();
                        $selectizeControl.addOption({ value: response.product['ids'], text: response.product['name'] });
                        $selectizeControl.setValue(response.product['ids']);
                    } else {
                        console.error('Selectize control not found.');
                    }
                } else {
                    alert(response.message || 'Product not found!');
                }
            } else {
                console.error('Error fetching product details:', xhr.responseText);
                alert('An error occurred while fetching product details.');
            }
        };

        xhr.send(`csrfmiddlewaretoken=${csrfToken}&barcode=${barcode}`);
    }

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initialize ZXing BrowserMultiFormatReader
    const codeReader = new ZXing.BrowserMultiFormatReader();

    // Start scanner on button click
    document.getElementById('start-scanner').addEventListener('click', async function () {
        if (isScannerActive) return; // Don't start the scanner if it's already active
        isScannerActive = true; // Set flag to indicate scanner is active

        const readerElement = document.getElementById('reader');
        readerElement.style.display = 'block'; // Show the reader container

        try {
            // List video input devices
            const videoInputDevices = await codeReader.listVideoInputDevices();

            // Select the back camera (if available)
            let selectedDeviceId = videoInputDevices[0].deviceId; // Default to the first device
            videoInputDevices.forEach((device) => {
                if (device.label.toLowerCase().includes('back')) {
                    selectedDeviceId = device.deviceId;
                }
            });

            // Start decoding video stream from the selected camera
            codeReader.decodeFromVideoDevice(selectedDeviceId, 'reader', (result) => {
                if (result) {
                    console.log(`Scanned Code: ${result.getText()}`);
                    fetchProductDetails(result.getText()); // Send barcode to server
                    // Optionally reset scanner or stop here
                    codeReader.reset(); // Stop scanner after successful scan
                    readerElement.style.display = 'none'; // Hide reader container
                    isScannerActive = false; // Reset flag
                }
            });
        } catch (err) {
            console.error('Error initializing scanner:', err);
            alert('Unable to access camera.');
            isScannerActive = false; // Reset flag on error
        }
    });
});
