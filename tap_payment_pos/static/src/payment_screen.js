/** @odoo-module **/

import { PaymentScreenPaymentLines } from "@point_of_sale/app/screens/payment_screen/payment_lines/payment_lines";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import {useService} from "@web/core/utils/hooks";
import {useState} from "@odoo/owl";


patch(PaymentScreenPaymentLines.prototype, {
setup(){
    super.setup();
      this.orm = useService('orm');
    this.state = useState({
        datas: {},
    });
},
onClickTest(amount) {
let price=0;
    console.log("Clicked Test Button",this);
    console.log("amount",amount.props.paymentLines);
    // amounts=a
    amount.props.paymentLines.forEach(line => {
        if(line.payment_method_id.name === 'Tap'){
            price=line.amount;
            console.log('price',price)
        }
        console.log('lines',line.payment_method_id)
    })
    // console.log('ppp',this.pos.selectedOrder.uuid)
    // console.log('ppp',this.pos)
    this.sendPaymentRequest(this.pos.selectedOrder.uuid,price)
},
    async sendPaymentRequest(uuid,price) {
        console.log('1',this.pos.getOrder())
        console.log('2',uuid)
        // const paymentLine = this.pos.getOrder().getPaymentlineByUuid(uuid);
        // console.log('paymentline1',paymentLine)
        // if (paymentLine.amount < 0) {
        //     const originalPaymentId = this._findOriginalPaymentId(paymentLine);
        //     if (!originalPaymentId) {
        //         this._showTapError(
        //             _t("You can only refund an order that was paid for with Tap.")
        //         );
        //         return false;
        //     }
        //     return this._createTapRefund(paymentLine, originalPaymentId);
        // }
        return this._createTapPayment(uuid,price);
    },
    async _createTapPayment(uuid,price) {
        console.log('12')
        let method_id
        try {
            console.log('this',this)
            console.log('pay',this.pos.session.id)
            // console.log('payment method',this.payment_method_id.id)
            this.props.paymentLines.forEach(line => {
        if(line.payment_method_id.name === 'Tap'){
           method_id=line.payment_method_id.id
            console.log('price',method_id,uuid,this.pos.session.id)
        }})
            const data = await this.pos.data.call("pos.payment.method", "tap_create_payment", [
                method_id,
               price, uuid,
                this.pos.session.id,
            ]);
             this.state.datas=data
            console.log('ddd',data)
            if (!["CREATED"].includes(data.status)) {
                this._showTapError(_t("Failed to initiate payment: %s", data.status));
                return false;
            }
            // if (data.url) {
                // browser.open(data.url, "_blank");
                // redirect(data.url.href);
            // }
            // const paymentLine = this.getPaymentlineByUuid(uuid);
            // console.log('tansac',paymentLine)
            // paymentLine.transaction_id = data.id;
            await this.pos.data.synchronizeLocalDataInIndexedDB();
            const { promise, resolve } = Promise.withResolvers();
            // this.paymentLineResolvers[paymentLine.uuid] = resolve;
            return promise;
        } catch (error) {
            console.log('catch')
            this._showTapError(error);
            return false;
        }
    },
    _showTapError(error) {
        this.env.services.dialog.add(AlertDialog, {
            title: _t("Tap Error"),
            body: this._extractErrorMessage(error),
        });
    },
     _extractErrorMessage(error) {
        if (typeof error === "string") {
            return error;
        }
        if (error.name === "RPC_ERROR") {
            return error.data.message;
        }
        return error.message;
    },
     onClickCheck(){
        console.log('check',this)
        try {
            this.orm.call("pos.payment.method", "_tap_get_payment", [this.state.datas.id]);
            // console.log('payyy', pays)
        }  catch (error) {
            console.log('catch')
            this._showTapError(error);
            return false;
        }

    }
});
