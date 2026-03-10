# models.py

from django.db import models


class Category(models.Model):
    id          = models.BigAutoField(primary_key=True)
    name        = models.CharField(max_length=100, unique=True,
                                   help_text="e.g. temple, fort, museum")
    description = models.TextField(blank=True, null=True)
    icon_url    = models.CharField(max_length=500, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        indexes  = [
            models.Index(fields=["name"], name="idx_categories_name"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="uq_categories_name"),
        ]

    def __str__(self):
        return self.name


class Experience(models.Model):
    id                 = models.BigAutoField(primary_key=True)
    category_id          = models.ForeignKey(
                             Category,
                             on_delete=models.RESTRICT,
                             db_column="category_id",
                             related_name="experiences",
                         )
    name               = models.CharField(max_length=255)
    description        = models.TextField(blank=True, null=True)
    location           = models.CharField(max_length=255)
    latitude           = models.DecimalField(
                             max_digits=10, decimal_places=8,
                             blank=True, null=True
                         )
    longitude          = models.DecimalField(
                             max_digits=11, decimal_places=8,
                             blank=True, null=True
                         )
    image_url          = models.CharField(max_length=500, blank=True, null=True)
    max_daily_capacity = models.IntegerField(
                             help_text="Maximum visitors per day"
                         )
    entry_fee_base     = models.DecimalField(max_digits=10, decimal_places=2)
    is_open            = models.BooleanField(default=True)
    opening_time       = models.TimeField(blank=True, null=True)
    closing_time       = models.TimeField(blank=True, null=True)
    last_entry_time    = models.TimeField(blank=True, null=True)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)
    deleted_at         = models.DateTimeField(
                             blank=True, null=True,
                             help_text="Soft delete — NULL means active"
                         )

    class Meta:
        db_table = "experience"
        indexes  = [
            models.Index(fields=["category"],            name="idx_experience_category_id"),
            models.Index(fields=["name"],                name="idx_experience_name"),
            models.Index(fields=["category", "is_open"], name="idx_experience_category_is_open"),
        ]

    def __str__(self):
        return f"{self.name} ({self.category})"

    # ------------------------------------------------------------------ #
    #  Soft-delete helpers                                                 #
    # ------------------------------------------------------------------ #

    def soft_delete(self):
        """Mark the record as deleted without removing it from the DB."""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def restore(self):
        """Undo a soft delete."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])

    @property
    def is_deleted(self):
        return self.deleted_at is not None