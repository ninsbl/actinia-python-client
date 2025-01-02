#!/usr/bin/env python
"""Test cases for actinia STRDS management.

actinia-python-client is a python client for actinia - an open source REST
API for scalable, distributed, high performance processing of geographical
data that uses GRASS GIS for computational tasks.

Copyright (c) 2023 mundialis GmbH & Co. KG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann, Stefan Bøumentrath"
__copyright__ = "Copyright 2023-2024, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"


from actinia import Actinia
from actinia.strds import SpaceTimeRasterDataset

from .actinia_config import (
    ACTINIA_AUTH,
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    LOCATION_NAME,
    MAPSET_NAME,
    STRDS_NAME,
)

NEW_MAPSET_NAME = "new_test_mapset"
UPLOAD_RASTER_TIF = "../test_data/elevation.tif"
UPLOAD_RASTER_NAME = "test_raster"


class TestActiniaSpaceTimeRasterDatasets:
    """Test SpaceTimeRasterDatasets management."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up test environment."""
        cls.testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication(ACTINIA_AUTH[0], ACTINIA_AUTH[1])
        cls.testactinia.get_locations()
        cls.testactinia.locations[LOCATION_NAME].get_mapsets()
        cls.testactinia.locations[LOCATION_NAME].create_mapset(NEW_MAPSET_NAME)

    @classmethod
    def teardown_class(cls) -> None:
        """Tear down test environment."""
        if NEW_MAPSET_NAME in cls.testactinia.locations[LOCATION_NAME].mapsets:
            cls.testactinia.locations[LOCATION_NAME].delete_mapset(
                NEW_MAPSET_NAME,
            )

    def test_get_strds_info(self) -> None:
        """Test get_strds_info."""
        # get raster layers
        resp = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .create_strds(
                STRDS_NAME,
                "test title",
                "test description",
                "absolute",
            )
        )
        # register_raster_layer
        strds = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .strds
        )
        assert isinstance(strds, dict), "response is not a dictionary"
        assert STRDS_NAME in strds, f"STRDS '{STRDS_NAME}' is not in response"
        assert isinstance(
            strds[STRDS_NAME],
            SpaceTimeRasterDataset,
        ), "STRDS is not of type SpaceTimeRasterDataset"

        # Get STRDS info
        resp = strds[STRDS_NAME].get_info()
        assert isinstance(resp, dict), "response is not a dictionary"
        assert "cells" in resp, "response is not correct"
        assert resp["cells"] == "2025000", "response is not correct"
        assert resp["min"] == "55.57879", "response is not correct"
