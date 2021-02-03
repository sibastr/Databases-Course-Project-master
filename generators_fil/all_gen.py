from random import choice, randint, shuffle
import os
import cv2


class Product:
	def __init__(self, id, name, category, color, cost, description, image, displayed, in_stock, on_sale, discount):
		self.id = id
		self.name = name
		self.category = category
		self.color = color
		self.cost = cost
		self.description = description
		self.image = image
		self.displayed = displayed
		self.in_stock = in_stock
		self.on_sale = on_sale
		self.discount = discount


class FeatureSet:
	def __init__(self, id, product, feature_variant):
		self.id = id
		self.product = product
		self.feature_variant = feature_variant




def get_name_pool(filename):
	names = []

	with open(filename, "r", encoding="utf-8") as f:
		for line in f:
			word = line[:-1]
			names.append(word.lower())

	return names


names = get_name_pool('swe_nouns.txt')
shuffle(names)
color_d = {
	1: 1,
	2: 2,
	3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7
}
products = []
feature_sets = []


def get_name(names_d, id):
        abc = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        name = ""
        name += names_d[id]
        name += " "
        n = randint(6, 8)
        
        for i in range(n):
                name += abc[randint(0, len(abc) - 1)]

        return name


def tv_generator(first_prod_id, first_set_id, n):
	images = [f for f in os.listdir(os.path.join('images', 'TVs'))]
	img_len = len(images)

	maker_var_d = {
		1 : 7,
		2 : 8,
		3 : 9,
		4 : 10
	}
	maker_names = {
                1 : 'Samsung',
                2 : 'LG',
                3 : 'Sony',
                4 : 'Philips'
        }

	for id in range(first_prod_id, first_prod_id + n, 1):
		image_f = images[id % img_len]
		color = image_f[0:image_f.find('-')]
		var = image_f[len(color) + 1:image_f[len(color) + 1:].find('-') + len(color) + 1]

		if randint(0, 100) > 94:
			in_stock = 0
		else:
			in_stock = 1
		if in_stock:
			if randint(0, 100) > 70:
				on_sale = 1
				discount = int(randint(1, 3) * 10)
			else:
				on_sale = 0
				discount = 0
		else:
			on_sale = 0
			discount = 0

		image_name = str(randint(0, 1000000)) + '_' + image_f
		img = cv2.imread(os.path.join('images', 'TVs', image_f))
		base = os.path.split(os.getcwd())[0]
		cv2.imwrite(os.path.join(base, 'shop_v4', 'media', 'product_pics', image_name), img)

		product = Product(
			id=id,
			name=get_name(maker_names, int(var)),
			category=1,
			color=color_d[int(color)],
			cost=int(randint(15, 100) * 1000 - 1),
			description="",
			image='product_pics/' + image_name,
			displayed=1,
			in_stock=in_stock,
			on_sale=on_sale,
			discount=discount
		)
		products.append(product)
                #Производитель
		feature_set = FeatureSet(
			id=first_set_id,
			product=id,
			feature_variant=maker_var_d[int(var)]
		)
		feature_sets.append(feature_set)
		feature_set = FeatureSet(
			id=first_set_id + 1,
			product=id,
			feature_variant=randint(1, 3)
		)
		feature_sets.append(feature_set)
		feature_set = FeatureSet(
			id=first_set_id + 2,
			product=id,
			feature_variant=randint(4, 6)
		)
		first_set_id += 3
		feature_sets.append(feature_set)

	return first_prod_id + n, first_set_id


def player_generator(first_prod_id, first_set_id, n):
	shuffle(names)
	images = [f for f in os.listdir(os.path.join('images', 'Players'))]
	img_len = len(images)

	maker_var_d = {
		1 : 16,
		2 : 17,
		3 : 18,
		4 : 19
	}

	maker_names = {
                1 : 'Ritmix',
                2 : 'Sony',
                3 : 'Digma',
                4 : 'FiiO'
        }

	for id in range(first_prod_id, first_prod_id + n, 1):
		image_f = images[id % img_len]
		color = image_f[0:image_f.find('-')]
		var = image_f[len(color) + 1:image_f[len(color) + 1:].find('-') + len(color) + 1]

		if randint(0, 100) > 94:
			in_stock = 0
		else:
			in_stock = 1
		if in_stock:
			if randint(0, 100) > 70:
				on_sale = 1
				discount = int(randint(1, 3) * 10)
			else:
				on_sale = 0
				discount = 0
		else:
			on_sale = 0
			discount = 0

		image_name = str(randint(0, 1000000)) + '_' + image_f
		img = cv2.imread(os.path.join('images', 'players', image_f))
		base = os.path.split(os.getcwd())[0]
		cv2.imwrite(os.path.join(base, 'shop_v4', 'media', 'product_pics', image_name), img)

		product = Product(
			id=id,
			name=get_name(maker_names, int(var)),
			category=2,
			color=color_d[int(color)],
			cost=int(randint(20, 45) * 100 - 1),
			description="",
			image='product_pics/' + image_name,
			displayed=1,
			in_stock=in_stock,
			on_sale=on_sale,
			discount=discount
		)
		products.append(product)

		feature_set = FeatureSet(
			id=first_set_id,
			product=id,
			feature_variant=maker_var_d[int(var)]
		)
		feature_sets.append(feature_set)
		feature_set = FeatureSet(
			id=first_set_id + 1,
			product=id,
			feature_variant=randint(11, 15)
               )
		first_set_id += 2
		feature_sets.append(feature_set)

	return first_prod_id + n, first_set_id


