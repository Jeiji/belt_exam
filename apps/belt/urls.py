from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^add_plan$', views.add_plan),
    url(r'^add_plan_process$', views.add_plan_process),
    url(r'^join_plan_process_(?P<plan_dest>.+)$', views.join_plan_process),
    url(r'^remove_plan_(?P<plan_id>\d+)$', views.remove_plan),
    url(r'^delete_plan_(?P<plan_id>\d+)$', views.delete_plan),
    url(r'^show_plan_(?P<plan_id>\d+)$', views.show_plan),
]
