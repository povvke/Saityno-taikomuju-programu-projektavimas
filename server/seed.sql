-- Insert parent categories
INSERT INTO category (name, description, parent_category, slug) VALUES
('Breakfast', 'Morning meals to start your day', NULL, 'breakfast'),
('Lunch', 'Midday meals', NULL, 'lunch'),
('Dinner', 'Evening meals', NULL, 'dinner'),
('Dessert', 'Sweet treats and desserts', NULL, 'dessert');

-- Insert breakfast subcategories
INSERT INTO category (name, description, parent_category, slug) VALUES
('Eggs', 'Egg-based breakfast dishes', 1, 'eggs'),
('Pancakes & Waffles', 'Fluffy breakfast staples', 1, 'pancakes-waffles'),
('Smoothies', 'Blended breakfast drinks', 1, 'smoothies');

-- Insert lunch subcategories
INSERT INTO category (name, description, parent_category, slug) VALUES
('Salads', 'Fresh and light salad options', 2, 'salads'),
('Sandwiches', 'Bread-based lunch favorites', 2, 'sandwiches'),
('Pasta', 'Pasta-based dishes', 2, 'pasta');

-- Insert dinner subcategories
INSERT INTO category (name, description, parent_category, slug) VALUES
('Pork', 'Pork-based main courses', 3, 'pork'),
('Chicken', 'Chicken-based main courses', 3, 'chicken'),
('Fish', 'Seafood and fish dishes', 3, 'fish'),
('Vegetarian', 'Meat-free dinner options', 3, 'vegetarian');

-- Insert dessert subcategories
INSERT INTO category (name, description, parent_category, slug) VALUES
('Cakes', 'Layer cakes and sheet cakes', 4, 'cakes'),
('Cookies', 'Baked cookies and treats', 4, 'cookies'),
('Chocolate', 'Chocolate desserts', 4, 'chocolate');

-- Insert breakfast recipes (Eggs - category_id 5)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Scrambled Eggs', 'Soft and creamy scrambled eggs', 'Beat eggs, cook in butter on medium heat until soft', '{"eggs": 3, "butter": "1 tbsp", "salt": "to taste", "pepper": "to taste"}', 180, 10, 2, 5, 'scrambled-eggs', 3),
('Egg Frittata', 'Italian-style baked eggs with vegetables', 'Mix eggs with veggies, cook on stovetop then finish in oven', '{"eggs": 6, "peppers": 1, "onions": 1, "cheese": "1 cup"}', 240, 25, 4, 5, 'egg-frittata', 3),
('Eggs Benedict', 'Poached eggs on English muffin with hollandaise', 'Poach eggs, toast muffin, pour hollandaise sauce on top', '{"eggs": 2, "english_muffin": 1, "hollandaise": "1/2 cup"}', 320, 20, 1, 5, 'eggs-benedict', 3),
('Egg Fried Rice', 'Quick egg and rice breakfast', 'Scramble eggs, mix with cooked rice and vegetables', '{"eggs": 2, "rice": "1 cup", "peas": "1/2 cup", "soy_sauce": "2 tbsp"}', 260, 15, 2, 5, 'egg-fried-rice', 3);

-- Insert breakfast recipes (Pancakes & Waffles - category_id 6)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Classic Pancakes', 'Fluffy buttermilk pancakes', 'Mix dry ingredients, combine with wet ingredients, cook on griddle', '{"flour": "2 cups", "milk": "1.5 cups", "eggs": 2, "butter": "4 tbsp"}', 290, 20, 4, 6, 'classic-pancakes', 3),
('Belgian Waffles', 'Crispy Belgian-style waffles', 'Prepare batter, cook in waffle iron until golden', '{"flour": "2 cups", "eggs": 3, "milk": "1.5 cups", "sugar": "2 tbsp"}', 310, 25, 4, 6, 'belgian-waffles', 3);

-- Insert breakfast recipes (Smoothies - category_id 7)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Strawberry Smoothie', 'Fresh strawberry and yogurt smoothie', 'Blend strawberries, yogurt, and milk until smooth', '{"strawberries": "1 cup", "yogurt": "1 cup", "milk": "1/2 cup"}', 150, 5, 2, 7, 'strawberry-smoothie', 3),
('Green Smoothie', 'Healthy green smoothie with spinach', 'Blend spinach, banana, mango, and coconut milk', '{"spinach": "2 cups", "banana": 1, "mango": 1, "coconut_milk": "1 cup"}', 180, 5, 2, 7, 'green-smoothie', 3);

