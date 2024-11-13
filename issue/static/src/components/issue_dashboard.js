/** @odoo-module */
import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks";

import { ChartRenderer1 } from "./pco_kanbanpie/pco_pie"
import { ChartRendererdco } from "./dco_kanbanpie/dco_pie"
import { ChartRendererprj } from "./prj_kanbanbar/prj_bar"
import { ChartRenderertask } from "./task_kanbanbar/task_bar"
import { ChartRendererisutag } from "./isue_kanbanpie/issuetag_pie"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, UseRef, onMounted } = owl

export class IssueDashboard extends Component {
    setup() {
        super.setup()
        this.orm = useService('orm')
        this._fetch_data()
}
_fetch_data(){
var self = this;
this.orm.call("issue", "get_tiles_data", [], {}).then(function(result){
        $('#source_customer').append('<span>' + result.total_customer + '</span>');
        $('#source_internal').append('<span>' + result.total_internal + '</span>');
        $('#source_supplier').append('<span>' + result.total_supplier + '</span>');
        });
    };
}

IssueDashboard.template ="IssueDashboard"
IssueDashboard.components = { ChartRendererdco,ChartRenderer1,ChartRendererprj,ChartRenderertask,ChartRendererisutag }
// IssueDashboard.components = { ChartRendererdco }
registry.category("actions").add("action_issue_dashboard",IssueDashboard)