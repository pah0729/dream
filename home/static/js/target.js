
var targets = [] ; // 모드 선택 요소를 넣을 배열 
var selectTarget = []; // 중복을 제거하고 선택된 요소를 넣을 배열
$(document).ready(function() {

    $('#example-example-enableFiltering-enableClickableOptgroups').multiselect({
        enableClickableOptGroups: true,
        enableCollapsibleOptGroups: true,
        enableFiltering: true,
        includeSelectAllOption: false
    });

    $(".multiselect-selected-text").html("수신자 선택");
    
    $("#addArr").click(function(e){
        $("#example-example-enableFiltering-enableClickableOptgroups option:selected ").each(function(){
            targets.push ( $(this).text()+"") ;
            $.each(targets, function(i, el){
                if($.inArray(el, selectTarget) === -1)selectTarget.push(el);
            });
        });
        $("#id_targets").val(selectTarget);

    }) ;
    $('.multiselect-native-select .btn-group, button').addClass('btn-block');
});

