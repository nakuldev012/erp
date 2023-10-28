import pytz
from django.conf import settings

# Timezone
TZ = pytz.timezone("UTC")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB 