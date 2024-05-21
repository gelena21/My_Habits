from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UsersTestCase(APITestCase):
    """
    Тесты для операций CRUD с пользователями.
    """

    def setUp(self):
        """
        Настройка данных для тестов.
        """
        self.user = User.objects.create(email="whoare@mail.com")  # Создаем обычного пользователя

        self.user = User.objects.create(email="test@test.com",  # Создаем суперпользователя
                                        password="1234",
                                        is_staff=True,
                                        is_superuser=True)

    def test_create_user(self):
        """
        Тест создания нового пользователя.
        """
        data = {"email": "new_user@mail.com", "password": "1234"}

        response = self.client.post("/users/create/", data)  # Отправляем POST запрос для создания пользователя

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем успешный статус ответа

        self.assertTrue(User.objects.all().exists())  # Проверяем, что пользователь был создан

        self.assertEqual(response.json()["email"], data["email"])  # Проверяем, что email в ответе совпадает с отправленным

    def test_get_list(self):
        """
        Тест получения списка пользователей.
        """
        self.client.force_authenticate(user=self.user)  # Авторизуемся как суперпользователь

        response = self.client.get("/users/list/")  # Отправляем GET запрос для получения списка пользователей

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем успешный статус ответа

    def test_update_user(self):
        """
        Тест обновления данных пользователя.
        """
        self.client.force_authenticate(user=self.user)  # Авторизуемся как суперпользователь

        user_update = User.objects.create(  # Создаем пользователя, которого будем обновлять
            email="whois789@mail.com",
        )

        response = self.client.patch(  # Отправляем PATCH запрос для обновления данных пользователя
            f"/users/{user_update.pk}/", data={"email": "ktoto@kto.ru"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем успешный статус ответа

        self.assertEqual(response.json()["email"], "ktoto@kto.ru")  # Проверяем, что email
        # обновленного пользователя совпадает с ожидаемым
