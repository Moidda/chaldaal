$(document).ready(function(){

    $(document.body).on('click', '.create', function(){
        var valid = true;
        var plist = [];
        var bundle_name = $('#bundle_name').val();
        var bundle_cost = $('#bundle_cost').val();

        $('.user_card').each(function(){
            var product_id = $(this).find('select[name="products"]').val();
            var amount = $(this).find('input').val();
            if(product_id == null || amount == null || amount <= 0) valid = false;
            else {
                plist.push(product_id);
                plist.push(amount);
            }
        });

        if(valid == false || bundle_name == null || bundle_cost == null){
            alert('Some fields are missing');
            return;
        }

        req = $.ajax({
            url: "ajax/create_bundle_offer/",
            dataType: "json",
            data: {
                'product_list': plist,
                'bundle_cost': bundle_cost,
                'bundle_name': bundle_name
            }
        });
        req.done(function(data){
            alert("Bundle offer created successfully!");
            $('.user_card').each(function(){
                $(this).remove();
            });
            $('#bundle_name').val('');
            $('input[name="bundle_cost"]').val('');
            $('button[class="btn btn-primary create"]').remove();
        });
    });

});