from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email='user@example.com',
                name='testuser',
                password='testpass123'):
    """Creates a user returns it."""
    return get_user_model().objects.create_user(email, name, password)


class ModelTest(TestCase):
    "Test models."

    def test_create_user_with_email_successful(self):
        "Test creating a user with an email is successful."

        email = "test@example.com"
        name = 'testuser'
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            name=name,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        "Test email is normalized for new users"

        sample_emails = [
            ("test1@EXAMPLE.com", "test1@example.com"),
            ("Test2@Example.com", "Test2@example.com"),
            ("TEST3@EXAMPLE.COM", "TEST3@example.com"),
            ("test4@example.COM", "test4@example.com")
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email,
                                                        name='testuser',
                                                        password='SamplePass')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        """Test that create user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testuser', 'SamplePass')

    def test_new_user_without_name_raise_error(self):
        """Test that create user without a name raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('user@example.com',
                                                 '',
                                                 'SamplePass')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testuser',
            'testpassword'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