-- Insert lunch recipes (Salads - category_id 8)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Caesar Salad', 'Classic Caesar with romaine and parmesan', 'Toss lettuce with dressing, top with croutons and cheese', '{"romaine": "4 cups", "parmesan": "1/2 cup", "croutons": "1 cup", "dressing": "1/2 cup"}', 220, 10, 2, 8, 'caesar-salad', 3),
('Greek Salad', 'Fresh Greek salad with feta', 'Combine tomatoes, cucumber, olives, feta, and dressing', '{"tomatoes": 2, "cucumber": 1, "feta": "1 cup", "olives": "1/2 cup"}', 180, 10, 2, 8, 'greek-salad', 3),
('Caprese Salad', 'Tomato, mozzarella, and basil salad', 'Layer tomatoes and mozzarella, drizzle with olive oil and vinegar', '{"tomatoes": 2, "mozzarella": "8 oz", "basil": "1/4 cup", "olive_oil": "2 tbsp"}', 240, 5, 2, 8, 'caprese-salad', 3),
('Quinoa Salad', 'Protein-packed quinoa salad', 'Cook quinoa, mix with vegetables and vinaigrette', '{"quinoa": "1 cup", "bell_peppers": 2, "cucumbers": 1, "vinaigrette": "1/3 cup"}', 280, 20, 3, 8, 'quinoa-salad', 3);

-- Insert lunch recipes (Sandwiches - category_id 9)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Club Sandwich', 'Triple-decker club with bacon and turkey', 'Layer turkey, bacon, lettuce, tomato on toasted bread', '{"bread": "3 slices", "turkey": "6 oz", "bacon": "4 slices", "lettuce": 1, "tomato": 1}', 450, 10, 1, 9, 'club-sandwich', 3),
('Grilled Cheese', 'Classic melted cheese sandwich', 'Butter bread, add cheese, grill until golden', '{"bread": "2 slices", "cheddar": "2 slices", "butter": "1 tbsp"}', 320, 8, 1, 9, 'grilled-cheese', 3),
('Caprese Panini', 'Pressed mozzarella and tomato sandwich', 'Layer mozzarella, tomato, basil, grill in panini press', '{"bread": "2 slices", "mozzarella": "4 oz", "tomato": 1, "basil": "3 leaves"}', 380, 10, 1, 9, 'caprese-panini', 3);

-- Insert lunch recipes (Pasta - category_id 10)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Cacio e Pepe', 'Creamy pecorino and black pepper pasta', 'Cook pasta, toss with pecorino cheese and black pepper', '{"pasta": "1 lb", "pecorino": "1 cup", "black_pepper": "2 tbsp"}', 420, 20, 4, 10, 'cacio-e-pepe', 3),
('Penne Arrabbiata', 'Spicy tomato and garlic pasta', 'Cook penne, toss with spicy tomato sauce', '{"penne": "1 lb", "tomatoes": "28 oz", "garlic": 4, "red_pepper": "1 tsp"}', 380, 25, 4, 10, 'penne-arrabbiata', 3),
('Fettuccine Alfredo', 'Rich and creamy Alfredo sauce', 'Cook fettuccine, toss with butter, cream, and parmesan', '{"fettuccine": "1 lb", "butter": "1 cup", "cream": "1 cup", "parmesan": "1.5 cups"}', 520, 20, 4, 10, 'fettuccine-alfredo', 3),
('Pasta Primavera', 'Pasta with fresh spring vegetables', 'Cook pasta, toss with sautéed vegetables and olive oil', '{"pasta": "1 lb", "zucchini": 1, "asparagus": "1 bunch", "carrots": 2, "olive_oil": "1/4 cup"}', 340, 25, 4, 10, 'pasta-primavera', 3);

-- Insert dinner recipes (Pork - category_id 11)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Grilled Pork Chops', 'Seasoned and grilled pork chops', 'Season chops, grill over medium-high heat until cooked through', '{"pork_chops": "2 lbs", "garlic": 3, "olive_oil": "2 tbsp", "herbs": "to taste"}', 380, 20, 4, 11, 'grilled-pork-chops', 3),
('Pulled Pork', 'Slow-cooked pulled pork', 'Slow cook pork shoulder until tender, shred and mix with sauce', '{"pork_shoulder": "4 lbs", "bbq_sauce": "1 cup", "spices": "to taste"}', 420, 480, 8, 11, 'pulled-pork', 3),
('Pork Stir-Fry', 'Quick and easy pork stir-fry', 'Slice pork, stir-fry with vegetables and sauce', '{"pork": "1 lb", "broccoli": 1, "bell_peppers": 2, "soy_sauce": "1/4 cup"}', 340, 25, 4, 11, 'pork-stir-fry', 3),
('Pork Schnitzel', 'Breaded and fried pork cutlets', 'Pound thin, bread, and fry until golden', '{"pork_loin": "1 lb", "breadcrumbs": "1 cup", "eggs": 2, "oil": "1 cup"}', 450, 25, 4, 11, 'pork-schnitzel', 3);

