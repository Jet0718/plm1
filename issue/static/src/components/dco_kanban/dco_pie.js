/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"

import { ChartRendererdcotag } from "./dco_tagbar"

const { Component, onWillStart, useRef, onMounted } = owl

export class ChartRendererdco extends Component {
    setup(){
        // debugger
        
        super.setup()
        this.orm = useService('orm')
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })
        onMounted(()=>this.renderChart())   
      }  

     async  renderChart(){
      // debugger      
      var self = this;
      this.orm.call("issue", "getdco_status_counts", [], {}).then(function(result){
             var array=[]
             array.push(result.new_count)
             array.push(result.review_count)
             array.push(result.approved_count)
             array.push(result.cancel_count)
             const dataarry =array             
             new Chart(self.chartRef.el,
              {
                type: 'pie',
                data: {
                  labels: [
                      'New',
                      'Review',
                      'Approved',
                      'Cancel'
                    ],
                    datasets: [
                    {
                      label: 'dco states count',
                      data:  dataarry,
                      hoverOffset: 4
                    }
                  ]
                },
                options: {
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'bottom',
                    },
                    title: {
                      display: true,
                      text: self.props.title,
                      position: 'bottom',
                    }
                  }
                },
              }
            );                     
      });     
    }
}

ChartRendererdco.template = "ChartRendererdco"
ChartRendererdco.components = {ChartRendererdcotag}
registry.category("actions").add("action_dco_dashboard",ChartRendererdco)
