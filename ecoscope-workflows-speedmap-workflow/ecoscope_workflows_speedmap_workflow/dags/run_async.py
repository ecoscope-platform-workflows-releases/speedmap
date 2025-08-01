# AUTOGENERATED BY ECOSCOPE-WORKFLOWS; see fingerprint in README.md for details
import json
import os

from ecoscope_workflows_core.graph import DependsOn, Graph, Node

from ecoscope_workflows_core.tasks.config import set_workflow_details
from ecoscope_workflows_core.tasks.io import set_er_connection
from ecoscope_workflows_core.tasks.filter import set_time_range
from ecoscope_workflows_ext_ecoscope.tasks.io import get_subjectgroup_observations
from ecoscope_workflows_core.tasks.groupby import set_groupers
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import process_relocations
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import (
    relocations_to_trajectory,
)
from ecoscope_workflows_core.tasks.transformation import add_temporal_index
from ecoscope_workflows_core.tasks.transformation import map_columns
from ecoscope_workflows_ext_ecoscope.tasks.transformation import apply_classification
from ecoscope_workflows_core.tasks.groupby import split_groups
from ecoscope_workflows_ext_ecoscope.tasks.results import set_base_maps
from ecoscope_workflows_core.tasks.transformation import sort_values
from ecoscope_workflows_ext_ecoscope.tasks.transformation import apply_color_map
from ecoscope_workflows_core.tasks.transformation import map_values_with_unit
from ecoscope_workflows_ext_ecoscope.tasks.results import create_polyline_layer
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_ecomap
from ecoscope_workflows_core.tasks.io import persist_text
from ecoscope_workflows_core.tasks.results import create_map_widget_single_view
from ecoscope_workflows_core.tasks.results import merge_widget_views
from ecoscope_workflows_core.tasks.results import gather_dashboard

from ..params import Params


