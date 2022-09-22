"""
maps module defines the available type of maps for netcdfella. 
Currently geostationary basemap is supported.
"""

import numpy as np
from mpl_toolkits.basemap import Basemap


class GeoStationaryMap(Basemap):
    def __init__(self, name, resolution="i", latitude0=0):
        self.name = name
        self.resolution = resolution
        self.latitude0 = latitude0

    def set_sat_height(self, height):
        "adjust the height of the satellite or leave blank for default"
        self.satellite_height = height
        return self

    def set_sphere(self, sphere):
        "set the sphere dimensions or leave blank for default"
        self.sphere = sphere
        return self

    def create_map(self):
        "create the basemap based on your previous settings"
        Basemap.__init__(
            self,
            projection="geos",
            resolution=self.resolution,
            rsphere=self.sphere,
            satellite_height=self.satellite_height,
            lat_0=self.latitude0,
            lon_0=0
        )
        return self

    def draw(self, kind=None):
        """
        choose the kind of map to draw.
        available: "basic","blue_marbel"
        """
        if kind == "blue_marble":
            self.bluemarble()
        else:
            self.draw_basic_earth()

    def draw_basic_earth(self, land="Linen", ocean="#AFDCEC"):
        "draw a basic style Earth globe"
        self.drawcoastlines(zorder=1)
        self.drawcountries(zorder=2)
        self.drawlsmask(
            land_color=land, ocean_color=ocean, zorder=0
        )
        self.drawmeridians(np.arange(0, 360, 30))
        self.drawparallels(np.arange(-90, 90, 30))