def mice_generator(first_prod_id, first_set_id, n):
	shuffle(names)
	images = [f for f in os.listdir(os.path.join('images', 'Mice'))]
	img_len = len(images)

	maker_var_d = {
		1 : 22,
		2 : 23,
		3 : 24,
		4 : 25,
                5 : 26,
                6 : 27
	}
	maker_names = {
                1 : 'Logitech',
                2 : 'A4Tech',
                3 : 'HP',
                4 : 'Razer',
                5 : 'Genius',
                6 : 'Microsoft'
        }

	for id in range(first_prod_id, first_prod_id + n, 1):
		image_f = images[id % img_len]
		color = image_f[0:image_f.find('-')]
		var = image_f[len(color) + 1:image_f[len(color) + 1:].find('-') + len(color) + 1]

		if randint(0, 100) > 94:
			in_stock = 0
		else:
			in_stock = 1
		if in_stock:
			if randint(0, 100) > 70:
				on_sale = 1
				discount = int(randint(1, 3) * 10)
			else:
				on_sale = 0
				discount = 0
		else:
			on_sale = 0
			discount = 0

		image_name = str(randint(0, 1000000)) + '_' + image_f
		img = cv2.imread(os.path.join('images', 'Mice', image_f))
		base = os.path.split(os.getcwd())[0]
		cv2.imwrite(os.path.join(base, 'shop_v4', 'media', 'product_pics', image_name), img)

		product = Product(
			id=id,
			name=get_name(maker_names, int(var)),
			category=3,
			color=color_d[int(color)],
			cost=int(randint(5, 30) * 100 - 1),
			description="",
			image='product_pics/' + image_name,
			displayed=1,
			in_stock=in_stock,
			on_sale=on_sale,
			discount=discount
		)
		products.append(product)

		feature_set = FeatureSet(
			id=first_set_id,
			product=id,
			feature_variant=maker_var_d[int(var)]
		)
		feature_sets.append(feature_set)
		feature_set = FeatureSet(
			id=first_set_id + 1,
			product=id,
			feature_variant=randint(20, 21)
               )
		first_set_id += 2
		feature_sets.append(feature_set)

	return first_prod_id + n, first_set_id


# зеркальные(да, нет)
# назначение(Гардероб, Купе, Детский)
# угловой(да, нет)
# [цвет]-[0,1]-[1(гард), 2(купе), 3(детск)]-[0,1]
def keyboard_generator(first_prod_id, first_set_id, n):
	shuffle(names)
	images = [f for f in os.listdir(os.path.join('images', 'Keyboards'))]
	img_len = len(images)

	maker_var_d = {
		1 : 30,
		2 : 31,
		3 : 32,
		4 : 33,
                5 : 34,
                6 : 35
	}
	maker_names = {
                1 : 'Logitech',
                2 : 'A4Tech',
                3 : 'HP',
                4 : 'Razer',
                5 : 'Genius',
                6 : 'Microsoft'
        }

	

	for id in range(first_prod_id, first_prod_id + n, 1):
		image_f = images[id % img_len]
		color = image_f[0:image_f.find('-')]
		var = image_f[len(color) + 1:image_f[len(color) + 1:].find('-') + len(color) + 1]
		#print(image_f)

		if randint(0, 100) > 94:
			in_stock = 0
		else:
			in_stock = 1
		if in_stock:
			if randint(0, 100) > 70:
				on_sale = 1
				discount = int(randint(1, 3) * 10)
			else:
				on_sale = 0
				discount = 0
		else:
			on_sale = 0
			discount = 0

		image_name = str(randint(0, 1000000)) + '_' + image_f
		img = cv2.imread(os.path.join('images', 'Keyboards', image_f))
		base = os.path.split(os.getcwd())[0]
		cv2.imwrite(os.path.join(base, 'shop_v4', 'media', 'product_pics', image_name), img)

		product = Product(
			id=id,
			name=get_name(maker_names, int(var)),
			category=4,
			color=color_d[int(color)],
			cost=int(randint(10, 35) * 100 - 1),
			description="",
			image='product_pics/' + image_name,
			displayed=1,
			in_stock=in_stock,
			on_sale=on_sale,
			discount=discount
		)
		products.append(product)

		feature_set = FeatureSet(
			id=first_set_id,
			product=id,
                        feature_variant=maker_var_d[int(var)]
		)
		feature_sets.append(feature_set)
		feature_set = FeatureSet(
			id=first_set_id+1,
			product=id,
                        feature_variant=randint(28, 29)
		)
		feature_sets.append(feature_set)
		first_set_id += 2
		"""feature_sets.append(feature_set)
		feature_set = FeatureSet(
			id=first_set_id + 1,
			product=id,
			feature_variant=cat_d[int(cat)]
		)
		feature_sets.append(feature_set)
		feature_set = FeatureSet(
			id=first_set_id + 2,
			product=id,
			feature_variant=ang_d[int(angle)]
		)
		feature_sets.append(feature_set)

		first_set_id += 3"""

	return first_prod_id + n, first_set_id