def main(params: Params):
    params_dict = json.loads(params.model_dump_json(exclude_unset=True))

    dependencies = {
        "workflow_details": [],
        "er_client_name": [],
        "time_range": [],
        "subject_obs": ["er_client_name", "time_range"],
        "groupers": [],
        "subject_reloc": ["subject_obs"],
        "subject_traj": ["subject_reloc"],
        "traj_add_temporal_index": ["subject_traj", "groupers"],
        "rename_grouper_columns": ["traj_add_temporal_index"],
        "classify_traj_speed": ["rename_grouper_columns"],
        "split_subject_traj_groups": ["classify_traj_speed", "groupers"],
        "base_map_defs": [],
        "sort_traj_speed": ["split_subject_traj_groups"],
        "colormap_traj_speed": ["sort_traj_speed"],
        "speedmap_legend_with_unit": ["colormap_traj_speed"],
        "traj_map_layers": ["speedmap_legend_with_unit"],
        "traj_ecomap": ["base_map_defs", "traj_map_layers"],
        "ecomap_html_urls": ["traj_ecomap"],
        "traj_map_widgets_single_views": ["ecomap_html_urls"],
        "traj_grouped_map_widget": ["traj_map_widgets_single_views"],
        "speedmap_dashboard": [
            "workflow_details",
            "traj_grouped_map_widget",
            "time_range",
            "groupers",
        ],
    }

    nodes = {
        "workflow_details": Node(
            async_task=set_workflow_details.validate()
            .handle_errors(task_instance_id="workflow_details")
            .set_executor("lithops"),
            partial=(params_dict.get("workflow_details") or {}),
            method="call",
        ),
        "er_client_name": Node(
            async_task=set_er_connection.validate()
            .handle_errors(task_instance_id="er_client_name")
            .set_executor("lithops"),
            partial=(params_dict.get("er_client_name") or {}),
            method="call",
        ),
        "time_range": Node(
            async_task=set_time_range.validate()
            .handle_errors(task_instance_id="time_range")
            .set_executor("lithops"),
            partial={
                "time_format": "%d %b %Y %H:%M:%S %Z",
            }
            | (params_dict.get("time_range") or {}),
            method="call",
        ),
        "subject_obs": Node(
            async_task=get_subjectgroup_observations.validate()
            .handle_errors(task_instance_id="subject_obs")
            .set_executor("lithops"),
            partial={
                "client": DependsOn("er_client_name"),
                "time_range": DependsOn("time_range"),
                "raise_on_empty": True,
                "include_details": False,
            }
            | (params_dict.get("subject_obs") or {}),
            method="call",
        ),
        "groupers": Node(
            async_task=set_groupers.validate()
            .handle_errors(task_instance_id="groupers")
            .set_executor("lithops"),
            partial=(params_dict.get("groupers") or {}),
            method="call",
        ),
        "subject_reloc": Node(
            async_task=process_relocations.validate()
            .handle_errors(task_instance_id="subject_reloc")
            .set_executor("lithops"),
            partial={
                "observations": DependsOn("subject_obs"),
                "relocs_columns": [
                    "groupby_col",
                    "fixtime",
                    "junk_status",
                    "geometry",
                    "extra__subject__name",
                    "extra__subject__subject_subtype",
                    "extra__subject__sex",
                ],
                "filter_point_coords": [
                    {"x": 180.0, "y": 90.0},
                    {"x": 0.0, "y": 0.0},
                    {"x": 1.0, "y": 1.0},
                ],
            }
            | (params_dict.get("subject_reloc") or {}),
            method="call",
        ),
        "subject_traj": Node(
            async_task=relocations_to_trajectory.validate()
            .handle_errors(task_instance_id="subject_traj")
            .set_executor("lithops"),
            partial={
                "relocations": DependsOn("subject_reloc"),
            }
            | (params_dict.get("subject_traj") or {}),
            method="call",
        ),
        "traj_add_temporal_index": Node(
            async_task=add_temporal_index.validate()
            .handle_errors(task_instance_id="traj_add_temporal_index")
            .set_executor("lithops"),
            partial={
                "df": DependsOn("subject_traj"),
                "time_col": "segment_start",
                "groupers": DependsOn("groupers"),
                "cast_to_datetime": True,
                "format": "mixed",
            }
            | (params_dict.get("traj_add_temporal_index") or {}),
            method="call",
        ),
        "rename_grouper_columns": Node(
            async_task=map_columns.validate()
            .handle_errors(task_instance_id="rename_grouper_columns")
            .set_executor("lithops"),
            partial={
                "df": DependsOn("traj_add_temporal_index"),
                "drop_columns": [],
                "retain_columns": [],
                "rename_columns": {"extra__name": "subject_name"},
            }
            | (params_dict.get("rename_grouper_columns") or {}),
            method="call",
        ),
        "classify_traj_speed": Node(
            async_task=apply_classification.validate()
            .handle_errors(task_instance_id="classify_traj_speed")
            .set_executor("lithops"),
            partial={
                "df": DependsOn("rename_grouper_columns"),
                "input_column_name": "speed_kmhr",
                "output_column_name": "speed_bins",
                "classification_options": {"scheme": "equal_interval", "k": 6},
                "label_options": {"label_ranges": False, "label_decimals": 1},
            }
            | (params_dict.get("classify_traj_speed") or {}),
            method="call",
        ),
        "split_subject_traj_groups": Node(
            async_task=split_groups.validate()
            .handle_errors(task_instance_id="split_subject_traj_groups")
            .set_executor("lithops"),
            partial={
                "df": DependsOn("classify_traj_speed"),
                "groupers": DependsOn("groupers"),
            }
            | (params_dict.get("split_subject_traj_groups") or {}),
            method="call",
        ),
        "base_map_defs": Node(
            async_task=set_base_maps.validate()
            .handle_errors(task_instance_id="base_map_defs")
            .set_executor("lithops"),
            partial=(params_dict.get("base_map_defs") or {}),
            method="call",
        ),
        "sort_traj_speed": Node(
            async_task=sort_values.validate()
            .handle_errors(task_instance_id="sort_traj_speed")
            .set_executor("lithops"),
            partial={
                "column_name": "speed_bins",
                "ascending": True,
                "na_position": "last",
            }
            | (params_dict.get("sort_traj_speed") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("split_subject_traj_groups"),
            },
        ),
        "colormap_traj_speed": Node(
            async_task=apply_color_map.validate()
            .handle_errors(task_instance_id="colormap_traj_speed")
            .set_executor("lithops"),
            partial={
                "input_column_name": "speed_bins",
                "output_column_name": "speed_bins_colormap",
                "colormap": [
                    "#1a9850",
                    "#91cf60",
                    "#d9ef8b",
                    "#fee08b",
                    "#fc8d59",
                    "#d73027",
                ],
            }
            | (params_dict.get("colormap_traj_speed") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("sort_traj_speed"),
            },
        ),
        "speedmap_legend_with_unit": Node(
            async_task=map_values_with_unit.validate()
            .handle_errors(task_instance_id="speedmap_legend_with_unit")
            .set_executor("lithops"),
            partial={
                "input_column_name": "speed_bins",
                "output_column_name": "speed_bins_formatted",
                "original_unit": "km/h",
                "new_unit": "km/h",
                "decimal_places": 1,
            }
            | (params_dict.get("speedmap_legend_with_unit") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["df"],
                "argvalues": DependsOn("colormap_traj_speed"),
            },
        ),
        "traj_map_layers": Node(
            async_task=create_polyline_layer.validate()
            .handle_errors(task_instance_id="traj_map_layers")
            .set_executor("lithops"),
            partial={
                "layer_style": {"color_column": "speed_bins_colormap"},
                "legend": {
                    "label_column": "speed_bins_formatted",
                    "color_column": "speed_bins_colormap",
                },
                "tooltip_columns": ["subject_name", "subject_subtype", "speed_kmhr"],
            }
            | (params_dict.get("traj_map_layers") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["geodataframe"],
                "argvalues": DependsOn("speedmap_legend_with_unit"),
            },
        ),
        "traj_ecomap": Node(
            async_task=draw_ecomap.validate()
            .handle_errors(task_instance_id="traj_ecomap")
            .set_executor("lithops"),
            partial={
                "tile_layers": DependsOn("base_map_defs"),
                "north_arrow_style": {"placement": "top-left"},
                "legend_style": {"placement": "bottom-right"},
                "static": False,
                "title": None,
                "max_zoom": 20,
            }
            | (params_dict.get("traj_ecomap") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["geo_layers"],
                "argvalues": DependsOn("traj_map_layers"),
            },
        ),
        "ecomap_html_urls": Node(
            async_task=persist_text.validate()
            .handle_errors(task_instance_id="ecomap_html_urls")
            .set_executor("lithops"),
            partial={
                "root_path": os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            }
            | (params_dict.get("ecomap_html_urls") or {}),
            method="mapvalues",
            kwargs={
                "argnames": ["text"],
                "argvalues": DependsOn("traj_ecomap"),
            },
        ),
        "traj_map_widgets_single_views": Node(
            async_task=create_map_widget_single_view.validate()
            .handle_errors(task_instance_id="traj_map_widgets_single_views")
            .set_executor("lithops"),
            partial={
                "title": "Subject Group Speed Map",
            }
            | (params_dict.get("traj_map_widgets_single_views") or {}),
            method="map",
            kwargs={
                "argnames": ["view", "data"],
                "argvalues": DependsOn("ecomap_html_urls"),
            },
        ),
        "traj_grouped_map_widget": Node(
            async_task=merge_widget_views.validate()
            .handle_errors(task_instance_id="traj_grouped_map_widget")
            .set_executor("lithops"),
            partial={
                "widgets": DependsOn("traj_map_widgets_single_views"),
            }
            | (params_dict.get("traj_grouped_map_widget") or {}),
            method="call",
        ),
        "speedmap_dashboard": Node(
            async_task=gather_dashboard.validate()
            .handle_errors(task_instance_id="speedmap_dashboard")
            .set_executor("lithops"),
            partial={
                "details": DependsOn("workflow_details"),
                "widgets": DependsOn("traj_grouped_map_widget"),
                "time_range": DependsOn("time_range"),
                "groupers": DependsOn("groupers"),
            }
            | (params_dict.get("speedmap_dashboard") or {}),
            method="call",
        ),
    }
    graph = Graph(dependencies=dependencies, nodes=nodes)
    results = graph.execute()
    return results
