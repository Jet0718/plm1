/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"
import { ChartRenderertask } from "../task_kanbanbar/task_bar"

const { Component, onWillStart, useRef, onMounted } = owl
top.prjbarchart;
top.prjbardocumetnthis=false;
top.listv="";
export class ChartRendererprj extends Component {
    setup(){
        // debugger
        
        top.prjbardocumetnthis=this;
        super.setup()
        this.orm = useService('orm')
        // const partners = await  this.orm.call("issue", "_getpco_status_counts", []);
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })        
        onMounted(()=>this.renderChart())
    }        
     async  renderChart(){
      
      document.getElementById('datas').addEventListener('change', function() {
        var list=document.getElementById("datas")    
        if(list)
        {
          top.listv=list.value
          
        }
        else{
            top.listv='0'            
        }
        top.prjbardocumetnthis.orm.call("issue", "getprj_tag_counts", [top.listv], {}).then(function(result){
              var labels = result.map(record => record.tag_ids[1]);
              var array = result.map(record => record.tag_ids_count);           
              top.prjbarchart.data.datasets[0].data=array
              top.prjbarchart.data.labels=labels
              top.prjbarchart.update();                    
          });
        top.tskbardocumetnthis.orm.call("issue", "gettask_state_counts", [top.listv], {}).then(function(result){
          var labels = result.map(record => record.state);
          var array = result.map(record => record.state_count);          
          top.tskbarchart.data.datasets[0].data=array
          top.tskbarchart.data.labels=labels
          top.tskbarchart.update();                    
        });
      });
      var self = this;
      // var dataarry=[];
      this.orm.call("issue", "getprj_tag_counts", [top.listv], {}).then(function(result){
        const labels = result.map(record => record.tag_ids[1]);
        const values = result.map(record => record.tag_ids_count);
        
        top.prjbarchart= new Chart(self.chartRef.el,
              {
                type: 'bar',
                data: {
                  labels: labels,
                    datasets: [
                    {
                      label: 'Project Tags',
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

ChartRendererprj.template = "ChartRendererprj"


ChartRendererprj.components = {ChartRenderertask}
registry.category("actions").add("action_prj_dashboard",ChartRendererprj)
