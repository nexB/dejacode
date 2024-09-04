#
# Copyright (c) nexB Inc. and others. All rights reserved.
# DejaCode is a trademark of nexB Inc.
# SPDX-License-Identifier: AGPL-3.0-only
# See https://github.com/aboutcode-org/dejacode for support or download.
# See https://aboutcode.org for more information about AboutCode FOSS projects.
#

from django.urls import path

from vulnerabilities.views import VulnerabilityListView

urlpatterns = [
    path("", VulnerabilityListView.as_view(), name="vulnerability_list"),
]
