/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector: '.categories_section',
    async start() {
    const result = await rpc('/get_credit_list', {});
    const size=Math.ceil((result.credits_ids.length)/4)
    var page = Array.from(Array(size).keys());

    if(result)  {
    this.$target.empty().html(renderToElement('recurring_subscription.category_data', {
        result: result , pages: page
    }));
    }
},

});
