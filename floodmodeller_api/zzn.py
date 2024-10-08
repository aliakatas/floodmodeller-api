"""
Flood Modeller Python API
Copyright (C) 2024 Jacobs U.K. Limited

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/.

If you have any query about this program or this License, please contact us at support@floodmodeller.com or write to the following
address: Jacobs UK Limited, Flood Modeller, Cottons Centre, Cottons Lane, London, SE1 2QG, United Kingdom.
"""

from __future__ import annotations

import ctypes as ct
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ._base import FMFile
from .to_from_json import to_json
from .util import handle_exception, is_windows


def get_reader() -> ct.CDLL:
    # Get zzn_dll path
    lib = "zzn_read.dll" if is_windows() else "libzzn_read.so"
    zzn_dll = Path(__file__).resolve().parent / "libs" / lib

    # Catch LD_LIBRARY_PATH error for linux
    try:
        return ct.CDLL(str(zzn_dll))
    except OSError as e:
        msg_1 = "libifport.so.5: cannot open shared object file: No such file or directory"
        if msg_1 in str(e):
            msg_2 = "Set LD_LIBRARY_PATH environment variable to be floodmodeller_api/lib"
            raise OSError(msg_2) from e
        raise


def get_associated_file(original_file: Path, new_suffix: str) -> Path:
    new_file = original_file.with_suffix(new_suffix)
    if not new_file.exists():
        msg = (
            f"Error: Could not find associated {new_suffix} file."
            f" Ensure that the {original_file.suffix} results"
            f" have an associated {new_suffix} file with matching name."
        )
        raise FileNotFoundError(msg)
    return new_file


def check_errstat(routine: str, errstat: int) -> None:
    if errstat != 0:
        msg = (
            f"Errstat from {routine} routine is {errstat}."
            f" See zzread_errorlog.txt for more information."
        )
        raise RuntimeError(msg)


