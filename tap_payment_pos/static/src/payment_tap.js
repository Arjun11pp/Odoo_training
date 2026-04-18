import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(OrderPaymentValidation.prototype, {
    setup(vals) {
        super.setup(...arguments);
        this.dialog = this.pos.env.services.dialog;
    },
    async validateOrder() {
        this.paymentLines.forEach(line => {
            if(line.payment_method_id.name==='Tap' && line.payment_status!=='done' ){
                console.log('doneee')
                return this.dialog.add(AlertDialog, {
                title: _t("PAYMENT Error"),
                body: _t(
                    " Tap payment is not validated." ),
            });

            }
        })


    },
});