/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, useState} from "@odoo/owl";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {DropdownItem} from "@web/core/dropdown/dropdown_item";
import {rpc} from '@web/core/network/rpc';

class SystrayIcon extends Component {
   setup() {
       super.setup();
       this.notification = useService("notification");
       this.state = useState({
            data: {},
           weather:{},
           date:{},
           temp:{},
            curr_datetime:{},
           icon:{},
           has_value:{ },
        });

   }
   async showNotification() {
         /**
       * fetched data from  controller and passes to the xml
       */
       try {
           this.state.data = await rpc('/request/submit', {});
           if (this.state.data){
               this.state.has_value=true
            this.state.curr_datetime =  new Date().toTimeString()
           this.state.date=new Date().toDateString()
           this.state.weather= this.state.data.weather[0].description
           this.state.temp=this.state.data.main
            this.state.icon=this.state.data.weather[0].icon}
           else{

               this.state.has_value=false
           }
       }
        catch (error) {
           console.error('Error:', error);
       }
       };
    _onClickSettngs() {
       /**
       * redirect to settngs page
       */
       console.log('543w')
        this.env.services.action.doAction({
            name: ("settngs"),
            type: 'ir.actions.act_window',
            res_model: 'res.config.settings',
            context:{ module :'api'},
            views: [[false, 'form']],
            target: 'current',

        });
    }
   }
SystrayIcon.template = "systray_dropdown";
SystrayIcon.components = { Dropdown, DropdownItem };
export const systrayItem = {
   Component: SystrayIcon,
};
registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });
