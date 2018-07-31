from datetime import datetime

from flask import (Flask, render_template, request, redirect, url_for, flash)

app = Flask(__name__)
app.secret_key = '4gdff25EYE33";"№%'

products = [
    {
        'image' : '/static/image/dodo.jpg',
        'name' : 'Додо',
        'description' : 'Ветчина, говядина (фарш), пикантная пепперони, томатный соус, шампиньоны, сладкий перец, лук красный, моцарелла и маслины.',
        'price' : '385'
    },
    {
        'image' : '/static/image/italian.jpg',
        'name' : 'Итальянская',
        'description' : 'Пикантная пепперони, томатный соус, шампиньоны, моцарелла, маслины и орегано.',
        'price' : '375'
    },
    {
        'image' : '/static/image/mexican.jpg',
        'name' : 'Мексиканская',
        'description' : 'Цыпленок, томатный соус, шампиньоны, сладкий перец, лук красный, моцарелла, острый перец халапеньо и томаты.',
        'price' : '375'
    },
    {
        'image' : '/static/image/pepperoni.jpg',
        'name' : 'Пеперони',
        'description' : 'Пикантная пепперони, томатный соус и моцарелла.',
        'price' : '375'
    },
    {
        'image' : '/static/image/supermeat.jpg',
        'name' : 'Супермясная',
        'description' : 'Цыпленок, говядина (фарш), пикантная пепперони, томатный соус, острая чоризо, моцарелла и бекон.',
        'price' : '395'
    },
]

orders = {}
num = 0
order_ok = False

@app.route('/')
def index():
    return render_template('products.html', products = products)

@app.route('/make_order/', methods = ['POST', 'GET'])
def order():
    if request.method == 'POST':

        order = {

            'client' : {
                'name': request.form['name'],
                'surname': request.form['surname'],
                'adress': request.form['adress'],
                'phone': request.form['phone']
            },
            'pizza' : {},
            'status' : {'Поступил' : datetime.now()}
        }

        global order_ok

        if request.form.get('Додо'):
            value = request.form['value_Додо']
            order['pizza'].update({'Додо' : value})
            order_ok = True

        if request.form.get('Итальянская'):
            value = request.form['value_Итальянская']
            order['pizza'].update({'Итальянская' : value})
            order_ok = True

        if request.form.get('Мексиканская'):
            value = request.form['value_Мексиканская']
            order['pizza'].update({'Мексиканская' : value})
            order_ok = True

        if request.form.get('Пеперони'):
            value = request.form['value_Пеперони']
            order['pizza'].update({'Пеперони' : value})
            order_ok = True

        if request.form.get('Супермясная'):
            value = request.form['value_Супермясная']
            order['pizza'].update({'Супермясная' : value})
            order_ok = True

        if order_ok:
            if (request.form['name'] == '') or (request.form['surname'] == '') or (request.form['adress'] == '') or (request.form['phone'] == ''):
                flash('Заполните все данные в форме заказа. И повторите выбор пиццы')
                order_ok = False
                return render_template('make_order.html', products=products)
            else:
                global num
                num = num + 1
                orders.update({num : order})
                flash('{}, Ваш заказ принят. Менеджер перезвонит на номер {}.'.format(order['client']['name'], order['client']['phone']))
                order_ok = False
                return redirect(url_for('index'))
        else:
            flash('Необходимо выбрать пиццу для заказа.')
            return render_template('make_order.html', products=products)
    else:
        return render_template('make_order.html', products = products)

@app.route('/orders/', methods = ['POST', 'GET'])
def orders_list():
    if request.method == 'POST':
        for num in orders.keys():
            splitted_status = request.form.get('select_status').split("-")
            if splitted_status[0] == str(num):
                orders[num]['status'].clear()
                orders[num]['status'] = {splitted_status[1] : datetime.now()}

        #return redirect(url_for('index'))
        return render_template('orders.html', orders=orders)
    else:
        return render_template('orders.html', orders = orders)

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')