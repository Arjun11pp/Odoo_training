import {ProductInfoPopup} from "@point_of_sale/app/components/popups/product_info_popup/product_info_popup";
import { useService } from "@web/core/utils/hooks";
import {patch} from "@web/core/utils/patch";
import { useState } from "@odoo/owl";

patch(ProductInfoPopup.prototype, {
    setup() {
         super.setup();
        this.orm = useService("orm");
        this.state = useState({
            data: {},
            final_qty:0,
            location:{},
        });
        this.showLocation()
    },
    async showLocation() {
        let tmpl_ids =[]
        this.props.productTemplate.product_variant_ids.forEach(line => {
            tmpl_ids.push(line.id) });
        let qqq =  await this.orm.searchRead("stock.quant",
            [["location_id", "=", this.props.productTemplate.selected_stock_location_id],['product_id','in',tmpl_ids]]);
        let quantity=0
        qqq.forEach(line => {
            if (this.state.location[line.display_name])
            {
                quantity+= line.quantity

            }else {
                quantity = line.quantity
            }
            this.state.location[line.display_name]=quantity

        });
        this.state.final_qty=quantity
    },
});
