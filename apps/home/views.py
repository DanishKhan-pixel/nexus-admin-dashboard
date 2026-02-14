# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template, shortcuts
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.authentication.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bussiness,PriceHistory,Stock,Listings
import yfinance as yf
import datetime
import pandas as pd
import secrets
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import pandas_datareader as data 
from sklearn.preprocessing import MinMaxScaler
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from keras.models import load_model    
import string
from psx import stocks, tickers
from keras.initializers import Orthogonal
from keras.models import Sequential
from keras.layers import Dense, Reshape
# To be Changed
model_path=r"apps\home\keras_model.h5"
# Landing Page
def landing_page(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('landing/index.html')
    return HttpResponse(html_template.render(context, request))
def listings(request):
    tickerss = tickers()
    stock_data = []
    for index, row in tickerss.iterrows():
        ticker_data = {
            'symbol': row['symbol'],
            'name': row['name'],
            'sectorName': row['sectorName'],
            'isETF': row['isETF'],
            'isDebt': row['isDebt'],
            'isGEM': row['isGEM']
        }
        stock_data.append(ticker_data)
    # for index, row in tickerss.iterrows():
    #     ticker = row['symbol']
    #     sector = row['sectorName']
    #     Listings.objects.create(ticker=ticker, sector=sector)
        # context = {
        #     'segment': 'listings',
        #     'stock_data': stock_data
        # }
    unique_sectors = set(data['sectorName'] for data in stock_data)
    
    context = {
        'segment': 'listings',
        'stock_data': stock_data,
        'unique_sectors': unique_sectors
    }
    # AI MODEL
    user=request.user
    
 
    if user.is_authenticated:
        if user.is_admin:
            return render(request, 'landing/listings.html', context)
        elif user.is_ent:
            return render(request, 'entSide/landing/listings.html', context)
        elif user.is_investor:
            return render(request, 'invnSide/landing/listings.html', context)
        else:
            return render(request, 'home/landing/listings.html', context)
    else:
        return render(request, 'landing/listings.html', context)
def viewlistingDetails(request, symbol):
    stock = stocks(symbol, start=datetime.date(2020, 1, 1), end=datetime.date.today())
    # print(stock)
    yesterday = datetime.date.today() - datetime.timedelta(days=7)
    sdata_dict = stocks(symbol, start=yesterday, end=datetime.date.today())
    # print(sdata_dict)
    # print("XXXXXXXXx")
    open = sdata_dict.iloc[-1]['Open']
    high = sdata_dict.iloc[-1]['High']
    low = sdata_dict.iloc[-1]['Low']
    close = sdata_dict.iloc[-1]['Close']
    context = {
        'segment': 'listings',
        'stock': stock,
        'symbol': symbol,
        'open': open,
        'high': high,
        'low': low,
        'close': close,
    }
    user=request.user
    if user.is_authenticated:
        if user.is_admin:
            return render(request, 'landing/listings_detail.html', context)
        elif user.is_ent:
            return render(request, 'entSide/landing/listings_detail.html', context)
        else:
            return render(request, 'invnSide/landing/listings_detail.html', context)
    else:  
        return render(request, 'landing/listings_detail.html', context)
# Admin Views
@login_required(login_url="/login/")
def index(request):
    bids=Stock.objects.count()
    context = {'segment': 'index','bids':bids}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
def admin_profile(request):
    if request.method == 'POST':
        user_id=request.user.id
        fnmae=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        address=request.POST.get('address')
        city=request.POST.get('city')
        country=request.POST.get('country')
        zip=request.POST.get('postal')
        bio=request.POST.get('bio')
        User.objects.filter(id=user_id).update(first_name=fnmae,last_name=lname,email=email,address=address,city=city,country=country,zip=zip,bio=bio)
        return redirect('admin_profile')
    else: 
        user_id=request.user.id
        current_user = get_object_or_404(User, id=user_id)
        context = {'segment': 'admin_profile'}
        return render(request, 'home/page-user.html', {'current_user':current_user, **context})

def all_bids(request):
    stocks=Stock.objects.all()
    context = {'segment': 'bids', 'stocks': stocks}
    return render(request, 'home/bids.html', context)

    
def users(request):
    users=User.objects.filter(is_verified=True)
    context = {'segment': 'users'}
    return render(request, 'home/user_lists.html',{'users':users, **context})
def user_profile(request,id):
    current_user = get_object_or_404(User, id=id)
    context = {'segment': 'user_profile'}
    return render(request, 'home/page-user.html', {'current_user':current_user, **context})
def delete_user(request,user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    users = User.objects.all()
    context = {'segment': 'users'}
    return render(request, 'home/user_lists.html', {'users': users, **context})
def verfications(request):
    users=User.objects.filter(is_verified=False)
    context = {'segment': 'verfications'}
    return render(request, 'home/verify.html', {'users':users, **context})
def sch_meet(request,id):
    user_id=request.user.id
    if request.method == 'POST':
        date=request.POST.get('date')
        link=request.POST.get('link')
        User.objects.filter(id=user_id).update(int_date=date,int_link=link)
        return redirect('admin_profile')
    else:
        current_user = get_object_or_404(User, id=id)
        return render(request, 'home/sch.html', {'current_user':current_user})
    # user.is_verified=True
    # user.save()
    # return redirect('verfications')
def acc(request,id):
    user = get_object_or_404(User, id=id)
    user.is_verified=True
    user.save()
    return redirect('verfications')
def rej(request,id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('verfications')

# For Ent
def ent_index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('entSide/home/page-user.html')
    return HttpResponse(html_template.render(context, request))
def ent_profile(request):
    if request.method == 'POST':
        user_id=request.user.id
        fnmae=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        address=request.POST.get('address')
        city=request.POST.get('city')
        country=request.POST.get('country')
        zip=request.POST.get('postal')
        bio=request.POST.get('bio')
        User.objects.filter(id=user_id).update(first_name=fnmae,last_name=lname,email=email,address=address,city=city,country=country,zip=zip,bio=bio)
        return redirect('ent_profile')
    else: 
        user_id=request.user.id
        current_user = get_object_or_404(User, id=user_id)
        context = {'segment': 'ent_profile'}
        return render(request, 'entSide/home/page-user.html', {'current_user':current_user, **context})
    
def ent_bussiness(request):
    user = request.user
    bussinesses = Bussiness.objects.filter(user=user)
    yesterday = datetime.date.today() - datetime.timedelta(days=7)
    stock_data = []
    for bussiness in bussinesses:
        data = stocks(bussiness.ticker, start=yesterday, end=datetime.date.today())
        last_data = data.tail(1) 
        stock_data.append({'bussiness_id': bussiness.id, 'ticker': bussiness.ticker, 'data': last_data})
    context = {'segment': 'ent_bussiness', 'stock_data': stock_data, 'bussinesses': bussinesses}
    return render(request, 'entSide/home/bussiness.html', context)

def ent_stocks(request):
    user = request.user
    bus= Bussiness.objects.filter(user=user)
    stocks=Stock.objects.filter(symbol__in=bus)
    context = {'segment': 'ent_stocks', 'stocks': stocks}
    # print(context)
    return render(request, 'entSide/home/ent_stocks.html', context)


def generate_random_link(base_url='meet.jit.si/bussinessnexus/', length=10):
    """Generate a random string of letters and digits."""
    characters = string.ascii_letters + string.digits
    random_link = ''.join(secrets.choice(characters) for _ in range(length))
    return base_url + random_link

def ent_stocks_meeting(request, id):
    if request.method == 'POST':
        description = request.POST.get('desp')
        link = generate_random_link() 
        stock = Stock.objects.filter(id=id)
        stock.update(link=link, description=description)
        return redirect('ent_stocks')
    else:
        stock = get_object_or_404(Stock, symbol=id)
        context = {'segment': 'ent_stocks_meeting'}
        return render(request, 'entSide/home/ent_stocks_meeting.html', {'stock': stock, **context})
    
def ent_stocks_meeting_acc(request,id):
    stock = get_object_or_404(Stock, symbol=id)
    stock.status = '1'
    stock.link='1'
    stock.save()
    return redirect('ent_stocks')
    
def ent_stocks_meeting_rej(request,id):
    stock= get_object_or_404(Stock, symbol=id)
    stock.status = '0'
    stock.link='2'
    stock.save()
    return redirect('ent_stocks')

def add_bussiness(request):
    user=request.user
    if user.is_verified==True:
        if request.method == 'POST':
            user_id=request.user.id
            name="N/A"
            description=request.POST.get('sector')
            location="N/A"
            contact="N/A"
            email="N/A"
            website="N/A"
            ticker=request.POST.get('ticker')
            stock_qty="0"
            price="0"
            Bussiness.objects.create(user=user,name=name,description=description,location=location,contact=contact,email=email,website=website,ticker=ticker,stocks_qty=stock_qty,price=price)
            return redirect('ent_bussiness')
        else:
            context = {'segment': 'add_bussiness'}
            return render(request, 'entSide/home/add_bussiness.html', context)
    else:
        return redirect('ent_profile')

def edit_bussiness(request,id):
    user=request.user
    old_price=Bussiness.objects.get(id=id).price
    bussiness = get_object_or_404(Bussiness, id=id)
    if request.method == 'POST':
        name="N/A"
        description=request.POST.get('ticker')
        location="N/A"
        contact="N/A"
        email="N/A"
        website="N/A"
        ticker=request.POST.get('ticker')
        stock_qty="0"
        price="0"
        Bussiness.objects.filter(id=id).update(name=name,description=description,contact=contact,email=email,website=website,ticker=ticker,stocks_qty=stock_qty,price=price)
        # if old_price!=price:
        #     PriceHistory.objects.create(bussiness=bussiness,price=price)
        # else:
        #     pass
        return redirect('ent_bussiness')
    else:
        context = {'segment': 'edit_bussiness'}
        return render(request, 'entSide/home/edit_bussiness.html', {'bussiness':bussiness,**context})
    
def delete_bussiness(request,id):
    bussiness = get_object_or_404(Bussiness, id=id)
    PriceHistory.objects.filter(bussiness=bussiness).delete()
    bussiness.delete()
    bussiness = Bussiness.objects.all()
    context = {'segment': 'ent_bussiness'}
    return render(request, 'entSide/home/bussiness.html', {'bussiness': bussiness, **context})

# For Investor
def in_index(request):
    user=request.user
    stocks=Stock.objects.filter(user=user,status='1')
    # Total Investments
    total_value = sum(stock.price * stock.quantity for stock in stocks)
    # Total Stocks
    total_stocks = sum(stock.quantity for stock in stocks)

    bids=Stock.objects.filter(user=user,status='0').count()

    context = {'segment': 'index','stocks':stocks,'total_value':total_value,'total_stocks':total_stocks,'bids':bids}
    html_template = loader.get_template('invnSide//home/index.html')
    return HttpResponse(html_template.render(context, request))

def in_profile(request):
    if request.method == 'POST':
        user_id=request.user.id
        fnmae=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        address=request.POST.get('address')
        city=request.POST.get('city')
        country=request.POST.get('country')
        zip=request.POST.get('postal')
        bio=request.POST.get('bio')
        User.objects.filter(id=user_id).update(first_name=fnmae,last_name=lname,email=email,address=address,city=city,country=country,zip=zip,bio=bio)
        return redirect('in_profile')
    else: 
        user_id=request.user.id
        current_user = get_object_or_404(User, id=user_id)
        context = {'segment': 'in_profile'}
        return render(request, 'invnSide/home/page-user.html', {'current_user':current_user, **context})

def place_bids(request):
    user=request.user
    if request.method == 'POST':
        user_id=request.user.id
        symbol=request.POST.get('symbol')
        quantity=request.POST.get('vol')
        price=request.POST.get('price')
        status="2"
        bussiness = get_object_or_404(Bussiness, ticker=symbol)
        if bussiness:
            Stock.objects.create(user=user, symbol=bussiness, quantity=quantity, price=price, status=status)
            return redirect('in_index')
        else:
            return redirect('listings')
    else:
        context = {'segment': 'place_bid'}
        return render(request, 'invnSide/landing/listings_detail.html', context)
    
def bids(request):
    user=request.user
    stocks=Stock.objects.filter(user=user)
    context = {'segment': 'bids', 'stocks': stocks}
    return render(request, 'invnSide/home/bids.html', context)

def bids_acc(request,id):
    stock = get_object_or_404(Stock, symbol=id)
    stock.paid = '1'
    stock.save()
    return redirect('bids')

def inv_bussiness(request):
    user=request.user
    paid=Stock.objects.filter(user=user,paid='1')
    context = {'segment': 'inv_bussiness', 'paid': paid}
    return render(request, 'invnSide/home/inv_bussiness.html', context)

def investments(request):
    user=request.user
    stocks=Stock.objects.filter(user=user,paid='1')
    stock_sector_map = {}
    for stock in stocks:
        ticker_symbol = stock.symbol.ticker
        try:
            print(ticker_symbol)
            listing = Listings.objects.get(ticker=ticker_symbol)
            print(listing)
            stock_sector_map[stock] = listing.sector
        except Listings.DoesNotExist:
           stock_sector_map[stock] = "Unknown"
           
    unique_sectors = set(stock_sector_map.values())
    matching_listings = Listings.objects.filter(sector__in=unique_sectors)
    matching_tickers = [listing.ticker for listing in matching_listings]
    data=prediction_model(request,matching_tickers,stock_sector_map)
    # print(data)
    # data=0
    context = {'segment': 'investments', 'stocks': stocks,'stock_sector_map': stock_sector_map,  'matching_tickers': matching_tickers, 'data': data}
    return render(request, 'invnSide/home/investments.html', context)

def paywall(request,id):
    context = {'segment': 'paywall','id':id}
    return render(request, 'invnSide/home/paywall.html',context)
from keras.initializers import glorot_uniform,Orthogonal
from keras.models import load_model

# Load the model
# model = load_model(model_path, custom_objects=custom_objects)
# def prediction_model(request,matching_tickers):
#     for symbol in matching_tickers:
#         df = stocks(symbol, start=datetime.date(2020, 1, 1), end=datetime.date.today())
#         if df.empty:
#             continue
#         else:
#             data_training=pd.DataFrame(df['Close'][0:int(len(df)*0.70)]) 
#             data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
#             if data_training.empty or data_testing.empty:
#                 continue
#             else:
#                 scaler=MinMaxScaler(feature_range=(0,1))
#                 data_training_array=scaler.fit_transform(data_training)
#                 model=load_model(r'D:\FYP\10k\material-dashboard-django-1.0.2\material-dashboard-django-1.0.2\apps\home\keras_model.h5')
#                 past_100_days=data_training.tail(100)
#                 final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
#                 input_data=scaler.fit_transform(final_df)
#                 x_test=[]
#                 y_test=[]
#                 for i in range(100,input_data.shape[0]):
#                     x_test.append(input_data[i-100:i])
#                     y_test.append(input_data[i,0])

#                 if len(x_test)==0 or len(y_test)==0:
#                     continue
#                 else:
#                     x_test,y_test=np.array(x_test),np.array(y_test)
#                     y_predicted=model.predict(x_test)
#                     scaler= scaler.scale_
#                     scale_factor=1/scaler[0]
#                     y_predicted=y_predicted*scale_factor
#                     y_test=y_test*scale_factor
from heapq import nlargest
import random
def prediction_model(request, matching_tickers, stock_sector_map):
    results = {}
    presults = {}
    try:
        for symbol in matching_tickers:
            try:
                df = stocks(symbol, start=datetime.date(2020, 1, 1), end=datetime.date.today())
            except KeyError as e:
                print(f"KeyError: {e}")
                continue
            if df.empty:
                continue
            else:
                data_training = pd.DataFrame(df['Close'][0:int(len(df) * 0.70)])
                data_testing = pd.DataFrame(df['Close'][int(len(df) * 0.70):int(len(df))])
                if data_training.empty or data_testing.empty:
                    continue
                else:
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    data_training_array = scaler.fit_transform(data_training)
                    model = Sequential()
                    model.add(Reshape((100, 1), input_shape=(100,)))
                    model.add(Dense(64, kernel_initializer=Orthogonal(), activation='relu'))
                    past_100_days = data_training.tail(100)
                    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
                    input_data = scaler.fit_transform(final_df)
                    x_test = []
                    y_test = []
                    for i in range(100, input_data.shape[0]):
                        x_test.append(input_data[i - 100:i])
                        y_test.append(input_data[i, 0])

                    if len(x_test) == 0 or len(y_test) == 0 or (np.array(x_test).size == 0).any() or (np.array(y_test).size == 0).any():
                        continue
                    else:
                        x_test, y_test = np.array(x_test), np.array(y_test)
                        y_predicted = model.predict(x_test)
                        scaler = scaler.scale_
                        scale_factor = 1 / scaler[0]
                        y_predicted = y_predicted * scale_factor
                        y_test = y_test * scale_factor
                        top_indices = nlargest(3, range(len(y_predicted)), key=y_predicted.__getitem__)
                        results[symbol] = [(y_predicted[i], symbol) for i in top_indices]
                        presults[symbol] = [(y_predicted[i], df['ticker'].iloc[i]) for i in top_indices]
    except Exception as e:
        print(f"Error occurred: {e}")
        unique_sectors = set(stock_sector_map.values())
        random_listings = list(Listings.objects.filter(sector__in=unique_sectors).order_by('?')[:3])
        for listing in random_listings:
            results[listing.ticker] = [(None, listing.ticker, listing.sector)]
    return results

# Graph API
from django.http import JsonResponse
from rest_framework.views import APIView
# Open Value
class StockDataAPIView(APIView):
    def get(self, request, symbol):
        yesterday = datetime.date.today() - datetime.timedelta(days=7)
        sdata = stocks(symbol, start=yesterday, end=datetime.date.today())
        if 'High' in sdata and len(sdata['High']) > 0:
            data = {
                'labels': list(sdata.index.strftime('%d')),
                'series': [list(sdata['High'])]  
            }
        else:
            data = {'error': 'No data available for the specified symbol'}

        return JsonResponse(data) 

# Volume
class StockVolAPIView(APIView):
    def get(self, request, symbol):
        yesterday = datetime.date.today() - datetime.timedelta(days=7)
        sdata = stocks(symbol, start=yesterday, end=datetime.date.today())
        if 'Volume' in sdata and len(sdata['Volume']) > 0:
            data = {
                'labels': list(sdata.index.strftime('%d')),
                'series': [list(sdata['Volume'])]  
            }
        else:
            data = {'error': 'No data available for the specified symbol'}
        return JsonResponse(data) 
 
# Close 
class StockcloseAPIView(APIView):
    def get(self, request, symbol):
        yesterday = datetime.date.today() - datetime.timedelta(days=7)
        sdata = stocks(symbol, start=yesterday, end=datetime.date.today())
        if 'Close' in sdata and len(sdata['Close']) > 0:
            data = {
                'labels': list(sdata.index.strftime('%d')),
                'series': [list(sdata['Close'])]  
            }
        else:
            data = {'error': 'No data available for the specified symbol'}
        return JsonResponse(data) 
    
from rest_framework.response import Response
from django.db.models import Sum
# Admin
class UsersView(APIView):
    def get(self, request):
        seven_days_ago = timezone.now() - timedelta(days=30)
        users = User.objects.filter(date_joined__gte=seven_days_ago)
        data = users.values('date_joined__date').annotate(num_users=Count('id'))
        response_data = []
        for entry in data:
            response_data.append({
                'date': entry['date_joined__date'],
                'num_users': entry['num_users']
            })
        return JsonResponse(response_data, safe=False)
    
class TotalBidsByDateAdmin(APIView):
    def get(self, request):
        seven_days_ago = timezone.now() - timedelta(days=7)
        stocks = Stock.objects.filter(created_at__gte=seven_days_ago)
        data = stocks.values('created_at__date').annotate(num_bids=Count('id'))
        response_data = []
        for entry in data:
            response_data.append({
                'date': entry['created_at__date'],
                'num_bids': entry['num_bids']
            })
        return JsonResponse(response_data, safe=False)

class TotalRejBidsByDateAdmin(APIView):
    def get(self, request):
        seven_days_ago = timezone.now() - timedelta(days=7)
        stocks = Stock.objects.filter(created_at__gte=seven_days_ago, status='2')
        data = stocks.values('created_at__date').annotate(num_bids=Count('id'))
        response_data = []
        for entry in data:
            response_data.append({
                'date': entry['created_at__date'],
                'num_bids': entry['num_bids']
            })
        return JsonResponse(response_data, safe=False)
# Investor
from django.utils.timezone import localtime
from django.db.models import F
from django.utils import timezone
from datetime import timedelta

class TotalValueByDate(APIView):
    def get(self, request):
        seven_days_ago = timezone.now() - timedelta(days=7)
    
        stocks = Stock.objects.filter(user=request.user, created_at__gte=seven_days_ago)
        data = stocks.values('created_at__date').annotate(total_value=Sum(F('price') * F('quantity')))
        response_data = []
        for entry in data:
            response_data.append({
                'date': entry['created_at__date'],
                'total_value': entry['total_value']
            })
        return JsonResponse(response_data, safe=False)

from django.db.models import Count   
class TotalBidsByDate(APIView):
    def get(self, request):
        seven_days_ago = timezone.now() - timedelta(days=7)
        stocks = Stock.objects.filter(user=request.user, created_at__gte=seven_days_ago, status='0')
        data = stocks.values('created_at__date').annotate(num_bids=Count('id'))
        response_data = []
        for entry in data:
            response_data.append({
                'date': entry['created_at__date'],
                'num_bids': entry['num_bids']
            })
        return JsonResponse(response_data, safe=False)
    
class TotalRejBidsByDate(APIView):
    def get(self, request):
        seven_days_ago = timezone.now() - timedelta(days=7)
        stocks = Stock.objects.filter(user=request.user, created_at__gte=seven_days_ago, status='1')
        data = stocks.values('created_at__date').annotate(num_bids=Count('id'))
        response_data = []
        for entry in data:
            response_data.append({
                'date': entry['created_at__date'],
                'num_bids': entry['num_bids']
            })
        return JsonResponse(response_data, safe=False)
# Form 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
# importing messages
from django.contrib import messages

# Model Forms.
from .forms import UserPostForm, AnswerForm
# String module
from django.template.loader import render_to_string

# Create your views here.

def home2(request):
    user_posts = UserPost.objects.all()
    
    # Display latest posts.
    latest_blogs = BlogPost.objects.order_by('-timestamp')[0:3]

    latest_topics = UserPost.objects.order_by('-date_created')[0:3]
    
    context = {
        'user_posts':user_posts,
        'latest_blogs':latest_blogs,
        'latest_topics':latest_topics
    }
    return render(request, 'form/forum-main.html', context)

@login_required(login_url='login')
def userPost(request):
    # User Post form.
    form = UserPostForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            title = request.POST.get('title')
            description = request.POST.get('description')
            topic = UserPost.objects.create(title=title, author=request.user.author, description=description)
            topic.save()
            return redirect('home')
    else:
        form = UserPostForm()

    context = {'form':form}
    return render(request, 'user-post.html', context)

@login_required(login_url='login')
def postTopic(request, pk):
    # Get specific user post by id.
    post_topic = get_object_or_404(UserPost, pk=pk)

    # Count Post View only for authenticated users
    if request.user.is_authenticated:
        TopicView.objects.get_or_create(user=request.user, user_post=post_topic)

    # Get all answers of a specific post.
    answers = Answer.objects.filter(user_post = post_topic)

    # Answer form.
    answer_form = AnswerForm(request.POST or None)
    if request.method == "POST":
        if answer_form.is_valid():
            content = request.POST.get('content')
            # passing User Id & User Post Id to DB
            ans = Answer.objects.create(user_post=post_topic, user=request.user, content=content)
            ans.save()
            return HttpResponseRedirect(post_topic.get_absolute_url())
    else:
        answer_form = AnswerForm()
    
    context = {
        'topic':post_topic,
        'answers':answers,
        'answer_form':answer_form,
        
    }
    return render(request, 'topic-detail.html', context)

@login_required(login_url='login')
def userDashboard(request):
    topic_posted = request.user.author.userpost_set.all()
    ans_posted = request.user.answer_set.all()
    topic_count = topic_posted.count()
    ans_count = ans_posted.count()
    
    context = {
        'topic_posted':topic_posted,
        'ans_posted':ans_posted,
        'topic_count':topic_count,
        'ans_count':ans_count
    }
    return render(request, 'user-dashboard.html', context)

def searchView(request):
    queryset = UserPost.objects.all()
    search_query = request.GET.get('q')

    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query) 
        ).distinct()
        
        q_count = queryset.count()
    else:
        messages.error(request, f"Oops! Looks like you didn't put any keyword. Please try again.")
        return redirect('home')

    
    context = {
        'queryset':queryset,
        'search_query':search_query,
        'q_count':q_count
    }

    return render(request, 'search-result.html', context)


def upvote(request):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    
    has_upvoted = False

    if answer.upvotes.filter(id = request.user.id).exists():
        answer.upvotes.remove(request.user)
        has_upvoted = False        
    else:
        answer.upvotes.add(request.user)
        answer.downvotes.remove(request.user)
        has_upvoted = True

    return HttpResponseRedirect(answer.user_post.get_absolute_url())
    

def downvote(request):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    
    has_downvoted = False
    
    if answer.downvotes.filter(id = request.user.id).exists():
        answer.downvotes.remove(request.user)
        has_downvoted = False
    else:
        answer.downvotes.add(request.user)
        answer.upvotes.remove(request.user)
        has_downvoted = True
    
    return HttpResponseRedirect(answer.user_post.get_absolute_url())

# Blog listing page view.
def blogListView(request):
    
    # Display all blog posts.
    all_posts = BlogPost.objects.all()
    
    context = {
        'all_posts':all_posts
    }
    return render(request, 'blog-listing.html', context)

    
# Blog single post detail view.
def blogDetailView(request, slug):
    # Get specific post by slug.
    post_detail = get_object_or_404(BlogPost, slug=slug)

    context = {
        'post_detail':post_detail,
    }

    return render(request, 'blog-detail.html', context)  



