$(document).ready(function () {
    $(document).on("click", ".delValueFetch", function () {
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
                                selectize.clearOptions();
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
    $("#logout").on("click",function(){
        $('#myForm .input-field').each(function() {
            var inputField = $(this);
            if (inputField.attr('required')) {
                inputField.removeAttr('required');
            } else {
                inputField.attr('required', 'required');
            }
        });
    });
    //hide the store dropdown 
    $("#password").on("click focus", function() {
        var username = $("#username").val();
        if  (username.includes("dow")) {
            console.log('inside');
            $(".storediv").attr('hidden', true),
            $(".storedropdown").attr('hidden', true),
            $(".cartonbox").attr('hidden', true),
            $(".cartonboxdiv").attr('hidden', true);

        }
        else{
            $(".storediv").removeAttr('hidden'),
            $(".storedropdown").removeAttr('hidden'),
            $(".cartonbox").removeAttr('hidden'),
            $(".cartonboxdiv").removeAttr('hidden');
        }

    });
    $("#signin").on("click",function(){
        var spanElement = $('.selectize-input span'); 
        if (spanElement.length > 0){
         if ($(".storedropdown").prop('hidden')){
            console.log('test');
            $("#storeValueFetch").removeAttr('required'),
            $("#rackno").removeAttr('required');
        }}
        else{
            if($(".storediv").prop('hidden')){
                $("#storeValueFetch").removeAttr('required'),
                $("#rackno").removeAttr('required');
            }else{
                $("#storeValueFetch").attr('required', 'required');
                $("#rackno").attr('required', 'required');
            }
        }
    });
    // $(document).on("change", ".delValueFetch", function () {
    //     var selectize = $(this)[0].selectize;
    //     var selectedValues = encodeURIComponent(selectize.getValue());
        
    //     var value = [];
    //     try{
    //         $.ajax({
    //             type: "GET",
    //             url: "/getpacksize/?value=" + selectedValues ,
    //             dataType: "json",
    //             success: function (data) {
    //                 data.product.packSize.forEach(function (size) {
    //                     value += '<option value="' + size + '">' + size + "</option>";
    //                 });
    //                 console.log(value);
    //                 $("#packsize").empty();
    //                 $("#packsize").append(value);
    //             }
    //         })
    //     }catch(i){
    //         console.log(i);
    //     }
    // });
    // for dow user need to hide the store details
    $('#storeValueFetch').selectize({
        create: true,
        placeholder: "Select a store",
        onInitialize: function() {
            this.$control_input.attr("name", "store_name");
            // Ensure proper width
            this.$control.css('width', '100%');
        }
    });
    $(document).on("click", ".storeValueFetch", function () {
        var selectize = $(this).prev('.storeValueFetch').selectize()[0].selectize,
            selectedValues = selectize.getValue();
            if (selectedValues == "") {
                filter = '-'
                try {
                    $.ajax({
                        type: "GET",
                        url: "/storelist/" + filter + "/",
                        dataType: "json",
                        success: function (data) {
                            for (let i = 0; i < data.length; i++) {
                                selectize.clear();
                                $.each(data, function (index, option) {
                                    selectize.addOption({ value: option.store_code, text: option.store_name });
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
                            url: "/storelist/" + str + "/",
                            dataType: "json",
                            success: function (data) {
                                selectize.clearOptions();
                                for (let i = 0; i < data.length; i++) {
                                    $.each(data, function (index, option) {
                                        selectize.addOption({ value: option.store_code, text: option.store_name });
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
    // $("#manualCheck").on("click",function(){
    //    if($("#manualCheck").prop("checked")){
    //     $("#packsize").attr("hidden",true),
    //     $("#packsize_input").attr("hidden",false),
    //     $("#packsize").removeAttr("required");
    //    }else{
    //     $("#packsize").attr("hidden",false),
    //     $("#packsize_input").attr("hidden",true),
    //     $("#packsize_input").removeAttr("required");
    //    } 
    // });
});
// Add the selected store name into the hidden field
$(document).on("change", ".storeValueFetch", function () {
    var selectize = $(this).selectize()[0].selectize,
     selectedValues = selectize.getValue();
    storeHtml = '<input type="hidden" name="store_name" id="store_name" value="' + selectedValues + '">'
    $("#getstorename").empty().append(storeHtml);
});
document.addEventListener("DOMContentLoaded", function () {
    const barcodeInput = document.getElementById("enterBarcode");
    
    barcodeInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent form submission
        }
    });
});
