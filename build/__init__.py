"""
Maxalding document build module.

One shared template (build/template.py) defines fonts, header, logo and styling.
Generators produce the Creative Plan XLSX and the four .docx deliverables to the
exact rules in the System Prompt.
"""

from .build_all import build_all
from .creative_plan import build_creative_plan
from .video_ad_scripts import build_video_ad_scripts
from .vsl_script import build_vsl_script
from .landing_page import build_landing_page
from .crm_automation import build_crm_automation

__all__ = [
    "build_all",
    "build_creative_plan",
    "build_video_ad_scripts",
    "build_vsl_script",
    "build_landing_page",
    "build_crm_automation",
]
