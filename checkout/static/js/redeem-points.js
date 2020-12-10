$(document).ready(function(){

    $('#redeem-button').on('click', function(){
        var redeemed_point = $('input[name="using_points"]').val() || 0;
        var current_point = $('#credits_remaining').text();
        current_point = current_point.replace(/\D/g, '');
        if(redeemed_point < 0){
            alert("Cannot redeem negative amount");
            return;
        }
        if(redeemed_point > parseInt(current_point)){
            alert("Cannot redeem more than your credit");
            return;
        }

        req = $.ajax({
            url: "ajax/using_points/",
            dataType: "json",
            data: {'redeemed_point': redeemed_point}
        });
        req.done(function(data){
            var credits_remaining = data.credits_remaining;
            var per_credits_discount = data.per_credits_discount;
            var used_bonus = per_credits_discount*redeemed_point;
            var cart_cost = data.cart_cost;
            $('#credits_remaining').text("You have " + credits_remaining + " credit points");
            $('#credits_discount').text("- " + used_bonus);
            $('#total_cost').text("" + cart_cost-used_bonus);
        });
    });

});