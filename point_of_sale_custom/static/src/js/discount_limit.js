
import { patch } from "@web/core/utils/patch";

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/services/pos_store";


let orderDiscount = 0;
patch(PosStore.prototype, {
    async pay() {
        super.pay();
        console.log('this1234',this);
        var total_order_discount =0
        console.log('limit',this.session.discount_limit_amount);
        const order_lines=this.openOrder.lines
        order_lines.forEach(line => {
        total_order_discount+=line.prices.discount_amount;
        console.log('discount',total_order_discount);
        });

        if (total_order_discount >this.session.discount_limit_amount){
          this.dialog.add(AlertDialog, {
                title: _t("Discount limit reached"),
                body: _t("the discount limit reached "),
            });
//              this.mobile_pane = "right";
                this.navigate("ProductScreen", {
                    orderUuid: this.selectedOrderUuid,
                });
            return false;
        }
        else{
        this.session.discount_limit_amount-=total_order_discount;
        }
        console.log('discount left',this.session.discount_limit_amount);

},
//getDiscountCheck(){
//    console.log('this2',this);
//
////    console.log('this3',dis_props);
//    const dis_props = 0;
//    return dis_props;
//}
});
