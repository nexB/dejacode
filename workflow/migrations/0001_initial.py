# Generated by Django 4.2.7 on 2023-11-27 21:12

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import dje.fields
import uuid
import workflow.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dje", "0002_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Priority",
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
                    "label",
                    models.CharField(
                        help_text="Concise name to identify the Priority.",
                        max_length=50,
                    ),
                ),
                (
                    "position",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        db_index=True,
                        help_text="A number to control the sequence of the Priorities presented to the user when selecting one from the dropdown list.",
                        null=True,
                    ),
                ),
                (
                    "color_code",
                    models.CharField(
                        blank=True,
                        help_text="You can specify a valid HTML color code (e.g. #FFFFFF) to apply to your Priority.",
                        max_length=7,
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
            ],
            options={
                "verbose_name_plural": "priorities",
                "ordering": ["position", "label"],
                "unique_together": {("dataspace", "label"), ("dataspace", "uuid")},
            },
        ),
        migrations.CreateModel(
            name="RequestTemplate",
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
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text="The date and time the object was created.",
                    ),
                ),
                (
                    "last_modified_date",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text="The date and time the object was last modified.",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Unique name of the template.", max_length=100
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Provide a title and/or general instructions to the Requestor about this Request form.",
                        verbose_name="Request header text",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text="Enable this to set the current form active. Only one Form can be active per content type.",
                    ),
                ),
                (
                    "include_applies_to",
                    models.BooleanField(
                        default=True,
                        help_text='Enable this to present an "Applies to" field to a requester creating a request based on this template, or anyone subsequently editing that request. Disable it for a request that does not need an "Applies to" reference.',
                    ),
                ),
                (
                    "include_product",
                    models.BooleanField(
                        default=False,
                        help_text="Enable this to present a Product choice to a requester using this template. Disable it for a request that does not need a Product context.",
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        help_text="You can define one Request Template for each application object.",
                        limit_choices_to=models.Q(
                            models.Q(
                                ("app_label", "component_catalog"),
                                ("model", "component"),
                            ),
                            models.Q(
                                ("app_label", "component_catalog"), ("model", "package")
                            ),
                            models.Q(
                                ("app_label", "license_library"), ("model", "license")
                            ),
                            models.Q(
                                ("app_label", "product_portfolio"), ("model", "product")
                            ),
                            _connector="OR",
                        ),
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contenttypes.contenttype",
                        verbose_name="object type",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        help_text="The application user who created the object.",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_%(class)ss",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
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
                    "default_assignee",
                    models.ForeignKey(
                        blank=True,
                        help_text="Optionally specify the application user that should be the first to review a request using this template, and should receive an email when the request is submitted.",
                        limit_choices_to={"is_active": True, "is_staff": True},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    dje.fields.LastModifiedByField(
                        editable=False,
                        help_text="The application user who last modified the object.",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="modified_%(class)ss",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "unique_together": {("dataspace", "uuid"), ("dataspace", "name")},
            },
        ),
        migrations.CreateModel(
            name="Request",
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
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text="The date and time the object was created.",
                    ),
                ),
                (
                    "last_modified_date",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text="The date and time the object was last modified.",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("open", "Open"),
                            ("closed", "Closed"),
                            ("draft", "Draft"),
                        ],
                        db_index=True,
                        default="open",
                        help_text='Status of the request. "Draft" indicates that the request is not yet ready for action, pending further details from the requestor. "Open" indicates that the assignee has not finished the requested actions, and also that comments from all interested parties are welcome. "Closed" indicates that no further actions or comments are needed or expected.',
                        max_length=10,
                    ),
                ),
                (
                    "is_private",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text="When checked, the details of this request are visible only to the original requester and to request reviewers, and other users only see a limited summary. As an administrator, you can check or un-check this indicator to make a request private or public.",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Notes from one or more request reviewers regarding research, issues, and conclusions related to the request.",
                    ),
                ),
                (
                    "product_context",
                    models.ForeignKey(
                        blank=True,
                        help_text="Identify the Product impacted by your Request.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        parent_link=True,
                        to="product_portfolio.product",
                    ),
                ),
                (
                    "serialized_data",
                    models.TextField(
                        blank=True,
                        help_text="Optional data provided by the User making the request. Can be used by an Admin to pre-fill a form. Stored as JSON format.",
                    ),
                ),
                (
                    "object_id",
                    models.PositiveIntegerField(
                        blank=True,
                        db_index=True,
                        help_text="ID of the object attached to this request. This is used in combination with the content_type for the content_object field.",
                        null=True,
                    ),
                ),
                (
                    "content_object_repr",
                    models.CharField(
                        blank=True,
                        help_text="String representation of the attached content_object if any. This is useful for search purposes and not intended for display.",
                        max_length=1000,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        db_index=True,
                        help_text="The Request Title is a concise statement of the Request purpose and content.",
                        max_length=255,
                    ),
                ),
                (
                    "cc_emails",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.EmailField(max_length=254),
                        blank=True,
                        help_text="You can provide a comma-separated list of email addresses to publish email notifications to any users that should be aware of the progress of this request.",
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        help_text="The application user currently assigned to review the request and take appropriate action.",
                        limit_choices_to={"is_active": True, "is_staff": True},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="request_as_assignee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        help_text="Stores the type of the object requested. Supported types are Component, Package, License and Product",
                        limit_choices_to=models.Q(
                            models.Q(
                                ("app_label", "component_catalog"),
                                ("model", "component"),
                            ),
                            models.Q(
                                ("app_label", "component_catalog"), ("model", "package")
                            ),
                            models.Q(
                                ("app_label", "license_library"), ("model", "license")
                            ),
                            models.Q(
                                ("app_label", "product_portfolio"), ("model", "product")
                            ),
                            _connector="OR",
                        ),
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contenttypes.contenttype",
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
                    "last_modified_by",
                    dje.fields.LastModifiedByField(
                        editable=False,
                        help_text="The application user who last modified the object.",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="modified_%(class)ss",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "priority",
                    models.ForeignKey(
                        blank=True,
                        help_text="The priority is intended to provide team members with a guideline for selecting and assigning requests for additional action, based on the criticality of the request.",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="workflow.priority",
                    ),
                ),
                (
                    "request_template",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="requests",
                        to="workflow.requesttemplate",
                    ),
                ),
                (
                    "requester",
                    models.ForeignKey(
                        editable=False,
                        help_text="Creator of the request.",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="request_as_requester",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-last_modified_date"],
                "unique_together": {("dataspace", "uuid")},
            },
        ),
        migrations.CreateModel(
            name="RequestEvent",
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
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text="The date and time the object was created.",
                    ),
                ),
                (
                    "last_modified_date",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text="The date and time the object was last modified.",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "event_type",
                    models.IntegerField(
                        choices=[(1, "Edition"), (2, "Attachment"), (3, "Closed")]
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
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="workflow.request",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["created_date"],
                "unique_together": {("dataspace", "uuid")},
            },
        ),
        migrations.CreateModel(
            name="RequestComment",
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
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text="The date and time the object was created.",
                    ),
                ),
                (
                    "last_modified_date",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text="The date and time the object was last modified.",
                    ),
                ),
                ("text", models.TextField()),
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
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="workflow.request",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["created_date"],
                "unique_together": {("dataspace", "uuid")},
            },
        ),
        migrations.CreateModel(
            name="RequestAttachment",
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
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text="The date and time the object was created.",
                    ),
                ),
                (
                    "last_modified_date",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text="The date and time the object was last modified.",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        max_length=350,
                        upload_to=workflow.models.generate_attachment_path,
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
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="workflow.request",
                    ),
                ),
                (
                    "uploader",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["created_date"],
                "unique_together": {("dataspace", "uuid")},
            },
        ),
        migrations.CreateModel(
            name="Question",
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
                    "label",
                    models.CharField(
                        help_text="Label for the form input.", max_length=255
                    ),
                ),
                (
                    "help_text",
                    models.TextField(
                        blank=True,
                        help_text="Descriptive text (instructions) to display to the Requestor below the question.",
                    ),
                ),
                (
                    "input_type",
                    models.CharField(
                        choices=[
                            ("CharField", "Text"),
                            ("TextField", "Paragraph text"),
                            ("BooleanField", "Yes/No"),
                            ("DateField", "Date"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "is_required",
                    models.BooleanField(
                        default=False,
                        help_text="Indicate if the requestor must enter a value in the answer",
                    ),
                ),
                ("position", models.PositiveSmallIntegerField()),
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
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="workflow.requesttemplate",
                    ),
                ),
            ],
            options={
                "ordering": ["position"],
                "unique_together": {("dataspace", "uuid")},
            },
        ),
    ]
