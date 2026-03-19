/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import {Component, useState} from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { rpc } from '@web/core/network/rpc';
console.log('23')
class SystrayIcon extends Component {
   setup() {
       super.setup();
       this.notification = useService("notification");
       this.state = useState({
            data: {},

        });

   }
   async showNotification() {
       try {
           this.state.data = await rpc('/request/submit', {});
           // let lat=this.getAndUpdateLocation()
           console.log('333',this.state.data.weather[0].main);










       }
        catch (error) {
           console.error('Error:', error);
       }
       }

   }
SystrayIcon.template = "systray_dropdown";
SystrayIcon.components = { Dropdown, DropdownItem };
export const systrayItem = {
   Component: SystrayIcon,
};
registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });
