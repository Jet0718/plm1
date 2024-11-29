/** @odoo-module */
import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks";

// import { ChartRenderer1 } from "./pco_kanban/pco_pie"

import { ChartRendererisutag } from "./isue_kanbanpie/issuetag_pie"
import { ChartRendererissueprdmax } from "./isue_kanbanpie/issueprdmaxbar"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, UseRef, onMounted } = owl
top.isuetotaldocumetn=false;
top.listv='0';
export class IssueDashboard extends Component {
    setup() {
        top.isuetotaldocumetn=this;
        super.setup()
        this.orm = useService('orm')
        this._fetch_data()
}
_fetch_data(){   
    var self = this;
        this.orm.call("issue", "get_tiles_data", [top.listv], {}).then(function(result){
                $('#source_customer').append('<span>' + result.total_customer + '</span>');
                $('#source_internal').append('<span>' + result.total_internal + '</span>');
                $('#source_supplier').append('<span>' + result.total_supplier + '</span>');
                });
    };
}

IssueDashboard.template ="IssueDashboard"
//ChartRenderer1
IssueDashboard.components = { ChartRendererisutag,ChartRendererissueprdmax}
// IssueDashboard.components = { ChartRendererdco }
registry.category("actions").add("action_issue_dashboard",IssueDashboard)