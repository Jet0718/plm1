/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"

const { Component, onWillStart, useRef, onMounted } = owl
top.pcotagchart;
top.pcodocumetnthis=false;
export class ChartRendererpcotags extends Component {
    setup(){
        debugger
        top.pcodocumetnthis=this;
        super.setup()
        this.orm = useService('orm')
        // const partners = await  this.orm.call("issue", "_getpco_status_counts", []);
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })        
        onMounted(()=>this.renderChart())       
    }   
    
    // 随机颜色生成函数
    randomColor() {
      return `rgba(${random(0, 255)}, ${random(0, 255)}, ${random(0, 255)}, 0.5)`;
    }
     async  renderChart(){
      debugger
      self =this;
      this.orm.call("issue", "getpco_tag_counts", [top.listv], {}).then(function(result){
            const labels = result.map(record => record.tag_ids[1]);
            const values = result.map(record => record.tag_ids_count);            
            top.pcotagchart=new Chart(self.chartRef.el,
              {                
                type: 'bar',
                data: {
                  labels: labels,
                    datasets: [
                    {
                      label: 'PCO Tags',
                      data:  values,
                      hoverOffset: 4,
                      // backgroundColor: labels.map(() => (`rgba(${Math.random(0, 255)}, ${Math.random(0, 255)}, ${Math.random(0, 255)}, 0.5)`))
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

ChartRendererpcotags.template = "owl.ChartRenderer"
