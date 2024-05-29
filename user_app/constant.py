
import random
import string


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
