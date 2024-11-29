/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"

import { ChartRendererdcotag } from "./dco_tagbar"

const { Component, onWillStart, useRef, onMounted } = owl
top.dcopiechart;
top.dcopiedocumetnthis=false;
top.listv="";
export class ChartRendererdco extends Component {
    setup(){
        // debugger
        top.dcopiedocumetnthis=this;
        super.setup()
        this.orm = useService('orm')
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })
        onMounted(()=>this.renderChart())   
      }  

     async  renderChart(){      
      var self =this;
      document.getElementById('datas').addEventListener('change', function() {
        var list=document.getElementById("datas")    
        if(list)
        {
          top.listv=list.value
          
        }
        else{
            top.listv='0'            
        }
        top.dcopiedocumetnthis.orm.call("issue", "getdco_status_counts", [top.listv], {}).then(function(result){
              var array=[]
              array.push(result.new_count)
              array.push(result.review_count)
              array.push(result.approved_count)
              array.push(result.cancel_count)            
              top.dcopiechart.data.datasets[0].data=array
              top.dcopiechart.update();                    
          });
        top.dcotagdocumetnthis.orm.call("issue", "getdco_tag_counts", [top.listv], {}).then(function(result){
          var labels = result.map(record => record.tag_ids[1]);
          var array = result.map(record => record.tag_ids_count);          
          top.dcotahchart.data.datasets[0].data=array
          top.dcotahchart.data.labels = labels
          top.dcotahchart.update();                    
        });
      });
      this.orm.call("issue", "getdco_status_counts", [top.listv], {}).then(function(result){
             var array=[]
             array.push(result.new_count)
             array.push(result.review_count)
             array.push(result.approved_count)
             array.push(result.cancel_count)
             const dataarry =array             
             top.dcopiechart = new Chart(self.chartRef.el,
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
