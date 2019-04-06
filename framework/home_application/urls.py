# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^host-status/$', 'host_status'),
    (r'^get_biz_list$', 'get_biz_list'),
    (r'^get_cluster$', 'get_cluster'),
    (r'^search_host_info', 'search_host_info'),# 通过业务和集群查找主机信息
    (r'^execute_task', 'execute_task'),
)
