/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"

const { Component, onWillStart, useRef, onMounted } = owl
top.dcotahchart;
top.dcotagdocumetnthis=false;
export class ChartRendererdcotag extends Component {
    setup(){
        // debugger
        top.dcotagdocumetnthis=this;
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
      this.orm.call("issue", "getdco_tag_counts", [top.listv], {}).then(function(result){
            const labels = result.map(record => record.tag_ids[1]);
            const values = result.map(record => record.tag_ids_count);
            top.dcotahchart=new Chart(self.chartRef.el,
              {
                type: 'bar',
                data: {
                  labels: labels,
                    datasets: [
                    {
                      label: 'dco tag count',
                      data:  values,
                      hoverOffset: 4,
                      backgroundColor: labels.map(() => (`rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)})`))
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

ChartRendererdcotag.template = "owl.ChartRenderer"
