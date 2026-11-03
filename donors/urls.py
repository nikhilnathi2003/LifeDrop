from django.urls import path

from . import views

urlpatterns = [
    # Sujith: index (ListView) + detail (DetailView) + post/edit/my
    path("", views.RequestListView.as_view(), name="home"),
    path("request/<int:pk>/", views.RequestDetailView.as_view(), name="request_detail"),
    path("post/", views.post_request, name="post_request"),
    path("request/<int:pk>/edit/", views.edit_request, name="edit_request"),
    path("my-requests/", views.my_requests, name="my_requests"),

    # Charan: image uploads + saved requests (bookmarks)
    path("request/<int:pk>/photos/", views.upload_images, name="upload_images"),
    path("image/<int:pk>/delete/", views.delete_image, name="delete_image"),
    path("request/<int:pk>/save/", views.toggle_saved, name="toggle_saved"),
    path("saved/", views.saved_requests, name="saved_requests"),

    # Sai Srinivas: messaging
    path("request/<int:pk>/message/", views.send_message, name="send_message"),
    path("request/<int:pk>/donate/", views.offer_to_donate, name="offer_to_donate"),

    # Sneha: contact, about, team
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("team/", views.team, name="team"),

    # Nikhil: accounts
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/upload-card/", views.upload_card, name="upload_card"),
]
