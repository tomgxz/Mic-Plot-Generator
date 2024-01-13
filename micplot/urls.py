from django.urls import path
from django.views.static import serve 
from django.views.generic.base import TemplateView

from . import views

app_name = "micplot"

urlpatterns = [
    path("", views.index, name="index"),
    path("shows/new", views.newshow, name="newshow"),
    path("shows/show/<int:show_id>/<str:show_name>", views.show, name="show"),
    path("shows/show/<int:show_id>/<str:show_name>/mic/new", views.newmic, name="newmic"),
    path("shows/show/<int:show_id>/<str:show_name>/act/new", views.newact, name="newact"),
    path("shows/show/<int:show_id>/<str:show_name>/act/<int:act_id>", views.act, name="act"),
    path("shows/show/<int:show_id>/<str:show_name>/act/<int:act_id>/scene/new", views.newscene, name="newscene"),
    path("shows/show/<int:show_id>/<str:show_name>/act/<int:act_id>/scene/new/multiple", views.newscenemultiple, name="newscenemultiple"),
    path("shows/show/<int:show_id>/<str:show_name>/act/<int:act_id>/update/<int:mic_id>/<int:scene_id>", views.updateplot, name="updateplot"),
    
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    )
]