import { OrderDisplay } from "@point_of_sale/app/components/order_display/order_display";
import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { ListContainer } from "@point_of_sale/app/components/list_container/list_container";
console.log("123");
let orderDiscount = 0;
//patch(OrderDisplay.prototype, {
    onNumpadClick(buttonValue) {
        if (["discount"].includes(buttonValue)) {
        console.log('discount');
        }
        };
//    setup() {
//
//        console.log('112',this);
//        const lines=this.props.order.lines;
//
//        console.log('this');
////        let order_discount = 0;
//        lines.forEach(line => {
//            orderDiscount +=line.prices.discount_amount;
//            if(orderDiscount > 100)
//            {
//             this.env.services.dialog.add(AlertDialog, {
//                title: _t("limit reached"),
//                body: _t("The discount limit reached for this session."),
//            });
//            console.log('limit reached');
//        }
//
//        });
//        console.log('diss',orderDiscount);
//    }
//});
//console.log('dissf',orderDiscount);
//patch(PosOrderline.prototype, {
//    setup() {
//    console.log('111',this.prices.discount_amount);
//    orderDiscount += this.prices.discount_amount
//    if(orderDiscount > 100)
//    {
////    return this.dialog.add(AlertDialog, {
////                title: _t("Error"),
////                body: _t("You cannot edit a discount line."),
////            });
//    }
//console.log('order',orderDiscount);
//    },
//});


