from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.permissions import IsUser
from habits.serializers import HabitSerializer

from rest_framework.pagination import PageNumberPagination


class HabitAPIViewSet(ModelViewSet):
    """
    ViewSet для работы с привычками. Реализует CRUD операции и пагинацию.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        """
        Переопределение метода сохранения для добавления пользователя к новой привычке.
        """
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()

    def list(self, request):
        """
        Переопределение метода получения списка для применения пагинации.
        """
        habits = Habit.objects.filter(is_public=True)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(habits, request)
        serializer = HabitSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_permissions(self):
        """
        Переопределение метода для установки прав доступа в зависимости от действия.
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsUser | IsAdminUser]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsUser | IsAdminUser]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsUser | IsAdminUser]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsUser]
        return [permission() for permission in self.permission_classes]


class UserHabitListApiView(generics.ListAPIView):
    """
    Представление для получения списка привычек текущего пользователя.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Получение списка привычек для текущего аутентифицированного пользователя.
        """
        return Habit.objects.filter(user=self.request.user)
