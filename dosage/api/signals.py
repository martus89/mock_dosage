from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from datetime import datetime
from warehouse.models import Storage, Product, ApprovedDrug, User, DrugFormChoice


@receiver(post_save, sender=Product)
def change_updated_by(sender, instance, created, **kwargs):
    if not created:
        date_stamp = datetime.now().strftime("%d-%m-%y")
        new_line = f"{date_stamp} Product has been transferred to {instance.storage}\n"
        result = new_line + instance.extra_info
        print(f"{instance.extra_info}")
        Product.objects.filter(id=instance.id).update(extra_info=result)

# TODO: CHANGE THIS TO UNIVERSAL SIGNAL FOR ALL MODELS AT ONCE


@receiver(post_save, sender=ApprovedDrug)
def approved_drug_status_checks(sender, instance, created, **kwargs):
    post_save.disconnect(approved_drug_status_checks, sender=ApprovedDrug)

    date_stamp = datetime.now().strftime("%d-%m-%y")

    prefix_updates = {
        (True, True): 'CONTROLLED: ',
        (True, False): '',
        (False, True): 'CONTROLLED/NOT APPROVED: ',
        (False, False): 'NOT APPROVED: ',
    }

    update_rule = prefix_updates[(instance.is_approved, instance.is_controlled)]
    new_prefix = update_rule

    log_lines = {
        (True, True): f"{date_stamp} !!! DRUG CONTROLLED / Approved for sale\n",
        (True, False): f"{date_stamp} Approved for sale\n",
        (False, True): f"{date_stamp} !!! DRUG CONTROLLED / NOT APPROVED FOR SALE\n",
        (False, False): f"{date_stamp} !!! NOT APPROVED FOR SALE\n"
    }

    new_line = log_lines[(instance.is_approved, instance.is_controlled)]
    result = new_line + instance.extra_info

    ApprovedDrug.objects.filter(id=instance.id).update(extra_info=result, str_prefix=new_prefix)

    products = Product.objects.filter(approved_drug=instance)

    for product in products:
        product_extra_info = product.extra_info if hasattr(product, 'extra_info') else ''
        updated_extra_info = new_line + product_extra_info
        Product.objects.filter(id=product.id).update(extra_info=updated_extra_info)

    post_save.connect(approved_drug_status_checks, sender=ApprovedDrug)
