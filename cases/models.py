from django.db import models


class CoronaCaseRaw(models.Model):
    QUARANTINED = 'QT'
    SUSPECTED = 'SP'
    INFECTED = 'IN'
    RECOVERED = 'RC'
    DECEASED = 'DC'
    CASE_TYPE_CHOICES = [
        (QUARANTINED, 'Quarantined'),
        (SUSPECTED, 'Suspected'),
        (INFECTED, 'Infected'),
        (RECOVERED, 'Recovered'),
        (DECEASED, 'Deceased'),
    ]
    case_type = models.CharField(
        max_length=2,
        choices=CASE_TYPE_CHOICES,
        default=SUSPECTED,
    )
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1200)
    latitude = models.DecimalField(max_digits=15, decimal_places=12) 
    longitude = models.DecimalField(max_digits=15, decimal_places=12) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['latitude', 'longitude'], name="location"),
        ]
