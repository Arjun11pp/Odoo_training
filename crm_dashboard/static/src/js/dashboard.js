/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, onMounted, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {session} from "@web/session";
const actionRegistry = registry.category("actions");

const currentUserId = session.storeData.Store.settings.user_id.id;
class CrmDashboard extends Component {
  setup() {
            onMounted(()=>{
                this._renderChart();
            });
        this.orm = useService('orm');
        this.state = useState({
            data: {},
            period:{},
        });
        // this._renderChart();
      }
      async _renderChart(interval){
          /**
           * function to render charts
           */

          this.state.data=await this.orm.call("crm.lead", "get_tiles_data", [interval], {});
          let inter;
          if(!interval){
              inter=7
          }
        else{
            inter = interval
          }
        const date_interval=await this.orm.call("crm.lead", "date_calculation", [inter], {});
        const mediumIds=[1,2,3,4,5,6,7,8,9,10]
        const count=[]
        for(let i of mediumIds)  {
             var medium= await this.orm.searchCount('crm.lead',[['medium_id','=',i ]   ,['create_date','<=',date_interval]])
            count.push(medium)
        }
      new Chart("chart_example3", {
        type: "doughnut",
        data: {
            labels: ["Website" ,"Phone","Direct","Email", "Banner","X","Facebook","LinkedIn","Television","Google Adwords"  ],
            datasets: [{
            backgroundColor: ['yellow','red','blue','green','orange','violet','purple','pink','cyan','indigo'],
            data: count
        }]
    },
    options: {
    }
});
        var activity_count=  await this.orm.searchCount('crm.lead',[['activity_type_id','=',1 ],['create_date','<=',date_interval]])
        var activity_count1= await this.orm.searchCount('crm.lead',[['activity_type_id','=',2 ],['create_date','<=',date_interval]])
        var activity_count2= await this.orm.searchCount('crm.lead',[['activity_type_id','=',3 ],['create_date','<=',date_interval]])
        var activity_count3= await this.orm.searchCount('crm.lead',[['activity_type_id','=',4 ],['create_date','<=',date_interval]])
        var activity_count4= await this.orm.searchCount('crm.lead',[['activity_type_id','=',5 ],['create_date','<=',date_interval]])
          var chart = new Chart('chart_example', {
            type: "pie",
            data: {
            labels: ["Email" ,"Call","Meeting","To-Do", "Document"],
            datasets: [{
                backgroundColor: ['yellow','red','blue','green','orange'],
                data: [activity_count,activity_count1,activity_count2,activity_count3,activity_count4]
                }]
            },
                options: {}
            });
           var lost= await this.orm.call("crm.lead", "get_lost_leads", [inter], {});
               const lostt=lost.lost_leads
                var chart2 = new Chart("chart_example2", {
                    type: "bar",
            data: {
                labels: ["count"],
                datasets: [{
                    backgroundColor: "red",
                    data: [lostt]
                }]
            },
                    options: {}
});
       this.state.period=await this.orm.call("crm.lead", "leads_by_month", [], {});
       console.log('count',this.state.period)
        };

  _onClickLead() {
      /**
       * function will display leads of current loggedin user from crm.lead model
       */
        this.env.services.action.doAction({
            name: _t("My leads"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'list',
            views: [[false, 'list']],
            target: 'current',
            domain: [["user_id", "=", currentUserId],['type','=','lead']],
        });
    }
    _onClickOpportunity() {
       /**
       * function will display Opportunity  of current loggedin user from crm.lead model
       */
      interval=this.state.data
        console.log('interr',interval)
        this.env.services.action.doAction({
            name: _t("My leads"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'list',
            views: [[false, 'list']],
            target: 'current',
            domain: [["user_id", "=", currentUserId],['type','=','opportunity']],
        });
    }

}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
registry.category('actions').add('my_module.dashboard',CrmDashboard)
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
