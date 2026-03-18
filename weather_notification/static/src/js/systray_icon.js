/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { rpc } from '@web/core/network/rpc';
console.log('23')
class SystrayIcon extends Component {
   setup() {
       super.setup();
       this.notification = useService("notification");
   }
   async showNotification() {
       try {

           let response = await rpc('/request/submit', {});
           console.log('333',response);

       }
        catch (error) {
           console.error('Error:', error);

       }
           this.notification.add("Hello! This is a notification", {
               title: "Systray Notification",
               type: "info",
               sticky: true,
           });
       }
   }
SystrayIcon.template = "systray_icon";
export const systrayItem = {
   Component: SystrayIcon,
};
registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });
//https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={a7b5f91f8b72fb52e428cef7868ff6e5}