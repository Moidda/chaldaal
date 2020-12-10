$(document).ready(function(){

    var index = 0;

    $(document.body).on('click', '.p-remove' ,function(){
        $(this).closest('.user_card').remove();
        index = index-1;
        if(index == 0)
            $('.container').find('button[class="btn btn-primary create"]').remove();
    });

    $('.p-add').on('click', function(){
        if(index == 0)
            $('.container').append('<button type="button" class="btn btn-primary create">Create</button>');

        if(index == 3){
            alert("Cannot add more than 3 items");
            return;
        }
        $('.p-list').append('' +
            '<div class="user_card">' +
                '<div class="input-group mb-2">' +
                    '<select name="category" class="form-control" required>' +
                        '<option disabled selected hidden>Category</option>' +
                        '<option value="Breakfast">Breakfast</option>' +
                        '<option value="Fruit and Vegetable">Fruit and Vegetable</option>' +
                        '<option value="Beverage">Beverage</option>' +
                        '<option value="Meat and Fish">Meat and Fish</option>' +
                        '<option value="Snacks">Snacks</option>' +
                        '<option value="Dairy">Dairy</option>' +
                        '<option value="Frozen">Frozen</option>' +
                        '<option value="Bakery">Bakery</option>' +
                        '<option value="Baking Needs">Baking Needs</option>' +
                        '<option value="Cooking">Cooking</option>' +
                        '<option value="Baby Food">Baby Food</option>' +
                        '<option value="Diabetic Food">Diabetic Food</option>' +
                    '</select>' +
                '</div>' +

                '<div class="input-group mb-2">' +
                    '<select name="sub_category" class="form-control" required>' +
                        '<option value="" disabled selected>Sub-category</option>' +
                    '</select>' +
                '</div>' +

                '<div class="input-group mb-2">' +
                    '<select name="products" class="form-control" required>' +
                        '<option value="" disabled selected>Product</option>' +
                    '</select>' +
                '</div>' +

                '<div class="input-group mb-2">' +
                    '<input type="number" name="bundle_count" placeholder="Amount" class="form-control" required>' +
                '</div>' +

                '<button type="button" class="btn btn-danger p-remove">' +
                    'Remove Item' +
                '</button>' +
            '</div>'
        );
        index = index + 1;
    });

});
