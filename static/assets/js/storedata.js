$(document).ready(function () {
    $(".storedataValueFetch").each(function () {
        // Initialize TomSelect and store the instance in the element's data
        var tomSelectInstance = new TomSelect(this, {
            maxItems: 1,  // Allow only one selection
            create: false, // Prevent users from entering custom values
            plugins: ['remove_button'], // Adds a remove button
            valueField: 'item_code',
            labelField: 'item_name',
            searchField: 'item_name',
            load: function (query, callback) {
                var url = "/storeproductlist/" + (query ? query : "-") + "/";
                
                $.ajax({
                    type: "GET",
                    url: url,
                    dataType: "json",
                    success: function (data) {
                        callback(data); // Pass the data to TomSelect's callback function
                    },
                    error: function (xhr, status, error) {
                        callback([]); // Return empty array in case of error
                        console.log('Error fetching data:', error);
                    }
                });
            },
            onItemAdd: function () {
                // Disable input after selecting one item
                this.control_input.disabled = true;
            },
            onItemRemove: function () {
                // Re-enable input when the selected item is removed
                this.control_input.disabled = false;
            }
        });

        // Manually store the TomSelect instance in the element’s data
        $(this).data('tomSelectInstance', tomSelectInstance);
    });
});