-- Insert dinner recipes (Chicken - category_id 12)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Roasted Chicken', 'Whole roasted chicken with herbs', 'Season chicken, roast in oven until golden and cooked through', '{"whole_chicken": "5 lbs", "rosemary": "3 sprigs", "lemon": 1, "olive_oil": "3 tbsp"}', 520, 90, 6, 12, 'roasted-chicken', 3),
('Chicken Piccata', 'Lemony chicken with capers', 'Pan-fry breaded chicken, top with lemon caper sauce', '{"chicken_breasts": "4", "capers": "1/4 cup", "lemon": 2, "butter": "3 tbsp"}', 300, 20, 4, 12, 'chicken-piccata', 3),
('Thai Basil Chicken', 'Spicy Thai stir-fry', 'Stir-fry chicken with basil, chilies, and fish sauce', '{"chicken": "1.5 lbs", "thai_basil": "1 cup", "chilies": 3, "fish_sauce": "2 tbsp"}', 380, 25, 4, 12, 'thai-basil-chicken', 3);

-- Insert dinner recipes (Fish - category_id 13)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Baked Salmon', 'Herb-baked salmon fillet', 'Season salmon, bake with lemon and herbs', '{"salmon_fillets": "4", "lemon": 2, "dill": "2 tbsp", "olive_oil": "2 tbsp"}', 380, 25, 4, 13, 'baked-salmon', 3),
('Fish Tacos', 'Crispy fish tacos with slaw', 'Fry fish, serve in tortillas with cabbage slaw', '{"white_fish": "1 lb", "tortillas": 8, "cabbage": "2 cups", "lime": 2}', 320, 20, 4, 13, 'fish-tacos', 3),
('Cod en Papillote', 'Steamed cod in parchment paper', 'Wrap cod with vegetables in parchment, steam until tender', '{"cod_fillets": "4", "zucchini": 1, "tomatoes": 2, "herbs": "to taste"}', 280, 30, 4, 13, 'cod-en-papillote', 3),
('Tuna Steak', 'Seared tuna with soy glaze', 'Sear tuna quickly, finish with soy glaze', '{"tuna_steaks": "4", "soy_sauce": "1/4 cup", "ginger": "1 tbsp", "sesame_oil": "1 tbsp"}', 360, 15, 4, 13, 'tuna-steak', 3);

-- Insert dinner recipes (Vegetarian - category_id 14)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Veggie Stir-Fry', 'Mixed vegetable stir-fry', 'Stir-fry assorted vegetables with tofu and sauce', '{"tofu": "1 block", "broccoli": 1, "snap_peas": "2 cups", "soy_sauce": "1/4 cup"}', 260, 20, 4, 14, 'veggie-stir-fry', 3),
('Stuffed Bell Peppers', 'Peppers filled with rice and vegetables', 'Hollow peppers, fill with rice mixture, bake', '{"bell_peppers": 4, "rice": "2 cups", "tomatoes": 2, "cheese": "1 cup"}', 280, 40, 4, 14, 'stuffed-bell-peppers', 3),
('Mushroom Risotto', 'Creamy mushroom and arborio rice', 'Cook arborio rice with stock, add mushrooms and cheese', '{"arborio_rice": "2 cups", "mushrooms": "1 lb", "stock": "6 cups", "parmesan": "1 cup"}', 420, 45, 4, 14, 'mushroom-risotto', 3);

