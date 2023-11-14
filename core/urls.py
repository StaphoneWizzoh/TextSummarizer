from django.urls import path

from .views import index,summary_list,tutorial,vanilla_summary,SummaryDetail

urlpatterns = [
    path("", index, name="landing"),
    path("tutorial/", tutorial, name="tutorial"),
    path("summary/", vanilla_summary, name="vanilla"),
    path("summary_list/", summary_list, name="summary_list"),
    path("summary/<int:pk>/", SummaryDetail.as_view(), name="detail")
]
