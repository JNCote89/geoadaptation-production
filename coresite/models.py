# Import to connect with the database
from django.db import models

# Create your models here. Don't forget to use python manage.py makemigrations and migrate the first time you configure
# your model. The connection information to the database are setted in the settings.py file under databases.

# Table that consist of the position of the sensors. It's only 10 rows that will never change over time.
class magog_sensor(models.Model):
    web_lon = models.FloatField()
    web_lat = models.FloatField()
    device_id = models.CharField(max_length=25, primary_key=True)

    # The meta specify the name of your table in your PostgreSQL database
    class Meta:
        db_table = 'magog_sensor'


# Table that holds the temperature of each device and the time it was recorded. To be used with the table holding
# the coordinate of each sensor, with the device_id being the key to join them.
class magog_uhi(models.Model):
    device_id = models.CharField(max_length=25, primary_key=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    time = models.TimeField()
    date = models.DateField()

    class Meta:
        db_table = 'magog_uhi'
        # Django doesn't really support composite primary key. We still need to define a primary key, but beware that
        # this field will be read only. For my needs, it was ok to use this scheme, but it's not necessarily the best
        # practice if you want to scale up.
        unique_together = (('device_id', 'time', 'date'),)
