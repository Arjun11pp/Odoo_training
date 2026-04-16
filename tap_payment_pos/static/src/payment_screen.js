/** @odoo-module **/

import { PaymentScreenPaymentLines } from "@point_of_sale/app/screens/payment_screen/payment_lines/payment_lines";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { PaymentInterface } from "@point_of_sale/app/utils/payment/payment_interface";
import {PaymentTap} from "./payment_tap";

console.log('123333')
patch(PaymentScreenPaymentLines.prototype, {

onClickTest() {

    console.log("Clicked Test Button",this);
    this.sendPaymentRequest(this.pos.selectedOrderUuid)
},
    async sendPaymentRequest(uuid) {
        console.log('1',this.pos.getOrder().prototype)
        console.log('2',uuid)
        const paymentLine = this.pos.getOrder().getPaymentlineByUuid(uuid);
        console.log('paymentline',paymentLine)
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
        return this._createTapPayment(paymentLine);
    },
    async _createTapPayment(paymentLine) {
        console.log('12')
        try {
            console.log('this',this)
            console.log('pay',paymentLine)
            const data = await this.pos.data.call("pos.payment.method", "tap_create_payment", [
                this.payment_method_id.id,
                paymentLine.amount, paymentLine.uuid,
                this.pos.session.id,
            ]);
            console.log(data)
            if (!["CREATED"].includes(data.status)) {
                this._showTapError(_t("Failed to initiate payment: %s", data.status));
                return false;
            }
            if (data.url) {
                // browser.open(data.url, "_blank");
                // redirect(data.url.href);
            }
            paymentLine.transaction_id = data.id;
            await this.pos.data.synchronizeLocalDataInIndexedDB();
            const { promise, resolve } = Promise.withResolvers();
            this.paymentLineResolvers[paymentLine.uuid] = resolve;
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
    }
});
