$(document).ready(function () {
    $(document).on("click", ".delValueFetch", function () {
        console.log('1')
        var selectize = $(this).prev('.delValueFetch').selectize()[0].selectize,
            selectedValues = selectize.getValue();
            if (selectedValues == "") {
                filter = '-'
                try {
                    $.ajax({
                        type: "GET",
                        url: "/productlist/" + filter + "/",
                        dataType: "json",
                        success: function (data) {
                            for (let i = 0; i < data.length; i++) {
                                selectize.clear();
                                $.each(data, function (index, option) {
                                    console.log(option);
                                    selectize.addOption({ value: option.item_code, text: option.item_name });
                                });
                                selectize.load(function (callback) {
                                    callback(data);
                                });
                            }
    
                        }
                    })
                }catch (i) {
                    console.log(i);
                }
                selectize.on('type', function (str) {
                    // Retrieve the search input value on key press
                    if (str != "") {
                        $.ajax({
                            type: "GET",
                            url: "/productlist/" + str + "/",
                            dataType: "json",
                            success: function (data) {
                                for (let i = 0; i < data.length; i++) {
                                    $.each(data, function (index, option) {
                                        selectize.addOption({ value: option.item_code, text: option.item_name });
                                    });
                                    selectize.load(function (callback) {
                                        callback(data);
                                    });
                                }
                            }
                        });
                    }
                });
            }
    });
});
