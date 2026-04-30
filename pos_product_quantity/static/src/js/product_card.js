/** @odoo-module **/

import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
console.log('123')
patch(ProductCard.prototype, {

    get availableQty() {
        console.log('this',this)
        const productTemplate = this.props.product;
        console.log('product',productTemplate)

        let totalQty = 0;
        productTemplate.product_variant_ids.forEach(line => {
            // if (this.pos.session.product_location in line.stock_quant_ids)
            totalQty += line.qty_available || 0;
        })

        return totalQty;
    },
});