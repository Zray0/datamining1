from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

class AssocRule(models.Model):
    antecedents = ArrayField(models.CharField(max_length=64), default=list)
    consequents = ArrayField(models.CharField(max_length=64), default=list)
    support = models.FloatField()
    confidence = models.FloatField()
    lift = models.FloatField()
    leverage = models.FloatField(default=0.0)
    conviction = models.FloatField(default=0.0)
    mined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [models.Index(fields=["-lift", "-confidence", "-support"])]

class CustomerCluster(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="cluster_assignments"
    )
    customer_key = models.CharField(max_length=128, db_index=True)
    cluster_id = models.IntegerField(db_index=True)
    cluster_name = models.CharField(max_length=128, blank=True)
    algo = models.CharField(max_length=50, default="kmeans")
    k = models.IntegerField()
    features = models.JSONField(default=dict)
    fitted_at = models.DateTimeField(auto_now_add=True)

class ProductCluster(models.Model):
    sku = models.CharField(max_length=64, db_index=True)
    cluster_id = models.IntegerField(db_index=True)
    algo = models.CharField(max_length=50, default="kmeans")
    k = models.IntegerField()
    features = models.JSONField(default=dict)
    fitted_at = models.DateTimeField(auto_now_add=True)
