import os
import django

# Konfiguracja środowiska Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_system.settings') # Zmień na nazwę swojego folderu z settings.py
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'TwojeSilneHaslo123')

    if not User.objects.filter(username=username).exists():
        print(f"Tworzenie superusera: {username}...")
        User.objects.create_superuser(username, email, password)
        print("Superuser utworzony pomyślnie.")
    else:
        print(f"Użytkownik {username} już istnieje. Pomijam.")

if __name__ == "__main__":
    create_admin()