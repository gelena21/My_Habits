from rest_framework import routers
from django.urls import path
from habits.views import HabitAPIViewSet, UserHabitListApiView

router = routers.SimpleRouter()
router.register('habits', HabitAPIViewSet)

urlpatterns = [
    path('user_habits/', UserHabitListApiView.as_view(), name='user_habits')
]
urlpatterns += router.urls
