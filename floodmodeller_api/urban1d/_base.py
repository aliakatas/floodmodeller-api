"""
Flood Modeller Python API
Copyright (C) 2022 Jacobs U.K. Limited

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. 

You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/.

If you have any query about this program or this License, please contact us at support@floodmodeller.com or write to the following 
address: Jacobs UK Limited, Flood Modeller, Cottons Centre, Cottons Lane, London, SE1 2QG, United Kingdom.
"""

""" Holds the base unit class for all FM 1D units Units """


class UrbanUnit:
    _unit = None
    _subtype = None
    _name = None

    def __init__(self, unit_block=None, **kwargs):
        if unit_block != None:
            self._read(unit_block)
        else:
            self._create_from_blank(**kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    # Update this bit
    def __repr__(self):
        if self._subtype is None:
            return (
                f"<floodmodeller_api UrbanUnit Class: {self._unit}(name={self._name})>"
            )

    def _create_from_blank(self):
        raise NotImplementedError(
            f"Creating new {self._unit} units is not yet supported by floodmodeller_api, only existing units can be read"
        )

    def __str__(self):
        return self._write()

    def _read(self):
        raise NotImplementedError

    def _write(self):
        raise NotImplementedError


class UrbanSubsection:
    _name = None
    _urban_unit_class = None

    def __init__(self, subsection_block=None, **kwargs):
        if subsection_block != None:
            self._read(subsection_block)
        else:
            self._create_from_blank(**kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def __repr__(self):
        return f"<floodmodeller_api UrbanSubsection Class: {self._attribute}>"

    def _create_from_blank(self):
        raise NotImplementedError(
            f"Creating new {self._name} subsections is not yet supported by floodmodeller_api, only existing subsections can be read"
        )

    def __str__(self):
        return "\n".join(self._write())

    def _read(self, block):

        setattr(self, self._attribute, {})
        units = getattr(self, self._attribute)

        self._struct = []

        for line in block[1:]:  # first line is subsection name
            if line.strip() != "" and not line.startswith(";"):
                unit = self._urban_unit_class(line)
                units[unit.name] = unit
                self._struct.append(unit)

            else:
                self._struct.append(line)

    def _write(self):

        block = []

        if self._attribute == "raingauges":
            # handle required miss-spelling of raingauge in subsection header
            block.append("[" + "RAINGAGES" + "]")

        else:
            block.append("[" + self._attribute.upper() + "]")

        for line in self._struct:
            if isinstance(line, self._urban_unit_class):
                block.append(line._write())
            else:
                block.append(line)

        units = getattr(self, self._attribute)

        for name, unit in units.copy().items():
            if name != unit.name:
                # Miss-match found
                # check that it is not an existing label in units
                if unit.name in units:
                    raise Exception(
                        f'Error: Cannot update label "{name}" to "{unit.name}" beacuase "{unit.name}" already exists in the {self._attribute} subsection'
                    )

                units[unit.name] = unit
                del units[name]

                # TODO: update label in any other units where required.

        return block
