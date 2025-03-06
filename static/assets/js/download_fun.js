$(document).ready(function () {
    $("#allstore").on("click",function(){
        if ($(this).prop("checked")){
            console.log('test');
            $(".selectDrop").addClass("d-none");
        }else{
            console.log('test1');
            $(".selectDrop").removeClass("d-none");
        }
    });
    $(document).on("change", ".storeValueFetch", function () {
        var selectize = $(this).selectize()[0].selectize,
         selectedValues = selectize.getValue();
        storeHtml = '<input type="hidden" name="storeName" id="store_name" value="' + selectedValues + '">'
        console.log(storeHtml);
        $("#downloadStoreName").empty().append(storeHtml);
    });
});