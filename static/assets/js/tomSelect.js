$(document).ready(function () {
    $(".itemValueFetch").each(function () {
        // Initialize TomSelect and store the instance in the element's data
        var tomSelectInstance = new TomSelect(this, {
            maxItems: 1,  // Allow only one selection
            create: false, // Prevent users from entering custom values
            plugins: ['remove_button'], // Adds a remove button
            valueField: 'item_code',
            labelField: 'item_name',
            searchField: 'item_name',
            load: function (query, callback) {
                var url = "/productlist/" + (query ? query : "-") + "/";
                
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

    // Event listener for the change event
    $(document).on("change", ".itemValueFetch", function () {
        // Access the TomSelect instance from the element's data
        var selectize = $(this).data('tomSelectInstance'); // Retrieve instance via jQuery's data()

        // If selectize is defined, retrieve the selected value
        if (selectize) {
            var selectedValues = encodeURIComponent(selectize.getValue()); // Get and encode the selected value
            var value = [];

            try {
                $.ajax({
                    type: "GET",
                    url: "/getpacksize/?value=" + selectedValues, // Send the selected value in the request
                    dataType: "json",
                    success: function (data) {
                        if (data.product && data.product.packSize) {
                            // Loop through the pack size options and create <option> elements
                            data.product.packSize.forEach(function (size) {
                                value += '<option value="' + size + '">' + size + "</option>";
                            });
                            console.log(value);
                            $("#packsize").empty(); // Clear the previous options
                            $("#packsize").append(value); // Append new options to the dropdown
                        }
                    },
                    error: function (xhr, status, error) {
                        console.log('Error:', error); // Log any errors for debugging
                    }
                });
            } catch (i) {
                console.log(i); // Catch any potential errors
            }
        }
    });
});
