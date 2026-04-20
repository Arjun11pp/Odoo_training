import { PaymentScreenPaymentLines } from "@point_of_sale/app/screens/payment_screen/payment_lines/payment_lines";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import {useService} from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";

patch(PaymentScreenPaymentLines.prototype, {
setup(){
    super.setup();
      this.orm = useService('orm');
    this.state = useState({
        datas: {},
        methods: {},
        is_clicked: false,
    });
},
sendTapPaymentRequest(amount) {
    /**
     * Send tap payment request from pos
     */
    const is_clicked=true
    let price=0;
    amount.props.paymentLines.forEach(line => {
        if(line.payment_method_id.name === 'Tap'){
            price=line.amount;
            if(price<=0){
         this._showTapError(_t("Payment amount is zero"));
    }
        }
    })
    this.sendPaymentRequest(this.pos.selectedOrder.uuid,price)

},
    async sendPaymentRequest(uuid,price) {
        return this._createTapPayment(uuid,price);
    },
    async _createTapPayment(uuid,price) {
        /**
         * function calls tap payment request function from pos.payment.method model
         */
        let method_id
        try {
            this.props.paymentLines.forEach(line => {
        if(line.payment_method_id.name === 'Tap'){
           method_id=line.payment_method_id.id

        }})
            const data = await this.pos.data.call("pos.payment.method", "tap_create_payment", [
                method_id,
               price, uuid,
                this.pos.session.id,
            ]);
             this.state.datas=data
             this.state.methods=method_id
            if (!["CREATED"].includes(data.status)) {
                this._showTapError(_t("Failed to initiate payment: %s", data.status));
                return false;
            }

            await this.pos.data.synchronizeLocalDataInIndexedDB();
            const { promise, resolve } = Promise.withResolvers();
            this.state.is_clicked=true
            return promise;

        } catch (error) {
            this._showTapError(error);
            return false;
        }
    },
    _showTapError(error) {
        /**
         * throws error upon call
         */
        this.env.services.dialog.add(AlertDialog, {
            title: _t("Tap Error"),
            body: this._extractErrorMessage(error),
        });
    },
     _extractErrorMessage(error) {
         /**
          * function extracts the error message
          */
        if (typeof error === "string") {
            return error;
        }
        if (error.name === "RPC_ERROR") {
            return error.data.message;
        }
        return error.message;
    },
      async checkPaymentStatus(line){
          /**
           * function that calls tap_get_payment function to get payment details
           */
        try {
            const pay_details= await this.orm.call("pos.payment.method", "tap_get_payment", [this.state.methods,this.state.datas.id],{});
            if (pay_details.status === 'CREATED'){
                 this._showTapError('payment pending');
            }
            else {
                 line.setPaymentStatus('done')
            }

        }  catch (error) {
            this._showTapError(error);
            return false;
        }
    }
});
