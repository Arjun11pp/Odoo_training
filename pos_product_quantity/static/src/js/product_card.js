/** @odoo-module **/

import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
console.log('123')
patch(ProductCard.prototype, {
    
    get availableQty() {
        console.log('this',this)
        const productTemplate = this.props.product;
        console.log('product',this.props.product.qty_location)

        let totalQty = 0;
        // productTemplate.product_variant_ids.forEach(line => {
        //      // console.log('quant',line.product_stock_location_id)
        //         // console.log('1234',line.stock_quant_ids)
        //         totalQty += line.qty_available || 0;
        //
        // })
        totalQty=this.props.product.qty_location

        return totalQty;
    },
});