/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"
import { ChartRendererpcotags } from "./pco_tagbar"

const { Component, onWillStart, useRef, onMounted } = owl

export class ChartRendererpco extends Component {
    setup(){
        debugger
        
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

    _fetch_data(){
      var self = this;
      var dataarry=[];
      this.orm.call("issue", "getpco_status_counts", [], {}).then(function(result){
             var array=[]
             array.push(result.new_count)
             array.push(result.review_count)
             array.push(result.approved_count)
             array.push(result.cancel_count)
             dataarry =array  
                     
      }); 
      // if (dataarry && dataarry.length<1)
      //   setTimeout("_fetch_data();", 500); 
      return dataarry
     };
     async  renderChart(){
      debugger
      
      var self = this;
      // var dataarry=[];
      this.orm.call("issue", "getpco_status_counts", [], {}).then(function(result){
             var array=[]
             array.push(result.new_count)
             array.push(result.review_count)
             array.push(result.approved_count)
             array.push(result.cancel_count)
             const dataarry =array
             
             new Chart(self.chartRef.el,
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

ChartRendererpco.template = "ChartRendererpco"
ChartRendererpco.components = {ChartRendererpcotags}
registry.category("actions").add("action_pco_dashboard",ChartRendererpco)