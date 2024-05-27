# Generated by Django 5.0.3 on 2024-05-04 15:51

import django.contrib.postgres.fields
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dje", "0002_initial"),
        ("product_portfolio", "0004_alter_scancodeproject_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductPackageVEX",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, verbose_name="UUID"
                    ),
                ),
                (
                    "vulnerability_id",
                    models.CharField(help_text="VCID-xxxx-xxxx-xxxx", max_length=50),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("R", "RESOLVED"),
                            ("RWP", "RESOLVED_WITH_PEDIGREE"),
                            ("E", "EXPLOITABLE"),
                            ("IT", "IN_TRIAGE"),
                            ("FP", "FALSE_POSITIVE"),
                            ("NA", "NOT_AFFECTED"),
                        ],
                        help_text="The rationale of why the impact analysis state was asserted.",
                        max_length=3,
                    ),
                ),
                (
                    "responses",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True,
                            choices=[
                                ("CNF", "CAN_NOT_FIX"),
                                ("RB", "ROLLBACK"),
                                ("U", "UPDATE"),
                                ("WNF", "WILL_NOT_FIX"),
                                ("WA", "WORKAROUND_AVAILABLE"),
                            ],
                            max_length=3,
                        ),
                        help_text="A response to the vulnerability by the manufacturer, supplier, or project responsible for the affected component or service",
                        max_length=20,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "justification",
                    models.CharField(
                        choices=[
                            ("CNP", "CODE_NOT_PRESENT"),
                            ("CNR", "CODE_NOT_REACHABLE"),
                            ("PP", "PROTECTED_AT_PERIMITER"),
                            ("PR", "PROTECTED_AT_RUNTIME"),
                            ("PC", "PROTECTED_BY_COMPILER"),
                            ("PMC", "PROTECTED_BY_MITIGATING_CONTROL"),
                            ("RC", "REQUIRES_CONFIGURATION"),
                            ("RD", "REQUIRES_DEPENDENCY"),
                            ("RE", "REQUIRES_ENVIRONMENT"),
                        ],
                        help_text="The rationale of why the impact analysis state was asserted.",
                        max_length=3,
                    ),
                ),
                (
                    "detail",
                    models.CharField(help_text="Additional notes to explain the VEX."),
                ),
                (
                    "ignored",
                    models.BooleanField(
                        default=False, help_text="Ignore VEX for this vulnerability"
                    ),
                ),
                (
                    "dataspace",
                    models.ForeignKey(
                        editable=False,
                        help_text="A Dataspace is an independent, exclusive set of DejaCode data, which can be either nexB master reference data or installation-specific data.",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="dje.dataspace",
                    ),
                ),
                (
                    "productpackage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product_portfolio.productpackage",
                    ),
                ),
            ],
            options={
                "unique_together": {
                    ("productpackage", "vulnerability_id", "dataspace")
                },
            },
        ),
    ]
