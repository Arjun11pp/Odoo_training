///** @odoo-module */
//import { patch } from "@web/core/utils/patch";
//import { PosStore } from "@point_of_sale/app/services/pos_store";
//console.log('this1',this);
//patch(PosStore.prototype, {
//    async _processData (loadedData) {
//    await super. processData(...arguments);
//    this.product_owner_id= loadedData['product.template']
//    console.log('this2', this)
//    console.log('this3', this.product_owner_id)
//    }
//})