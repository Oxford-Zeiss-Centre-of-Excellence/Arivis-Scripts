# coding: utf-8
#
# NAME: FIJi ROI Loader
# FILE: object_import                         
# REVISION : 1.0.0 - 2024-03-13
# AUTHOR : Jacky Ka Long Ko (Oxford-ZEISS Centre of Excellence)
# Copyright(c) 2024 University of Oxford, UK. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
# PURPOSE : 
# Tested for V4d Release : 4.0

import arivis
import arivis_core
import arivis_objects
import arivis_parameter, arivis_operation

import numpy as np
from read_roi import read_roi_zip

@arivis_parameter.add_arivis_parameters(
        ROI_Path = arivis_parameter.param_file('G:/Fabi Data/X348_MRT68_1_ROI_CellShape.zip'),
        Repeat_Stack = True,
        # Tag = "Cell"
        )

@arivis_parameter.add_param_description(
    ROI_Path = 'Path to FIJI ROI File (.zip)',
    Repeat_Stack = "Repeat ROI polygons on all planes",
    # Tag = "Tag name for the ROI(s)"
    )

def main(ROI_Path,Repeat_Stack):
    context = arivis_operation.Operation.get_context()
    input_data = context.get_input()
    output_data = context.get_output()

    print("Reading FIJI zip ROI file from: {}".format(ROI_Path))
    rois = read_roi_zip(ROI_Path)

    for k, v in rois.items():
        points = []
        for id in range(v["n"]):
            points.append(arivis_core.Point2D(v["x"][id],v["y"][id]))
        polygon = arivis_objects.Polygon()
        polygon.set_contour(points)

        segment = arivis_objects.Segment()
        # segment.add_tag(Tag)
        if Repeat_Stack:
            for z in range(input_data.get_bounds().z1,input_data.get_bounds().z2+1):
                segment.add_polygon(polygon,z)
        else:
            segment.add_polygon(polygon,v["position"])
        output_data.add_object(segment)