def printers_generator(first_prod_id, first_set_id, n):
	shuffle(names)
	images = [f for f in os.listdir(os.path.join('images', 'Printers'))]
	img_len = len(images)

	maker_var_d = {
		1 : 38,
		2 : 39,
		3 : 40,
		4 : 41,
                5 : 42
                
	}
	maker_names = {
                1 : 'HP',
                2 : 'Canon',
                3 : 'Epson',
                4 : 'Xerox',
                5 : 'Brother'
        }


	for id in range(first_prod_id, first_prod_id + n, 1):
		image_f = images[id % img_len]
		color = image_f[0:image_f.find('-')]
		var = image_f[len(color) + 1:image_f[len(color) + 1:].find('-') + len(color) + 1]
		if randint(0, 100) > 94:
			in_stock = 0
		else:
			in_stock = 1
		if in_stock:
			if randint(0, 100) > 70:
				on_sale = 1
				discount = int(randint(1, 3) * 10)
			else:
				on_sale = 0
				discount = 0
		else:
			on_sale = 0
			discount = 0

		image_name = str(randint(0, 1000000)) + '_' + image_f
		img = cv2.imread(os.path.join('images', 'Printers', image_f))
		base = os.path.split(os.getcwd())[0]
		cv2.imwrite(os.path.join(base, 'shop_v4', 'media', 'product_pics', image_name), img)

		product = Product(
			id=id,
			name=get_name(maker_names, int(var)),
			category=5,
			color=color_d[int(color)],
			cost=int(randint(50, 160) * 100 - 1),
			description="",
			image='product_pics/' + image_name,
			displayed=1,
			in_stock=in_stock,
			on_sale=on_sale,
			discount=discount
		)
		products.append(product)
		feature_set = FeatureSet( id = first_set_id, product = id, feature_variant = maker_var_d[int(var)])
		feature_sets.append(feature_set)
		feature_set = FeatureSet(
			id=first_set_id+1,
			product=id,
                        feature_variant=randint(36, 37)
		)
		feature_sets.append(feature_set)
		first_set_id += 2
                
	return first_prod_id + n, first_set_id





def csv_output_product(fname):
	with open(fname, 'w', encoding='utf8') as f:
		for p in products:
			line = f'{p.id};{p.name};{p.category};{p.color};{p.description};{p.image};{p.discount};{p.displayed};{p.in_stock};{p.on_sale};{p.cost}\n'
			f.write(line)


def csv_output_feature_set(fname):
	with open(fname, 'w', encoding='utf8') as f:
		for fs in feature_sets:
			line = f'{fs.id};{fs.feature_variant};{fs.product}\n'
			f.write(line)


def generate_all():
	cur_p_id = 0
	cur_set_id = 0

	cur_p_id, cur_set_id = tv_generator(cur_p_id, cur_set_id, 50)
	cur_p_id, cur_set_id = player_generator(cur_p_id, cur_set_id, 50)
	cur_p_id, cur_set_id = mice_generator(cur_p_id, cur_set_id, 50)
	cur_p_id, cur_set_id = keyboard_generator(cur_p_id, cur_set_id, 50)
	cur_p_id, cur_set_id = printers_generator(cur_p_id, cur_set_id, 50)

	csv_output_product('product.csv')
	csv_output_feature_set('feature_set.csv')

generate_all()
