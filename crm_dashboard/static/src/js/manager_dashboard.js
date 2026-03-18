/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, onMounted, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {session} from "@web/session";

const actionRegistry = registry.category("actions");
const currentUserId = session.storeData.Store.settings.user_id.id;
class CrmDashboard2 extends Component {
  setup() {
        this.orm = useService('orm');
        this.state = useState({
            data: {},
        });

        this._fetch_data2();
      }


  async _fetch_data2(interval2){
      console.log('int',interval2)
      this.state.data=await this.orm.call("crm.lead","get_tiles_manager_data", [interval2], {});

  }
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
CrmDashboard2.template = "crm_manager_dashboard.CrmDashboard2";
// registry.category('actions').add('crm_manager_dashboard.dashboard',CrmDashboard2)
actionRegistry.add("crm_dashboard_tag_manager",CrmDashboard2);
