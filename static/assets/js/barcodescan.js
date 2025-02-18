$(function () { 
    let isScannerActive = false;

    function fetchProductDetails(barcode) {
        const csrfToken = getCookie('csrftoken');
        const xhr = new XMLHttpRequest();
    
        xhr.open('POST', '/scanbarcode/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    
        xhr.onload = function () {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                console.log(response);
    
                if (response.success) {
                    const selectElement = document.querySelector('.itemValueFetch');
                    const tomSelectInstance = selectElement.tomselect;
                    const product = response.product;
    
                    if (tomSelectInstance) {
                        tomSelectInstance.clear(); // Clear previous selection
    
                        // Check if the option exists in TomSelect
                        let optionExists = Object.values(tomSelectInstance.options).some(opt => opt.title === product.name);
    
                        if (!optionExists) {
                            // Add option dynamically if not found
                            tomSelectInstance.addOption({
                                item_code: product.ids, // Match with valueField
                                item_name: product.name // Match with labelField
                            });
                        }
    
                        // Set the value based on item_code (id)
                        tomSelectInstance.setValue(product.ids);
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

    const codeReader = new ZXing.BrowserMultiFormatReader();

    // Start scanner on button click
    document.getElementById('start-scanner').addEventListener('click', async function () {
        if (isScannerActive) return;
        isScannerActive = true;

        const readerElement = document.getElementById('reader');
        readerElement.style.display = 'block';

        try {
            const videoInputDevices = await codeReader.listVideoInputDevices();
            let selectedDeviceId = videoInputDevices[0].deviceId;
            videoInputDevices.forEach((device) => {
                if (device.label.toLowerCase().includes('back')) {
                    selectedDeviceId = device.deviceId;
                }
            });

            codeReader.decodeFromVideoDevice(selectedDeviceId, 'reader', (result) => {
                if (result) {
                    console.log(`Scanned Code: ${result.getText()}`);
                    fetchProductDetails(result.getText());
                    codeReader.reset();
                    readerElement.style.display = 'none';
                    isScannerActive = false;
                }
            });
        } catch (err) {
            console.error('Error initializing scanner:', err);
            alert('Unable to access camera.');
            isScannerActive = false;
        }
    });

    // Handle Barcode Scanner Input (Physical Scanner)
    let barcodeBuffer = '';
    let typingTimer;
    const barcodeInputField = document.getElementById('barcode-input');

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && barcodeBuffer.length > 3) {
            console.log(barcodeBuffer);
            fetchProductDetails(barcodeBuffer);
            barcodeBuffer = '';
        } else if (event.key.length === 1) {
            barcodeBuffer += event.key;
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => { barcodeBuffer = ''; }, 500); // Reset buffer after 500ms
        }
    });

    // Autofocus input field when a scanner is used
    barcodeInputField.addEventListener('focus', function () {
        barcodeBuffer = '';
    });
});
