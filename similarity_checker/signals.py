from django.db.models.signals import post_save
from django.dispatch import receiver
from similarity_checker.models import SimilarityChecker
from socmed_data.models import SocialMediaData

@receiver(post_save, sender=SimilarityChecker)
def update_verification_socmed(sender, instance, created, **kwargs):
    try:
        verifikasi = SocialMediaData.objects.get(similarity_checker=instance)
    except SocialMediaData.DoesNotExist:
        verifikasi = SocialMediaData.objects.create(similarity_checker=instance)
    
    if instance.kesesuaian == 'Sesuai':
        verifikasi.verify = True
    elif instance.kesesuaian == 'Tidak Sesuai':
        verifikasi.verify = False

    verifikasi.save()