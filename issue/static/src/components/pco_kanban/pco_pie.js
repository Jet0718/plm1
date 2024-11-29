/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"
import { ChartRendererpcotags } from "./pco_tagbar"

const { Component, onWillStart, useRef, onMounted } = owl
top.pcopietagchart;
top.pcopiedocumetnthis=false;
top.listv=""
export class ChartRendererpco extends Component {
    setup(){
        debugger
        top.pcopiedocumetnthis=this;
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
        top.pcodocumetnthis.orm.call("issue", "getpco_tag_counts", [top.listv], {}).then(function(result){
              var labels = result.map(record => record.tag_ids[1]);
              var values = result.map(record => record.tag_ids_count);            
              top.pcotagchart.data.datasets[0].data=values
              top.pcotagchart.data.labels=labels
              top.pcotagchart.update();                    
          });
        top.pcopiedocumetnthis.orm.call("issue", "getpco_status_counts", [top.listv], {}).then(function(result){
          var array=[]
             array.push(result.new_count)
             array.push(result.review_count)
             array.push(result.approved_count)
             array.push(result.cancel_count)      
          top.pcopietagchart.data.datasets[0].data=array
          top.pcopietagchart.update();                    
        });
      });  
      var self = this;
      this.orm.call("issue", "getpco_status_counts", [top.listv], {}).then(function(result){
             var array=[]
             array.push(result.new_count)
             array.push(result.review_count)
             array.push(result.approved_count)
             array.push(result.cancel_count)
             const dataarry =array
             
             top.pcopietagchart=new Chart(self.chartRef.el,
              {
                type: 'bar',
                data: {
                  labels: [
                      'New',
                      'Review',
                      'Approved',
                      'Cancel'
                    ],
                    datasets: [
                    {
                      label: 'pco states',
                      data:  dataarry,
                      hoverOffset: 4,
                      backgroundColor: [
                        'rgba(255, 99, 132, 0.6)', // 红色
                        'rgba(54, 162, 235, 0.6)', // 蓝色
                        'rgba(255, 206, 86, 0.6)', // 黄色
                        'rgba(128, 0, 128, 0.5)' // 紫色
                    ]
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

ChartRendererpco.template = "ChartRendererpco"
ChartRendererpco.components = {ChartRendererpcotags}
registry.category("actions").add("action_pco_dashboard",ChartRendererpco)