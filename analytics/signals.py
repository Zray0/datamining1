from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from analytics.models import CustomerCluster

@receiver(user_logged_in)
def assign_customer_cluster(sender, user, request, **kwargs):
    # Replace 'user' with your correct foreign key name if needed
    obj, created = CustomerCluster.objects.get_or_create(
        user=user,  # use 'customer=user' if your model uses 'customer'
        defaults={'cluster_id': 1, 'cluster_name': 'Default Segment'}
    )
    # Optionally, you could assign based on logic (profile, orders, etc.)