-- Insert dessert recipes (Cakes - category_id 15)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Chocolate Cake', 'Rich and moist chocolate cake', 'Mix dry ingredients, combine with wet, bake at 350F', '{"flour": "2 cups", "cocoa": "3/4 cup", "eggs": 3, "butter": "1 cup"}', 380, 40, 12, 15, 'chocolate-cake', 3),
('Vanilla Cake', 'Classic vanilla layer cake', 'Cream butter and sugar, add flour and milk, bake', '{"flour": "3 cups", "butter": "1 cup", "sugar": "2 cups", "eggs": 3}', 360, 40, 12, 15, 'vanilla-cake', 3),
('Carrot Cake', 'Moist carrot cake with cream cheese frosting', 'Blend carrots into batter, bake, frost with cream cheese', '{"flour": "2 cups", "carrots": "2 cups", "sugar": "1.5 cups", "oil": "1 cup"}', 420, 50, 12, 15, 'carrot-cake', 3),
('Strawberry Shortcake', 'Fluffy sponge with fresh strawberries', 'Layer sponge cake, whipped cream, and strawberries', '{"flour": "2 cups", "eggs": 4, "sugar": "1 cup", "strawberries": "2 lbs"}', 340, 35, 8, 15, 'strawberry-shortcake', 3);

-- Insert dessert recipes (Cookies - category_id 16)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Chocolate Chip Cookies', 'Classic chocolate chip cookies', 'Cream butter and sugar, add flour and chips, bake', '{"flour": "2.25 cups", "butter": "1 cup", "sugar": "3/4 cup", "chocolate_chips": "2 cups"}', 280, 25, 24, 16, 'chocolate-chip-cookies', 3),
('Oatmeal Cookies', 'Chewy oatmeal raisin cookies', 'Mix dry ingredients, combine with wet, add oats and raisins', '{"flour": "1.5 cups", "oats": "3 cups", "raisins": "1 cup", "butter": "1 cup"}', 240, 20, 20, 16, 'oatmeal-cookies', 3),
('Sugar Cookies', 'Soft and buttery sugar cookies', 'Roll dough, cut shapes, decorate and bake', '{"flour": "3 cups", "butter": "1 cup", "sugar": "1.5 cups", "vanilla": "1 tsp"}', 220, 30, 24, 16, 'sugar-cookies', 3);

-- Insert dessert recipes (Chocolate - category_id 17)
INSERT INTO recipe (name, description, instructions, ingredients, calories, prep_time, servings, category_id, slug, author_id) VALUES
('Chocolate Mousse', 'Light and airy chocolate mousse', 'Melt chocolate, fold in whipped cream and egg whites', '{"chocolate": "8 oz", "cream": "1 cup", "eggs": 3, "sugar": "1/4 cup"}', 320, 15, 4, 17, 'chocolate-mousse', 3),
('Brownies', 'Fudgy chocolate brownies', 'Mix chocolate mixture with flour, bake until gooey', '{"chocolate": "8 oz", "butter": "1 cup", "flour": "1 cup", "sugar": "1.5 cups"}', 380, 35, 16, 17, 'brownies', 3),
('Chocolate Lava Cake', 'Warm chocolate cake with molten center', 'Bake until edges are set but center is soft', '{"chocolate": "6 oz", "butter": "6 oz", "eggs": 2, "sugar": "1/4 cup"}', 420, 20, 2, 17, 'chocolate-lava-cake', 3);

-- Insert comments for some recipes
INSERT INTO "user" (id, email, username, password, role) VALUES
(1, "john@gmail.com", 'john_doe', 'hashed_password', 'USER'),
(2, "jane@gmail.com", 'jane_smith', 'hashed_password', 'USER'),
(3, "chef_mike@gmail.com", 'chef_mike', 'hashed_password', 'ADMIN'),
(4, "admin@admin.com", 'admin', '$2b$12$LKrBcPdYJ0kGqPj.hOw3vumrh89vs9Az7r6b0KVE08bt.cdOOQrCe', 'ADMIN');

INSERT INTO comment (title, text, rating, user_id, recipe_id) VALUES
('Delicious!', 'These eggs are the perfect breakfast', 5.0, 1, 1),
('Easy to make', 'Great recipe, followed the instructions perfectly', 5.0, 2, 2),
('Too rich', 'Good flavor but very heavy for lunch', 3.0, 3, 28),
('Family favorite', 'Everyone loved these pancakes, making them again tomorrow', 5.0, 1, 7),
('Perfect salmon', 'Moist and flaky, restaurant quality', 5.0, 2, 33),
('Not bad', 'Decent risotto but took longer than expected', 4.0, 3, 40),
('Amazing!', 'Best chocolate cake I have ever made', 5.0, 1, 42),
('Kids loved it', 'These cookies disappeared fast', 5.0, 2, 48),
('Needs seasoning', 'Good base recipe but add more salt and pepper', 3.5, 3, 16);
