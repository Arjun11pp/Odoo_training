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
            period:{},
        });
        this.showLocation()
    },
    async showLocation() {
        console.log('this',this)
        // console.log('wh',this.props.info.productInfo.warehouses[0].id)
        let wh =this.props.info.productInfo.warehouses[0].id
        let tmpl_ids =[]
        this.props.productTemplate.product_variant_ids.forEach(line => {
            tmpl_ids.push(line.id) });
        console.log('tmpl_ids',tmpl_ids)
        this.state.data =  await this.orm.searchRead("stock.location",
            [["warehouse_id", "=", wh]],['id',"complete_name"]
            );
        let qqq =  await this.orm.searchRead("stock.quant",
            [["location_id", "=", this.props.productTemplate.selected_stock_location_id],['product_id','in',tmpl_ids    ]]
            );
        console.log('qqq',qqq)
        console.log('locs',this.state.data[0],typeof this.state.period)
        let quantity=0
        qqq.forEach(line => {
            console.log('if_ids', line.id)
            if (this.state.period[line.display_name])
            {
                quantity+= line.quantity

            }else {
                quantity = line.quantity
            }
            this.state.period[line.display_name]=quantity

        });
        this.state.final_qty=quantity
             console.log('123',this.state.period);
             console.log('444',this.state.final_qty);
    },
});
