# Copyright 2017-24 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Base Tier Validation for state",
    "summary": "Implement a validation process based on tiers  for state.",
    "version": '1.0',
    "maintainers": ["LoisRForgeFlow"],
    "category": "Tools",
    "website": "https://github.com/OCA/server-ux",
    "author": "BWCS PMO",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["mail", "base_tier_validation"],
    "data": [
        "views/tier_definition_view.xml",
    ],
    'demo': [
        "demo/tier_definition_dcopco.xml",       
    ],
}
