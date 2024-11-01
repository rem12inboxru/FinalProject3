import requests
from sqlalchemy.orm import sessionmaker
from .models import DataSQLA, engine
from django.shortcuts import render
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep, time
import matplotlib.pyplot as plt

Session = sessionmaker(bind=engine)


def parser(x, y):
    url = 'https://coinmarketcap.com/currencies/bitcoin/'
    k = 0
    data_two = []
    while k <= y:
        ticker = 'BTC'
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'lxml')
        price_btc = bs.find('span', 'sc-65e7f566-0 WXGwg base-text')
        btc = float(price_btc.text[1:].replace(',', ''))
        dataevent = datetime.now()
        print(dataevent)
        data_one = [ticker, btc, x, dataevent]
        print(data_one)
        data_two.append(data_one)
        sleep(x * 60)
        k+=1
    print(data_two)
    return data_two


def render_up(request):
    if request.method == 'POST':
        timeframe = request.POST.get("timeframe")
        number_req = request.POST.get("number_req")
        session = Session()
        for i in parser(int(timeframe), int(number_req)):
            datasqla = DataSQLA(ticker= i[0], lastprice=i[1], timeframe=i[2], dataevent=i[3])
            session.add(datasqla)
            session.commit()
        session.close()
    return render(request, 'render_up.html')

def render_calc(request):
    context = {}
    session = Session()
    lastprices = []
    dateevents = []
    y1 = time()
    data = session.query(DataSQLA).all()
    for i in data:
        lastprices.append(i.lastprice)
        dateevents.append(i.dataevent)
    y2 = time()
    y = y2 - y1       # время извлечения всех элементов
    z1 = time()
    data1 = session.query(DataSQLA).get(1)
    z2 = time()
    z = z2 - z1        # время извлечения одного элемента
    a1 = time()
    data2 = session.query(DataSQLA).filter(DataSQLA.lastprice <= 68).all()
    a2 = time()
    a = a2 - a1        # время извлечения всех элементов по фильтру
    b1 = time()
    session.query(DataSQLA).delete()
    b2 = time()
    b = b2 - b1         # время удаления всех элементов
    session.commit()
    session.close()
    context = {'y': y, 'z': z, 'a': a, 'b': b }
    plt.plot(dateevents, lastprices)
    plt.show()
    plt.savefig('static/plot.jpg', format='jpg')

    return render(request, 'render_calc.html', context)

def render_pausa(request):
    return render(request, 'render_pausa.html')




# Create your views here.
