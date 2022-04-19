from django.urls import path
# from .views import peer1, peer2, peer
from .views import peer, record, create_or_join,temp_redirect

urlpatterns = [
    path('join-room/', record, name='peer'),
    path('', create_or_join, name='create_or_join'),
    path('not-able-to-join/', temp_redirect, name='temp_redirect'),
    
    # path("record/", record, name="record"),
    # path('peer1/', peer1, name='peer1'),
    # path('peer2/', peer2, name='peer2'),
]