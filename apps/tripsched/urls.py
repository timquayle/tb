from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process_registration$', views.process_registration),
    url(r'^logincheck$', views.loginchk),
    url(r'^travels/add$', views.newtrippage),
    url(r'^travels/process_trip$', views.processtrip),
    url(r'^travels/destination/(?P<number>\d+)$', views.destinationpage),
    url(r'^travels/join/(?P<number>\d+)$', views.processjoin),
    #url(r'^users/adminupdateinfo$', views.adminupdateinfo),
    #url(r'^users/normalupdateinfo$', views.normalupdateinfo),
    #url(r'^users/adminupdatepassword$', views.adminupdatepassword),
    #url(r'^users/editprofile/(?P<number>\d+)$', views.editprofilepage),
    url(r'^logout$', views.logout),
    ##url(r'^users/show/(?P<number>\d+)$', views.showuserpage),
    #url(r'^users/send_message$', views.sendmessage),
    #url(r'^users/post_comment$', views.postcomment),
    #url(r'^users/updatepassword$', views.updatepassword)
    #url(r'^users/(?P<number>\d+)$', views.userview),
    #url(r'^books/(?P<number>\d+)$', views.bookview),
    #url(r'^delete_review/(?P<number>\d+)$', views.deletereview),
    #url(r'^add_review/(?P<number>\d+)$', views.addreview)
  ]