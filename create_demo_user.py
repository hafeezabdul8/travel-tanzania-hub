import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afcon.settings')
django.setup()

from django.contrib.auth.models import User
from chatbot.models import ChatProfile

# Create demo user if not exists
user, created = User.objects.get_or_create(
    username='demo_user',
    defaults={
        'email': 'demo@afcon2027.tz',
        'is_active': True
    }
)

if created:
    user.set_password('demo1234')
    user.save()
    ChatProfile.objects.create(user=user)
    print("Demo user created:")
    print("Username: demo_user")
    print("Password: demo1234")
else:
    print("Demo user already exists")

# List all users
print("\nAll users:")
for u in User.objects.all():
    print(f"- {u.username} ({u.email})")
