/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"

const { Component, onWillStart, useRef, onMounted } = owl

export class ChartRendererisutag extends Component {
    setup(){
        // debugger
        
        super.setup()
        this.orm = useService('orm')
        // const partners = await  this.orm.call("issue", "_getpco_status_counts", []);
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })
        
        // const fetchPartners = async () => {
        //   const dataarry = await this.orm.call("issue", "getpco_status_counts", [], {});
        //   // this.orm.call("issue", "getpco_status_counts", [], {})
        // };
        // // this.fetchPartners()
        // var dataarry =this._fetch_data();
        
        // setTimeout("", 1000); 
        // if (dataarry.length<1)setTimeout("", 1000); 
        
        onMounted(()=>this.renderChart())
        
        // setTimeout("this.initChart();", 500); 
         
        
       
    }    

    
     async  renderChart(){
      // debugger
      
      var self = this;
      // var dataarry=[];
      this.orm.call("issue", "getisu_tag_counts", [], {}).then(function(result){
        const labels = result.map(record => record.issue_code_ids[1]);
        const values = result.map(record => record.issue_code_ids_count);
             
             new Chart(self.chartRef.el,
              {
                type: 'pie',
                data: {
                  labels: labels,
                    datasets: [
                    {
                      label: 'Issue Tags',
                      data:  values,
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

ChartRendererisutag.template = "owl.ChartRenderer"