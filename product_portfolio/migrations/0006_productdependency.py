# Generated by Django 5.0.6 on 2024-08-02 15:02

import django.db.models.deletion
import dje.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('component_catalog', '0005_remove_component_concluded_license_and_more'),
        ('dje', '0003_alter_dejacodeuser_homepage_layout'),
        ('product_portfolio', '0005_alter_product_license_expression_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The date and time the object was created.')),
                ('last_modified_date', models.DateTimeField(auto_now=True, db_index=True, help_text='The date and time the object was last modified.')),
                ('dependency_uid', models.CharField(help_text='The unique identifier of this dependency.', max_length=1024)),
                ('declared_dependency', models.CharField(blank=True, help_text='A dependency as stated in a project manifest or lockfile, which may be required or optional, and may be associated with specific version ranges.', max_length=1024)),
                ('extracted_requirement', models.CharField(blank=True, help_text='The version requirements of this dependency.', max_length=256)),
                ('scope', models.CharField(blank=True, help_text='The scope of this dependency, how it is used in a project.', max_length=64)),
                ('datasource_id', models.CharField(blank=True, help_text='The identifier for the datafile handler used to obtain this dependency.', max_length=64)),
                ('is_runtime', models.BooleanField(default=False, help_text='True if this dependency is a runtime dependency.')),
                ('is_optional', models.BooleanField(default=False, help_text='True if this dependency is an optional dependency')),
                ('is_resolved', models.BooleanField(default=False, help_text='True if this dependency version requirement has been pinned and this dependency points to an exact version.')),
                ('is_direct', models.BooleanField(default=False, help_text='True if this is a direct, first-level dependency relationship for a package.')),
                ('created_by', models.ForeignKey(editable=False, help_text='The application user who created the object.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_%(class)ss', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('dataspace', models.ForeignKey(editable=False, help_text='A Dataspace is an independent, exclusive set of DejaCode data, which can be either nexB master reference data or installation-specific data.', on_delete=django.db.models.deletion.PROTECT, to='dje.dataspace')),
                ('for_package', models.ForeignKey(blank=True, editable=False, help_text='The package that declares this dependency.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='declared_dependencies', to='component_catalog.package')),
                ('last_modified_by', dje.fields.LastModifiedByField(editable=False, help_text='The application user who last modified the object.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_%(class)ss', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependencies', to='product_portfolio.product')),
                ('resolved_to_package', models.ForeignKey(blank=True, editable=False, help_text='The resolved package for this dependency. If empty, it indicates the dependency is unresolved.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_from_dependencies', to='component_catalog.package')),
            ],
            options={
                'verbose_name': 'product dependency',
                'verbose_name_plural': 'product dependencies',
                'ordering': ['dependency_uid'],
                'indexes': [models.Index(fields=['scope'], name='product_por_scope_eb3e33_idx'), models.Index(fields=['is_runtime'], name='product_por_is_runt_3476a9_idx'), models.Index(fields=['is_optional'], name='product_por_is_opti_9b7ae0_idx'), models.Index(fields=['is_resolved'], name='product_por_is_reso_368f34_idx'), models.Index(fields=['is_direct'], name='product_por_is_dire_3abb9d_idx')],
                'unique_together': {('dataspace', 'uuid'), ('product', 'dependency_uid')},
            },
        ),
    ]
