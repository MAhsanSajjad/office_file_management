
import random
import string
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import user_passes_test

def create_slug(name=None, slugs=[]):
    non_url_safe = ['"', '#', '$', '%', '&', '+',
                    ',', '/', ':', ';', '=', '?',
                    '@', '[', '\\', ']', '^', '`',
                    '{', '|', '}', '~', "'", '.']
    name = name.lower()
    for i in non_url_safe:
        if i in name:
            name = name.replace(i, ' ')
    slug = name.replace(' ', '-')
    slug = slug.replace('--', '-')
    if slug in slugs:
        random_digits_for_slug = ''.join(
            random.SystemRandom().choice(string.hexdigits + string.hexdigits) for _ in range(4))
        slug = f"{slug}-{random_digits_for_slug}"
    return slug


# decorator for superuser login 
def superuser_required(view_func=None, redirect_field_name='login',
                   login_url='login'):
 
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator