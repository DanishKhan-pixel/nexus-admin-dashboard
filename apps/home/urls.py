# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.landing_page, name='index'),
    path('listings', views.listings, name='listings'),
    path('stock_detail/<str:symbol>/', views.viewlistingDetails, name='stock_detail'),
    # path('', views.index, name='home'),
    # path('', views.index, name='home'),

    # For Admin
    path('index', views.index, name='home'),
    path('ad/profile',views.admin_profile, name='admin_profile'),
    path('ad/bids',views.all_bids, name='all_bids'),
    # View Users
    path('ad/users', views.users, name='users'),
    # Edit Users
    path('ad/users/<int:id>', views.user_profile, name='user_profile'),
    # Delete Users
    path('ad/users/delete/<int:user_id>', views.delete_user, name='delete_user'),
    path('ad/verifications', views.verfications, name='verfications'),
    path('ad/verifications/<int:id>', views.sch_meet, name='sch_meet'),
    path('ad/verifications/acc/<int:id>', views.acc, name='acc'),
    path('ad/verifications/rej/<int:id>', views.rej, name='rej'),
    # For Ent
    path('ent',views.ent_index, name='ent_index'),
    path('ent/profile',views.ent_profile, name='ent_profile'),
    path('ent/bussiness',views.ent_bussiness, name='ent_bussiness'),
    path('ent/bussiness/add',views.add_bussiness, name='add_bussiness'),
    path('ent/bussiness/edit/<int:id>',views.edit_bussiness, name='edit_bussiness'),
    path('ent/bussiness/delete/<int:id>',views.delete_bussiness, name='delete_bussiness'),
    path('ent/stocks',views.ent_stocks, name='ent_stocks'),
    path('ent/stocks/ent_stocks_meeting/<int:id>',views.ent_stocks_meeting, name='ent_stocks_meeting'),
    path('ent/stocks/ent_stocks_meeting/acc/<int:id>',views.ent_stocks_meeting_acc, name='ent_stocks_meeting_acc'),
    path('ent/stocks/ent_stocks_meeting/rej/<int:id>',views.ent_stocks_meeting_rej, name='ent_stocks_meeting_rej'),
    # path('ent/verifications',views.ent_verfications, name='ent_verfications'),
    
    # For Investor
    path('investor',views.in_index, name='in_index'),
    path('in/profile',views.in_profile, name='in_profile'),
    path('in/place_bids',views.place_bids, name='place_bids'),
    path('in/bids',views.bids, name='bids'),
    path('in/bids/acc/<int:id>',views.bids_acc, name='bids_acc'),
    path('in/bussiness',views.inv_bussiness, name='inv_bussiness'),
    path('inv/investments/',views.investments, name='investments'),
    # path('ent/bussiness/edit/<int:id>',views.edit_bussiness, name='edit_bussiness'),
    # path('ent/bussiness/delete/<int:id>',views.delete_bussiness, name='delete_bussiness'),
    path('prediction_model',views.prediction_model, name='prediction_model'),
    path('paywall/acc/<int:id>',views.paywall, name='paywall'),
    
    # API
    path('api/stock-data/<str:symbol>/', views.StockDataAPIView.as_view(), name='stock-data'),
    path('api/vol-data/<str:symbol>/', views.StockVolAPIView.as_view(), name='vol-data'),
    path('api/close-data/<str:symbol>/', views.StockcloseAPIView.as_view(), name='close-data'),
    # Investor
    path('api/investor/graphin', views.TotalValueByDate.as_view(), name='investor-bids'),
    path('api/investor/bids', views.TotalBidsByDate.as_view(), name='pending-bids'),
    path('api/investor/rejbids', views.TotalRejBidsByDate.as_view(), name='rejbids'),
    # Entr
    # Admin
    path('api/admin/users', views.UsersView.as_view(), name='admin-users'),
    path('api/admin/bids',views.TotalBidsByDateAdmin.as_view(), name='admin-bids'),
    path('api/admin/rejbids', views.TotalRejBidsByDate.as_view(), name='admin-rejbids'),
    
    # Form 
    path('form', views.home2, name='home2'),
    path('user-post/', views.userPost, name='user-post'),
    path('topic/<int:pk>/', views.postTopic, name='topic-detail'),
    path('search-result/', views.searchView, name='search-result'),
    path('user-dashboard/', views.userDashboard, name='user-dashboard'),
    path('upvote/', views.upvote, name='upvote'),
    path('downvote/', views.downvote, name='downvote'),
    path('blog/', views.blogListView, name='blog'),
    path('article/<slug:slug>/', views.blogDetailView, name='article-detail'),
]   
