from floodmodeller_api import XML2D

from pathlib import Path
from shapely.geometry import LineString
import geopandas as gpd
import pandas as pd
import math


class ComponentConverter:
    def __init__(self, folder: Path) -> None:
        self._folder = folder

    def update_file(self):
        raise NotImplementedError()


class ComponentConverter2D(ComponentConverter):
    def __init__(self, xml: XML2D, folder: Path, domain_name: str) -> None:
        super().__init__(folder)
        self._xml = xml
        self._domain_name = domain_name


class ComputationalAreaConverter(ComponentConverter2D):

    _xll: float
    _yll: float
    _rotation: int

    def __init__(
        self,
        xml: XML2D,
        folder: Path,
        domain_name: str,
        dx: float,
        lx_ly: tuple,
        all_areas: gpd.GeoDataFrame,
    ) -> None:

        super().__init__(xml, folder, domain_name)

        self._dx = dx
        self._nrows = int(lx_ly[0] / self._dx)
        self._ncols = int(lx_ly[1] / self._dx)
        self._active_area = Path.joinpath(folder, "active_area.shp")
        self._deactive_area = Path.joinpath(folder, "deactive_area.shp")

        (
            all_areas[all_areas["code"] == 1]
            .drop(columns="code")
            .to_file(self._active_area)
        )
        (
            all_areas[all_areas["code"] == 0]
            .drop(columns="code")
            .to_file(self._deactive_area)
        )

    def update_file(self) -> None:
        self._xml.domains[self._domain_name]["computational_area"] = {
            "xll": self._xll,
            "yll": self._yll,
            "dx": self._dx,
            "nrows": self._nrows,
            "ncols": self._ncols,
            "active_area": self._active_area,
            "deactive_area": self._deactive_area,
            "rotation": self._rotation,
        }
        self._xml.update()


class LocLineConverter(ComputationalAreaConverter):
    def __init__(
        self,
        xml: XML2D,
        folder: Path,
        domain_name: str,
        dx: float,
        lx_ly: tuple,
        all_areas: gpd.GeoDataFrame,
        loc_line: LineString,
    ) -> None:
        super().__init__(xml, folder, domain_name, dx, lx_ly, all_areas)

        x1, y1 = loc_line.coords[0]
        x2, y2 = loc_line.coords[1]
        self._xll = x1
        self._yll = y1

        theta_rad = math.atan2(y2 - y1, x2 - x1)
        if theta_rad < 0:
            theta_rad += 2 * math.pi
        self._rotation = round(math.degrees(theta_rad))


class TopographyConverter(ComponentConverter2D):
    def __init__(
        self, xml: XML2D, folder: Path, domain_name: str, raster: Path
    ) -> None:
        super().__init__(xml, folder, domain_name)
        self._path = str(raster)

    def update_file(self) -> None:
        self._xml.domains[self._domain_name]["topography"] = self._path
        self._xml.update()


class RoughnessConverter(ComponentConverter2D):
    def __init__(
        self,
        xml: XML2D,
        folder: Path,
        domain_name: str,
        roughness_type: str,
        law: str,
        material: gpd.GeoDataFrame,
        mapping: pd.DataFrame
    ) -> None:
        super().__init__(xml, folder, domain_name)
        self._type = roughness_type
        self._law = law
        self._value = Path.joinpath(folder, "roughness.shp")
        
        (
            material
            .merge(mapping, left_on="material", right_on="Material ID")[["Manning's n", "geometry"]]
            .to_file(self._value)
        )

    def update_file(self) -> None:
        self._xml.domains[self._domain_name]["roughness"] = [{
            "type": self._type,
            "law": self._law,
            "value": self._value,
        }]
        self._xml.update()
