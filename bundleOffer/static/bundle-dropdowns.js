$(document).ready(function(){

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

    $(document.body).on('change', 'select[name="category"]' ,function(){
        var card = $(this).closest('.user-card');
        var categoryName = $(this).attr('name');
        alert(categoryName);
//        var sub_category = card.find('select[name="sub_category"]');
//
//        for(i = 0; i < lookup[categoryName]; i++){
//            sub_category.append("<option value='" + lookup[categoryName][i] + "'>" + lookup[categoryName][i] + "</option>");
//        }
    });

});