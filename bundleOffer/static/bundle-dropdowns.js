var lookup = {
    'Breakfast': ['Local', 'Energy Booster', 'Cereals', 'Jam and Spreads'],
    'Fruit and Vegetable': ['Fruits', 'Vegetables'],
    'Beverage': ['Tea', 'Coffee', 'Juice', 'Soft Drinks', 'Water', 'Powder Drinks'],
    'Meat and Fish': ['Meat', 'Fresh Fish', 'Dried Fish'],
    'Snacks': ['Noodles', 'Soups', 'Pasta', 'Chocolate', 'Local', 'Chips', 'Popcorn and nuts', 'Biscuits', 'Salad Dressing', 'Sauces'],
    'Dairy': ['Milk', 'Butter and cream', 'Cheese', 'Powder Milk', 'Yogurt and sweet'],
    'Frozen': ['Frozen', 'Canned'],
    'Bakery': ['Cookies', 'Snacks', 'Breads', 'Dips and spreads', 'Honey', 'Cakes'],
    'Baking Needs': ['Nut and dried fruit', 'Mixes', 'Ingredients', 'FLour'],
    'Cooking': ['Rice', 'Color and flavours', 'Pickles', 'Oil', 'Ghee', 'Ready Mix', 'Salt and Sugar', 'Dal or lentil', 'Shemai'],
    'Baby Food': ['Toddler Foods', 'Milk and Drinks'],
    'Diabetic Food': ['Diabetic'],
};

$(document).ready(function(){

    $(document.body).on('change', 'select[name="category"]' ,function(){
        var categoryName = $(this).val();
        var sub_category = $(this).closest('.user_card').find('select[name="sub_category"]');
        var product = $(this).closest('.user_card').find('select[name="products"]');

        sub_category.empty();
        product.empty();
        sub_category.append("<option value='' disabled selected>Sub-category</option>");
        for(i = 0; i < lookup[categoryName].length; i++){
            sub_category.append("<option value='" + lookup[categoryName][i] + "'>" + lookup[categoryName][i] + "</option>");
        }
    });

    $(document.body).on('change', 'select[name="sub_category"]', function(){
        var sub_categoryName = $(this).val();
        var categoryName = $(this).closest('.user_card').find('select[name="category"]').val();
        var product = $(this).closest('.user_card').find('select[name="products"]');
        product.empty();

        $.ajax({
            url: "http://127.0.0.1:8000/manage_product/stock/ajax/get_products/",
            data: {
                'category': categoryName,
                'subcategory': sub_categoryName
            },
            datatype: 'json',
            success: function(data) {
                for(i = 0; i < data.length; i++){
                    var product_name = data[i]['product_name'];
                    var product_id = data[i]['product_id'];
                    product.append("<option value='" + product_id.toString() + "'>" + product_name + "</option>");
                }
            },
            error: function() {
                alert("Something went wrong. Reload the page");
            }
        });
    });

});