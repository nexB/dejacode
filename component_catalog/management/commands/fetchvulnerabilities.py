#
# Copyright (c) nexB Inc. and others. All rights reserved.
# DejaCode is a trademark of nexB Inc.
# SPDX-License-Identifier: AGPL-3.0-only
# See https://github.com/nexB/dejacode for support or download.
# See https://aboutcode.org for more information about AboutCode FOSS projects.
#

from django.core.management.base import CommandError

from component_catalog.vulnerabilities import fetch_from_vulnerablecode
from dejacode_toolkit.vulnerablecode import VulnerableCode
from dje.management.commands import DataspacedCommand

# TODO: Retry failures -> log those
# ERROR VulnerableCode [Exception] HTTPSConnectionPool(host='public.vulnerablecode.io',
# port=443): Read timed out. (read timeout=10)


class Command(DataspacedCommand):
    help = "Fetch vulnerabilities for the provided Dataspace"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--batch-size",
            type=int,
            default=50,
            help="Specifies the number of objects per requests to the VulnerableCode service",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            help="Request timeout in seconds",
        )

    def handle(self, *args, **options):
        super().handle(*args, **options)
        batch_size = options["batch_size"]
        timeout = options["timeout"]

        if not self.dataspace.enable_vulnerablecodedb_access:
            raise CommandError("VulnerableCode is not enabled on this Dataspace.")

        vulnerablecode = VulnerableCode(self.dataspace)
        if not vulnerablecode.is_configured():
            raise CommandError("VulnerableCode is not configured.")

        fetch_from_vulnerablecode(self.dataspace, batch_size, timeout, logger=self.stdout)
