from django.db import models
from django.utils import timezone


class RequestedURL(models.Model):
    url_name = models.URLField(max_length=228)
    timeshift = models.DurationField(blank=True, null=True)  # Поле для указания задержки перед обработкой
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url_name

    def is_ready(self):
        if self.pub_date:
            if self.timeshift:
                now = timezone.now()
                #  Не будет парсить url с отрицательной задержкой
                return self.pub_date <= now - self.timeshift <= now
            else:
            	return True


    class Meta:
    	verbose_name = 'URL для парсинга'
    	verbose_name_plural = 'URL для парсинга'


class URLResults(models.Model):
    requested_url = models.OneToOneField(RequestedURL, on_delete = models.CASCADE, primary_key = True)
    # Не стал использовать разные поля, ибо так проще, а скорость и суть программы от этого не меняется
    info = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.url_name