def run_routines(filepath: Path, *, is_quality: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    reader = get_reader()
    zzl = get_associated_file(filepath, ".zzl")

    data: dict[str, Any] = {}
    meta: dict[str, Any] = {}

    meta["filepath"] = ct.create_string_buffer(bytes(str(filepath), "utf-8"), 255)
    meta["zzl_name"] = ct.create_string_buffer(bytes(str(zzl), "utf-8"), 255)

    # process zzl
    meta["model_title"] = ct.create_string_buffer(b"", 128)
    meta["nnodes"] = ct.c_int(0)
    meta["label_length"] = ct.c_int(0)
    meta["dt"] = ct.c_float(0.0)
    meta["timestep0"] = ct.c_int(0)
    meta["ltimestep"] = ct.c_int(0)
    meta["save_int"] = ct.c_float(0.0)
    meta["is_quality"] = ct.c_bool(is_quality)
    meta["nvars"] = ct.c_int(0)
    meta["tzero"] = (ct.c_int * 5)()
    meta["errstat"] = ct.c_int(0)
    reader.process_zzl(
        ct.byref(meta["zzl_name"]),
        ct.byref(meta["model_title"]),
        ct.byref(meta["nnodes"]),
        ct.byref(meta["label_length"]),
        ct.byref(meta["dt"]),
        ct.byref(meta["timestep0"]),
        ct.byref(meta["ltimestep"]),
        ct.byref(meta["save_int"]),
        ct.byref(meta["is_quality"]),
        ct.byref(meta["nvars"]),
        ct.byref(meta["tzero"]),
        ct.byref(meta["errstat"]),
    )
    check_errstat("process_zzl", meta["errstat"].value)

    # process labels
    meta["labels"] = (ct.c_char * meta["label_length"].value * meta["nnodes"].value)()
    reader.process_labels(
        ct.byref(meta["zzl_name"]),
        ct.byref(meta["nnodes"]),
        ct.byref(meta["label_length"]),
        ct.byref(meta["errstat"]),
    )
    check_errstat("process_labels", meta["errstat"].value)

    # get zz labels
    for i in range(meta["nnodes"].value):
        reader.get_zz_label(
            ct.byref(ct.c_int(i + 1)),
            ct.byref(meta["labels"][i]),
            ct.byref(meta["errstat"]),
        )
        check_errstat("get_zz_label", meta["errstat"].value)

    # preprocess zzn
    last_hr = (meta["ltimestep"].value - meta["timestep0"].value) * meta["dt"].value / 3600
    meta["output_hrs"] = (ct.c_float * 2)(0.0, last_hr)
    meta["aitimestep"] = (ct.c_int * 2)(meta["timestep0"].value, meta["ltimestep"].value)
    meta["isavint"] = (ct.c_int * 2)()
    reader.preprocess_zzn(
        ct.byref(meta["output_hrs"]),
        ct.byref(meta["aitimestep"]),
        ct.byref(meta["dt"]),
        ct.byref(meta["timestep0"]),
        ct.byref(meta["ltimestep"]),
        ct.byref(meta["save_int"]),
        ct.byref(meta["isavint"]),
    )

    # process zzn
    meta["node_ID"] = ct.c_int(-1)
    meta["savint_skip"] = ct.c_int(1)
    meta["savint_range"] = ct.c_int(
        int((meta["isavint"][1] - meta["isavint"][0]) / meta["savint_skip"].value),
    )
    nx = meta["nnodes"].value
    ny = meta["nvars"].value
    nz = meta["savint_range"].value + 1
    data["all_results"] = (ct.c_float * nx * ny * nz)()
    data["max_results"] = (ct.c_float * nx * ny)()
    data["min_results"] = (ct.c_float * nx * ny)()
    data["max_times"] = (ct.c_int * nx * ny)()
    data["min_times"] = (ct.c_int * nx * ny)()
    reader.process_zzn(
        ct.byref(meta["filepath"]),
        ct.byref(meta["node_ID"]),
        ct.byref(meta["nnodes"]),
        ct.byref(meta["is_quality"]),
        ct.byref(meta["nvars"]),
        ct.byref(meta["savint_range"]),
        ct.byref(meta["savint_skip"]),
        ct.byref(data["all_results"]),
        ct.byref(data["max_results"]),
        ct.byref(data["min_results"]),
        ct.byref(data["max_times"]),
        ct.byref(data["min_times"]),
        ct.byref(meta["errstat"]),
        ct.byref(meta["isavint"]),
    )
    check_errstat("process_zzn", meta["errstat"].value)

    # Convert useful metadata from C types into python types
    meta["dt"] = meta["dt"].value
    meta["nnodes"] = meta["nnodes"].value
    meta["save_int"] = meta["save_int"].value
    meta["nvars"] = meta["nvars"].value
    meta["savint_range"] = meta["savint_range"].value

    meta["filepath"] = meta["filepath"].value.decode()
    meta["labels"] = [label.value.decode().strip() for label in list(meta["labels"])]
    meta["model_title"] = meta["model_title"].value.decode()

    return data, meta


class ZZN(FMFile):
    """Reads and processes Flood Modeller 1D binary results format '.zzn'

    Args:
        zzn_filepath (str): Full filepath to model zzn file

    Output:
        Initiates 'ZZN' class object
    """

    _filetype: str = "ZZN"
    _suffix: str = ".zzn"

    @handle_exception(when="read")
    def __init__(
        self,
        zzn_filepath: str | Path | None = None,
        from_json: bool = False,
    ):
        if from_json:
            return

        FMFile.__init__(self, zzn_filepath)

        self.data, self.meta = run_routines(self._filepath, is_quality=False)

    def to_dataframe(  # noqa: PLR0911
        self,
        result_type: str = "all",
        variable: str = "all",
        include_time: bool = False,
        multilevel_header: bool = True,
    ) -> pd.Series | pd.DataFrame:
        """Loads zzn results to pandas dataframe object.

        Args:
            result_type (str, optional): {'all'} | 'max' | 'min'
                Define whether to return all timesteps or just max/min results. Defaults to 'all'.
            variable (str, optional): {'all'} | 'Flow' | 'Stage' | 'Froude' | 'Velocity' | 'Mode' | 'State'
                Specify a single output variable (e.g 'flow' or 'stage'). Defaults to 'all'.
            include_time (bool, optional):
                Whether to include the time of max or min results. Defaults to False.
            multilevel_header (bool, optional): If True, the returned dataframe will have multi-level column
                headers with the variable as first level and node label as second header. If False, the column
                names will be formatted "{node label}_{variable}". Defaults to True.

        Returns:
            pandas.DataFrame(): dataframe object of simulation results
        """
        nx = self.meta["nnodes"]
        ny = self.meta["nvars"]
        nz = self.meta["savint_range"] + 1
        result_type = result_type.lower()

        if result_type == "all":
            arr = np.array(self.data["all_results"])
            time_index = np.linspace(self.meta["output_hrs"][0], self.meta["output_hrs"][1], nz)
            vars_list = ["Flow", "Stage", "Froude", "Velocity", "Mode", "State"]
            if multilevel_header:
                col_names = [vars_list, self.meta["labels"]]
                df = pd.DataFrame(
                    arr.reshape(nz, nx * ny),
                    index=time_index,
                    columns=pd.MultiIndex.from_product(col_names),
                )
                df.index.name = "Time (hr)"
                if variable != "all":
                    return df[variable.capitalize()]

            else:
                col_names = [f"{node}_{var}" for var in vars_list for node in self.meta["labels"]]
                df = pd.DataFrame(arr.reshape(nz, nx * ny), index=time_index, columns=col_names)
                df.index.name = "Time (hr)"
                if variable != "all":
                    use_cols = [col for col in df.columns if col.endswith(variable.capitalize())]
                    return df[use_cols]
            return df

        if result_type in ("max", "min"):
            arr = np.array(self.data[f"{result_type}_results"]).transpose()
            node_index = self.meta["labels"]
            col_names = [
                result_type.capitalize() + lbl
                for lbl in [
                    " Flow",
                    " Stage",
                    " Froude",
                    " Velocity",
                    " Mode",
                    " State",
                ]
            ]
            df = pd.DataFrame(arr, index=node_index, columns=col_names)
            df.index.name = "Node Label"

            if include_time:
                times = np.array(self.data[f"{result_type}_times"]).transpose()
                # transform timestep into hrs
                times = ((times - self.meta["timestep0"]) * self.meta["dt"]) / 3600
                time_col_names = [name + " Time(hrs)" for name in col_names]
                time_df = pd.DataFrame(times, index=node_index, columns=time_col_names)
                time_df.index.name = "Node Label"
                df = pd.concat([df, time_df], axis=1)
                new_col_order = [x for y in list(zip(col_names, time_col_names)) for x in y]
                df = df[new_col_order]
                if variable != "all":
                    return df[
                        [
                            f"{result_type.capitalize()} {variable.capitalize()}",
                            f"{result_type.capitalize()} {variable.capitalize()} Time(hrs)",
                        ]
                    ]
                return df

            if variable != "all":
                return df[f"{result_type.capitalize()} {variable.capitalize()}"]
            return df

        raise ValueError(f'Result type: "{result_type}" not recognised')

    def export_to_csv(
        self,
        save_location: str | Path = "default",
        result_type: str = "all",
        variable: str = "all",
        include_time: bool = False,
    ) -> None:
        """Exports zzn results to CSV file.

        Args:
            save_location (str, optional): {default} | folder or file path
                Full or relative path to folder or csv file to save output csv, if no argument given or if set to 'default' then CSV will be saved in same location as ZZN file. Defaults to 'default'.
            result_type (str, optional): {all} | max | min
                Define whether to output all timesteps or just max/min results. Defaults to 'all'.
            variable (str, optional): {'all'} | 'Flow' | 'Stage' | 'Froude' | 'Velocity' | 'Mode' | 'State'
                Specify a single output variable (e.g 'flow' or 'stage'). Defaults to 'all'.
            include_time (bool, optional):
                Whether to include the time of max or min results. Defaults to False.

        Raises:
            Exception: Raised if result_type set to invalid option
        """
        if save_location == "default":
            save_location = Path(self.meta["zzn_name"]).with_suffix(".csv")
        else:
            save_location = Path(save_location)
            if not save_location.is_absolute():
                # for if relative folder path given
                save_location = Path(Path(self.meta["zzn_name"]).parent, save_location)

        if save_location.suffix != ".csv":  # Assumed to be pointing to a folder
            # Check if the folder exists, if not create it
            if not save_location.exists():
                Path.mkdir(save_location)
            save_location = Path(
                save_location,
                Path(self.meta["zzn_name"]).with_suffix(".csv").name,
            )

        elif not save_location.parent.exists():
            Path.mkdir(save_location.parent)

        result_type = result_type.lower()

        if result_type.lower() not in ["all", "max", "min"]:
            raise Exception(
                f" '{result_type}' is not a valid result type. Valid arguments are: 'all', 'max' or 'min' ",
            )

        df = self.to_dataframe(
            result_type=result_type,
            variable=variable,
            include_time=include_time,
        )
        df.to_csv(save_location)
        print(f"CSV saved to {save_location}")

    def to_dict_of_dataframes(self, variable: str = "all") -> dict:
        """Loads zzn results to a dictionary of pandas dataframe objects.

        Args:
            variable (str, optional): {'all'} | 'Flow' | 'Stage' | 'Froude' | 'Velocity' | 'Mode' | 'State'
                Specify a single output variable (e.g 'flow' or 'stage') or any combination passed as comma separated
                variable names. Defaults to 'all'.

        Returns:
            dict: dictionary of dataframe object of simulation results, keys corresponding to variables.
        """
        nx = self.meta["nnodes"]
        ny = self.meta["nvars"]
        nz = self.meta["savint_range"] + 1
        output = {}

        arr = np.array(self.data["all_results"])
        time_index = np.linspace(self.meta["output_hrs"][0], self.meta["output_hrs"][1], nz)

        vars_list = ["Flow", "Stage", "Froude", "Velocity", "Mode", "State"]

        col_names = self.meta["labels"]
        temp_arr = np.reshape(arr, (nz, ny, nx))

        for i, var in enumerate(vars_list):
            output[var] = pd.DataFrame(temp_arr[:, i, :], index=time_index, columns=col_names)
            output[var].index.name = "Time (hr)"

        output["Time (hr)"] = time_index

        if variable != "all":
            input_vars = variable.split(",")
            for i, var in enumerate(input_vars):
                input_vars[i] = var.strip().capitalize()
                if input_vars[i] not in vars_list:
                    raise Exception(
                        f" '{input_vars[i]}' is not a valid variable name. Valid arguments are: {vars_list} ",
                    )

            for var in vars_list:
                if var not in input_vars:
                    del output[var]
        return output

    def to_json(
        self,
        result_type: str = "all",
        variable: str = "all",
        include_time: bool = False,
        multilevel_header: bool = True,
    ) -> str:
        """Loads zzn results to JSON object.

        Args:
            result_type (str, optional): {'all'} | 'max' | 'min'
                Define whether to return all timesteps or just max/min results. Defaults to 'all'.
            variable (str, optional): {'all'} | 'Flow' | 'Stage' | 'Froude' | 'Velocity' | 'Mode' | 'State'
                Specify a single output variable (e.g 'flow' or 'stage'). Defaults to 'all'.
            include_time (bool, optional):
                Whether to include the time of max or min results. Defaults to False.
            multilevel_header (bool, optional): If True, the returned dataframe will have multi-level column
                headers with the variable as first level and node label as second header. If False, the column
                names will be formatted "{node label}_{variable}". Defaults to True.

        Returns:
            str: A JSON string representing the ZZN results.
        """
        df = self.to_dataframe(result_type, variable, include_time, multilevel_header)
        return to_json(df)

    @classmethod
    def from_json(cls, json_string: str = ""):
        # Not possible
        raise NotImplementedError("It is not possible to build a ZZN class instance from JSON")
