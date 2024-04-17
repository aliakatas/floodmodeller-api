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

flags = {
    "DATAFILE": "ISIS Event Header",
    "TITLE": "ISIS Event Header",
    "PATH": "ISIS Event Header",
    "RESULTS": "ISIS Event Header",
    "SUBTITLE": "ISIS Event Details",
    "INITIALCONDITIONS": "ISIS Event Details",
    "OUTPUTADAPTIVETIMESTEPFILE": "ISIS Event Details",
    "INPUTADAPTIVETIMESTEPFILE": "ISIS Event Details",
    "OUTPUTUICFILENAME": "ISIS Event Details",
    "UPDATINGINITIALCONDITIONS": "ISIS Event Details",
    "UPDATINGZZN": "ISIS Event Details",
    "SNAPSHOTTIME": "ISIS Event Details",
    "SNAPSHOTFILE": "ISIS Event Details",
    "UNUPDATEDSNAPSHOTTIME": "ISIS Event Details",
    "UNUPDATEDSNAPSHOTFILE": "ISIS Event Details",
    "UPDATESEDIMENTTIME": "ISIS Event Details",
    "UPDATESEDIMENTFILE": "ISIS Event Details",
    "EVENTDATA": "ISIS Event Details",
    "2DPACKAGERPATH": "ISIS Event Details",
    "2DFILE": "ISIS Event Details",
    "SWMMCONTROLFILE": "ISIS Event Details",
    "SWMMLINKFILE": "ISIS Event Details",
    "2DFLOW": "ISIS Event Details",
    "LINKFLOW": "ISIS Event Details",
    "RUNTYPE": "ISIS Event Details",
    "START": "ISIS Event Details",
    "OTTA": "ISIS Event Details",
    "WRITEUPDATINGINITIALCONDITIONS": "ISIS Event Details",
    "DESTROYINVALIDUICFILE": "ISIS Event Details",
    "UPDATINGCOLDSTART": "ISIS Event Details",
    "VOLUMEOUTPUTINTERVAL": "ISIS Event Details",
    "FINISH": "ISIS Event Details",
    "TIMEZERO": "ISIS Event Details",
    "TIMESTEP": "ISIS Event Details",
    "INITIALTIMESTEP": "ISIS Event Details",
    "MINIMUMTIMESTEP": "ISIS Event Details",
    "MAXIMUMTIMESTEP": "ISIS Event Details",
    "SAVEINTERVAL": "ISIS Event Details",
    "WARMUPTIME": "ISIS Event Details",
    "QUALITY": "ISIS Event Details",
    "VARIABLEVALUES": "ISIS Event Details",
    "MATRIXINFORMATION": "ISIS Event Details",
    "UNITDATASTORE": "ISIS Event Details",
    "SINGULARITYCHECK": "ISIS Event Details",
    "CONVERGENCE": "ISIS Event Details",
    "TEMPORARYRESULTS": "ISIS Event Details",
    "OUTPUTGXYERRORS": "ISIS Event Details",
    "OUTPUTUNITSUMMARY": "ISIS Event Details",
    "OUTPUTCONVERGENCEPLOTBMP": "ISIS Event Details",
    "CONTROLUNITOUTPUTS": "ISIS Event Details",
    "CONTROLLERTIMESTEP": "ISIS Event Details",
    "CONTROLTIMESTEP": "ISIS Event Details",
    "CONTROLLERSAVEINTERVAL": "ISIS Event Details",
    "CONTROLLEROUTPUTINTERVAL": "ISIS Event Details",
    "INTERACTIVECONTROLLERTUNING": "ISIS Event Details",
    "CONTROLLERTUNINGTIMESTEP": "ISIS Event Details",
    "SEDIMENT": "ISIS Event Details",
    "ADAPTIVETIMESTEP": "ISIS Event Details",
    "AUTOSHUTDOWN": "ISIS Event Details",
    "TRANSCRITICAL": "ISIS Event Details",
    "SLOT": "ISIS Event Details",
    "CONDUITTOPSLOT": "ISIS Event Details",
    "CONDUITBOTTOMSLOT": "ISIS Event Details",
    "BOTTOMSLOTDH": "ISIS Event Details",
    "BOTTOMSLOTDEPTH": "ISIS Event Details",
    "TOPSLOTDH": "ISIS Event Details",
    "TOPSLOTHEIGHT": "ISIS Event Details",
    "DECREASINGCONVEYANCE": "ISIS Event Details",
    "SUPPRESSWINDOWSOUTPUT": "ISIS Event Details",
    "OUTPUTBREACHPROFILES": "ISIS Event Details",
    "SPECIFYGLOBALSLOTROUGHNESS": "ISIS Event Details",
    "ENFORCEINCREASINGCONVEYANCE": "ISIS Event Details",
    "RELAXDRYCHANNELS": "ISIS Event Details",
    "CESTESTING": "ISIS Event Details",
    "EXTRATIMESTEPS": "ISIS Event Details",
    "OUTPUTVOLUMES": "ISIS Event Details",
    "OUTPUTTIMEZERO": "ISIS Event Details",
    "USEPARDISOSOLVER": "ISIS Event Details",
    "LARGERESULTSCHECK": "ISIS Event Details",
    "2DDOUBLEPRECISION": "ISIS Event Details",
    "FORCEPUMPCURVE": "ISIS Event Details",
    "OVERRIDEDEACTIVATIONMARKERS": "ISIS Event Details",
    "OUTPUTMAXMINMEAN": "ISIS Event Details",
    "SETLOWERPRIORITY": "ISIS Event Details",
    "WRITEERF": "ISIS Event Details",
    "QUICKSMOOTH": "ISIS Event Details",
    "QUICKNORMDEPTH": "ISIS Event Details",
    "RESRIVERVOLUME": "ISIS Event Details",
    "STRUCTUREVELOCITY": "ISIS Event Details",
    "WETTEDPERIMETER": "ISIS Event Details",
    "WETTEDAREA": "ISIS Event Details",
    "SURFACEAREA": "ISIS Event Details",
    "MAXSTAGE": "ISIS Event Details",
    "MEANSTAGE": "ISIS Event Details",
    "MAXFLOW": "ISIS Event Details",
    "MEANFLOW": "ISIS Event Details",
    "CONVEYANCEVALUE": "ISIS Event Details",
    "DQCONVERGENCEVALUE": "ISIS Event Details",
    "DHCONVERGENCEVALUE": "ISIS Event Details",
    "SLOTAREA": "ISIS Event Details",
    "SLOTVOLUME": "ISIS Event Details",
    "RULENUMBER": "ISIS Event Details",
    "PUMPDATA": "ISIS Event Details",
    "LEVEEDATA": "ISIS Event Details",
    "STREAMPOWERPERUNITWIDTH": "ISIS Event Details",
    "STREAMPOWER": "ISIS Event Details",
    "SHEARSTRESS": "ISIS Event Details",
    "STRUCTURECOEFFICIENTS": "ISIS Event Details",
    "RESERVOIRMETHOD": "ISIS Event Details",
    "WARMUP": "ISIS Event Details",
    "ECHOZZD": "ISIS Event Details",
    "ECHODIAGNOSTICS": "ISIS Event Details",
    "UPDATINGDIAGNOSTICS": "ISIS Event Details",
    "IGNOREDIVERGENCE": "ISIS Event Details",
    "FORCEREFACTORISATION": "ISIS Event Details",
    "FORCEREFRESH": "ISIS Event Details",
    "REFRESHLEVEL": "ISIS Event Details",
    "ALPHA": "ISIS Event Details",
    "DFLOOD": "ISIS Event Details",
    "DFLOODB": "ISIS Event Details",
    "REFINEBRIDGESECPROPS": "ISIS Event Details",
    "HTOL": "ISIS Event Details",
    "MAXITR": "ISIS Event Details",
    "MINITR": "ISIS Event Details",
    "QTOL": "ISIS Event Details",
    "THETA": "ISIS Event Details",
    "SCONMX": "ISIS Event Details",
    "DLTMAX": "ISIS Event Details",
    "DILMAX": "ISIS Event Details",
    "SWOP": "ISIS Event Details",
    "WEIGHT": "ISIS Event Details",
    "NSBINT": "ISIS Event Details",
    "AVITR": "ISIS Event Details",
    "PSWIDE": "ISIS Event Details",
    "PSDEEP": "ISIS Event Details",
    "LARGESTEXPECTEDQ": "ISIS Event Details",
    "LARGESTEXPECTEDH": "ISIS Event Details",
    "LAUNCHDOUBLEPRECISIONVERSION": "ISIS Event Details",
    "NUMTHREADS": "ISIS Event Details",
    "PSTRUEPERIMETER": "ISIS Event Details",
    "PCMXVD": "ISIS Event Details",
    "UNITANGSHARP": "ISIS Event Details",
    "MINBEDSLOPE": "ISIS Event Details",
    "FROUDELOWER": "ISIS Event Details",
    "FROUDEUPPER": "ISIS Event Details",
    "MINIMUMDEPTH": "ISIS Event Details",
    "DIRECTCONVERGENCE": "ISIS Event Details",
    "TEMPERATURE": "ISIS Event Details",
    "PIVOTALCHOICE": "ISIS Event Details",
    "MATRIXDUMMY": "ISIS Event Details",
    "NEWMATRIXDUMMY": "ISIS Event Details",
    "SLOTROUGHNESS": "ISIS Event Details",
    "DRYLOWER": "ISIS Event Details",
    "DRYUPPER": "ISIS Event Details",
    "RESERVOIREMPTYFACTOR": "ISIS Event Details",
    "DIRECTMAXITERS": "ISIS Event Details",
    "DIRECTSMALLPOSITIVE": "ISIS Event Details",
    "DIRECTMAXNEGSPLITS": "ISIS Event Details",
    "SPILLTHRESHOLD": "ISIS Event Details",
    "DHLINEARISE": "ISIS Event Details",
    "OVERTOPTRANSITIONDEPTH": "ISIS Event Details",
    "LEVEETRANSITIONDEPTH": "ISIS Event Details",
    "FLOODPLAINDEADSTORAGEFACTOR": "ISIS Event Details",
    "MOMENTUMDADXIMPLICIT": "ISIS Event Details",
    "MAXATTENUATION": "ISIS Event Details",
    "MINATTENUATION": "ISIS Event Details",
    "MATHRULES": "ISIS Event Details",
    "RULESATTIMEZERO": "ISIS Event Details",
    "RULESONFIRSTITERATION": "ISIS Event Details",
    "RESETTIMESAFTERPOS": "ISIS Event Details",
    "DEFAULTSATVERSION": "ISIS Event Details",
    "DEFAULTTOZZS": "ISIS Event Details",
    "ICSFROM": "ISIS Event Details",
    "CES_DEPTH_INTERVALS": "ISIS Event Details",
    "CES_EDDY_VISCOSITY": "ISIS Event Details",
    "CES_MIN_DEPTH": "ISIS Event Details",
    "CES_NO_PANELS": "ISIS Event Details",
    "CES_RELAXATION": "ISIS Event Details",
    "CES_TEMPERATURE": "ISIS Event Details",
    "CES_MAX_ITERATIONS": "ISIS Event Details",
    "CES_HYT_MULTIPLIER": "ISIS Event Details",
    "CES_CONVERGENCE_TOLERANCE": "ISIS Event Details",
    "CES_ROUGHNESS": "ISIS Event Details",
    "2DTIMESTEP": "ISIS Event Details",
    "2DSYNCHPC": "ISIS Event Details",
    "TUFLOW202010": "ISIS Event Details",
    "2DSCHEME": "ISIS Event Details",
    "2DOPTIONS": "ISIS Event Details",
    "2DCORRECTOR": "ISIS Event Details",
    "OUTPUTROLLINGZZN": "ISIS Event Details",
    "ROLLINGZZNSTARTTIME": "ISIS Event Details",
    "ROLLINGZZNTIMESTEPS": "ISIS Event Details",
    "SOLVEDHEQUALSZEROATSTART": "ISIS Event Details",
    "USEFPSMODULARLIMIT": "ISIS Event Details",
    "USEREMOTEQ": "ISIS Event Details",
    "THETA_WEIGHT_AVERAGES": "ISIS Event Details",
    "USE_CUNGE_ET_AL_3_97": "ISIS Event Details",
    "USE_CUNGE_ET_AL_3_85B": "ISIS Event Details",
    "DROP_DQ_DT": "ISIS Event Details",
    "US_K_WEIGHTING": "ISIS Event Details",
    "THETA_WEIGHT_SF": "ISIS Event Details",
    "ADD_BASE_FLOW": "ISIS Event Details",
    "RAINSCALING1": "Boundary Adjustments",
    "FLOWSCALING1": "Boundary Adjustments",
    "STORMDURATION1": "Boundary Adjustments",
    "RETURNPERIOD1": "Boundary Adjustments",
    "USERERAINSCALING1": "Boundary Adjustments",
    "USERRRAINSCALING1": "Boundary Adjustments",
    "USEQTFLOWSCALING1": "Boundary Adjustments",
    "USERRFLOWSCALING1": "Boundary Adjustments",
    "MMMSTART": "ISIS Event Details",
    "MMMFINISH": "ISIS Event Details",
    "OVERRIDEURBANTIMES": "ISIS Event Details",
    "NOOFFLOWTIMEPROFILES": "Flow Time Profiles",
    "NOOFFLOWTIMESERIES": "Flow Time Profiles",
    "FLOWTIMEPROFILE1": "Flow Time Profiles",
    "FLOWTIMEPROFILE2": "Flow Time Profiles",
    "FLOWTIMEPROFILE3": "Flow Time Profiles",
    "FLOWTIMEPROFILE4": "Flow Time Profiles",
    "FLOWTIMEPROFILE5": "Flow Time Profiles",
    "FLOWTIMEPROFILE6": "Flow Time Profiles",
    "FLOWTIMEPROFILE7": "Flow Time Profiles",
    "FLOWTIMEPROFILE8": "Flow Time Profiles",
    "FLOWTIMEPROFILE9": "Flow Time Profiles",
    "FLOWTIMEPROFILE10": "Flow Time Profiles",
    "FLOWTIMEPROFILE11": "Flow Time Profiles",
    "FLOWTIMEPROFILE12": "Flow Time Profiles",
    "FLOWTIMEPROFILE13": "Flow Time Profiles",
    "FLOWTIMEPROFILE14": "Flow Time Profiles",
    "FLOWTIMEPROFILE15": "Flow Time Profiles",
    "FLOWTIMEPROFILE16": "Flow Time Profiles",
    "FLOWTIMEPROFILE17": "Flow Time Profiles",
    "FLOWTIMEPROFILE18": "Flow Time Profiles",
    "FLOWTIMEPROFILE19": "Flow Time Profiles",
    "FLOWTIMEPROFILE20": "Flow Time Profiles",
}
