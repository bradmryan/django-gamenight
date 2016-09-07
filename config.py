import settings

if settings.DEBUG:
    from . import dev
    STEAM_KEY = dev.STEAM_KEY
else:
    STEAM_KEY = os.environ['STEAM_KEY']

MINIMUM_MATCHES = 2
