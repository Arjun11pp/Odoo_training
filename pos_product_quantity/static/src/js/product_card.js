/** @odoo-module **/
import { useService } from "@web/core/utils/hooks";

import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
import {useState} from "@odoo/owl";
console.log('123')
patch(ProductCard.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            data: {},
            period: [],
              quantity:{},
        });
        // this.showLocation()
    },
    async showLocation() {
        console.log('this',this)
        console.log('wh',this.props.info.productInfo.warehouses[0].id)
        let wh =this.props.info.productInfo.warehouses[0].id
        this.state.data =  await this.orm.searchRead("stock.location",
            [["warehouse_id", "=", wh]],["complete_name"]
            );
        console.log('locs',this.state.data[0],typeof this.state.period)
        this.state.data.forEach(line => {
            this.state.period.push(line.complete_name)
            // this.state.period = this.state.period + ','+line.complete_name;
            console.log('line',this.state.period,',');
        });


             console.log('123',this.state.period,',');

    },
    get availableQty() {
        // console.log('this',this)
        const productTemplate = this.props.product;
        // console.log('product',this.props.product.selected_stock_location_id)
        // console.log('this',this)

        let totalQty = 0;
        productTemplate.product_variant_ids.forEach(line => {
            // console.log('quant',line.product_stock_location_id)
            // console.log('1234',line.stock_quant_ids)
            let quant_id = line.stock_quant_ids
            // this.state.quantity = this.orm.searchRead('stock.quant', [['id', 'in', quant_id], ['location_id', '=', this.props.product.selected_stock_location_id]])
            // console.log('quant',this.state.quantity)
        //     if (this.state.quantity){
        //         totalQty += this.state.quantity.quantity;
        // }
        // else{ totalQty=0
        // }
                })
        // console.log('qq',this.state.quantity)
        // totalQty=this.props.product.qty_location

        return totalQty;
    },
});