/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"

const { Component, onWillStart, useRef, onMounted } = owl
top.tskbarchart;
top.tskbardocumetnthis=false;
export class ChartRenderertask extends Component {
    setup(){
        // debugger
        top.tskbardocumetnthis=this;
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
      var self = this;
      // var dataarry=[];
      this.orm.call("issue", "gettask_state_counts", [top.listv], {}).then(function(result){
        const labels = result.map(record => record.state);
        const values = result.map(record => record.state_count);
             
        top.tskbarchart= new Chart(self.chartRef.el,
              {
                type: 'bar',
                data: {
                  labels: labels,
                    datasets: [
                    {
                      label: 'Task State',
                      data:  values,
                      hoverOffset: 4,
                      // 每个柱子的数据
                      backgroundColor: [ // 每个柱子的颜色
                          'rgba(255, 99, 132, 0.6)', // 红色
                          'rgba(54, 162, 235, 0.6)', // 蓝色
                          'rgba(255, 206, 86, 0.6)', // 黄色
                          'rgba(75, 192, 192, 0.6)', // 绿色
                          'rgba(75, 192, 192, 0.6)' // 绿色
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

ChartRenderertask.template = "owl.ChartRenderer"
