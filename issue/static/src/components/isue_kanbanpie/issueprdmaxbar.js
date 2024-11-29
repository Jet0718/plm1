/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { loadJS } from "@web/core/assets"

const { Component, onWillStart, useRef, onMounted } = owl
top.isuemaxchart;
top.isuemaxdocumetn=false;
export class ChartRendererissueprdmax extends Component {
    setup(){
        // debugger
        top.isuemaxdocumetn=this;
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
        top.isuetotaldocumetn.orm.call("issue", "get_tiles_data", [top.listv], {}).then(function(result){
              var sp=document.getElementById("source_customer");             
              if(result.total_customer!='0')
                sp.innerHTML="<span>"+result.total_customer+"</span>"
              else{
                sp.innerHTML="<span></span>"
              }
              sp=document.getElementById("source_internal");
              if(result.total_internal!='0')
                sp.innerHTML="<span>"+result.total_internal+"</span>"
              else{
                sp.innerHTML="<span></span>"
              }
              sp=document.getElementById("source_supplier");
              if(result.total_supplier!='0')
                sp.innerHTML="<span>"+result.total_supplier+"</span>"
              else{
                sp.innerHTML="<span></span>"
              }
          });
      
        top.isuemaxdocumetn.orm.call("issue", "getprdmaxiss_counts", [top.listv], {}).then(function(result){
          var labels = result.map(record => record.issue_product_id[1]);
          var array = result.map(record => record.issue_product_id_count); 
          top.isuemaxchart.data.labels = labels        
          top.isuemaxchart.data.datasets[0].data=array
          top.isuemaxchart.update();                    
        });
        top.isuetagdocumetn.orm.call("issue", "getisu_tag_counts", [top.listv], {}).then(function(result){
          var labels = result.map(record => record.issue_code_ids[1]);
          var array = result.map(record => record.issue_code_ids_count);         
          top.isuetagchart.data.datasets[0].data=array
          top.isuetagchart.data.labels = labels
          top.isuetagchart.update();                    
        });
      });
      var self = this;
      // var dataarry=[];
      this.orm.call("issue", "getprdmaxiss_counts", [top.listv], {}).then(function(result){
        const labels = result.map(record => record.issue_product_id[1]);
        const values = result.map(record => record.issue_product_id_count);             
        top.isuemaxchart=new Chart(self.chartRef.el,
              {
                type: 'bar',
                data: {
                  labels: labels,
                    datasets: [
                    {
                      label: 'Issue Product Max',
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

ChartRendererissueprdmax.template = "owl.ChartRenderer"
