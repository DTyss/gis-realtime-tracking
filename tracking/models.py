from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser

# -----------------------------------------
# Model người dùng kế thừa từ AbstractUser
# Thêm trường avatar để hiển thị marker
# -----------------------------------------

ONLINE_TIMEOUT_SECONDS = 30
# Thời gian tối đa để người dùng được coi là online (30 giây)
class User(AbstractUser):
    avatar = models.CharField(
        max_length=255,
        default='tracking/avatar/default.png'  # Ảnh mặc định nếu chưa chọn avatar
    )
    last_seen = models.DateTimeField(null=True, blank=True) # thời gian hoạt động gần nhất

    def is_online(self):
        if self.last_seen:
            return timezone.now() - self.last_seen < timedelta(seconds=ONLINE_TIMEOUT_SECONDS)
        return False  

# -----------------------------------------
# Model lưu vị trí (lat, lng) người dùng
# Mỗi lần gửi sẽ lưu kèm thời gian timestamp
# -----------------------------------------
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - ({self.latitude}, {self.longitude})"
