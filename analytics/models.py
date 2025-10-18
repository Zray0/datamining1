# analytics/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField

class AssocRule(models.Model):
    antecedents = ArrayField(models.CharField(max_length=64))
    consequents = ArrayField(models.CharField(max_length=64))
    support = models.FloatField()
    confidence = models.FloatField()
    lift = models.FloatField()
    leverage = models.FloatField()
    conviction = models.FloatField()
    mined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-lift", "-confidence", "-support"]),
        ]

    def __str__(self):
        ants = ",".join(self.antecedents)
        cons = ",".join(self.consequents)
        return f"{ants} -> {cons} (lift={self.lift:.2f})"
