/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { loadJS } from "@web/core/assets";
//console.log('W');

publicWidget.registry.WarningWidget = publicWidget.Widget.extend({
    selector: '#backend_warning',

    start: function () {
        const message = this.$el.data('message');
        if (message) {

            alert(message);
        }
        return this._super.apply(this, arguments);
    },
});

    publicWidget.registry.WebsiteCustomerContactRequestForm = publicWidget.Widget.extend({
    selector: ".s_website_form_required1",

    start: function () {
        const self = this;
        return this._super.apply(this, arguments).then(function () {
            return loadJS("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js");
        }).then(() => {
            self.$("select").select2({
                placeholder: "Select an option",
                allowClear: true,
                width: '100%'
            });
        }).catch(err => console.error("Error loading Select2:", err));
    },
});
