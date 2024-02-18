from django.urls import path
from django.views.static import serve 
from django.views.generic.base import TemplateView

from .localsettings import APP_NAME as app_name
from . import views

_showprefix = "shows/show/<int:show_id>/<str:show_name>"

urlpatterns = [
    path("", views.index, name="index"),
    path("shows/new", views.newshow, name="newshow"),
    path(f"{_showprefix}", views.show, name="show"),
    path(f"{_showprefix}/mic/new", views.newmic, name="newmic"),
    path(f"{_showprefix}/act/new", views.newact, name="newact"),
    path(f"{_showprefix}/act/<int:act_id>", views.act, name="act"),
    path(f"{_showprefix}/act/<int:act_id>/scene/new", views.newscene, name="newscene"),
    path(f"{_showprefix}/act/<int:act_id>/scene/new/multiple", views.newscenemultiple, name="newscenemultiple"),
    path(f"{_showprefix}/act/<int:act_id>/update/<int:mic_id>/<int:scene_id>", views.updateplot, name="updateplot"),
    
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"))
]