import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { PaymentInterface } from "@point_of_sale/app/utils/payment/payment_interface";
import { register_payment_method } from "@point_of_sale/app/services/pos_store";

export class PaymentTap extends PaymentInterface {
    setup() {
        super.setup(...arguments);
        this.paymentLineResolvers = {};
    }

    async sendPaymentRequest(uuid) {
        const paymentLine = this.pos.getOrder().getPaymentlineByUuid(uuid);
        if (paymentLine.amount < 0) {
            const originalPaymentId = this._findOriginalPaymentId(paymentLine);
            if (!originalPaymentId) {
                this._showTapError(
                    _t("You can only refund an order that was paid for with Tap.")
                );
                return false;
            }
            return this._createTapRefund(paymentLine, originalPaymentId);
        }
        return this._createTapPayment(paymentLine);
    }

    async sendPaymentCancel(order, uuid) {
        const paymentLine = this.pos.getOrder().getPaymentlineByUuid(uuid);
        try {
            await this.pos.data.call("pos.payment.method", "tap_cancel_payment", [
                this.payment_method_id.id,
                paymentLine.transaction_id,
            ]);
            return true;
        } catch (error) {
            this._showTapError(error);
            return false;
        }
    }

    async _createTapPayment(paymentLine) {
        try {
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
                browser.open(data.url, "_blank");
                // redirect(data.url.href);
            }
            paymentLine.transaction_id = data.id;
            await this.pos.data.synchronizeLocalDataInIndexedDB();
            const { promise, resolve } = Promise.withResolvers();
            this.paymentLineResolvers[paymentLine.uuid] = resolve;
            console.log('promise',promise)
            return promise;
        } catch (error) {
            console.log('catch')
            this._showTapError(error);
            return false;
        }
    }

    async _createTapRefund(refundPaymentLine, originalPaymentId) {
         console.log('_createTapRefund')
        try {
            const data = await this.pos.data.call("pos.payment.method", "tap_create_refund", [
                this.payment_method_id.id,
                originalPaymentId,
                Math.abs(refundPaymentLine.amount),
                refundPaymentLine.uuid,
                this.pos.session.id,
            ]);

            if (!["queued", "pending"].includes(data.status)) {
                this._showTapError(_t("Failed to initiate refund: %s", data.status));
                return false;
            }
            refundPaymentLine.transaction_id = data.id;
            return true;
        } catch (error) {
            this._showTapError(error);
            return false;
        }
    }

    _findOriginalPaymentId(refundPaymentLine) {
         console.log('_findOriginalPaymentId')
        const currentOrder = refundPaymentLine.pos_order_id;
        const orderToRefund = currentOrder.lines[0]?.refunded_orderline_id?.order_id;
        if (!orderToRefund) {
            return null;
        }

        const amountDue = Math.abs(currentOrder.remainingDue);
        const matchedPaymentLine = orderToRefund.payment_ids.find(
            (line) =>
                line.payment_method_id.use_payment_terminal === "tap" && line.amount <= amountDue
        );

        return matchedPaymentLine?.transaction_id ?? null;
    }

    handleTapStatusResponse(paymentLine, notification) {
        console.log('status',paymentLine,notification)
        const isSuccessful = notification.status === "PAID";

        if (isSuccessful) {
            paymentLine.card_no = notification.card_no;
            paymentLine.card_type = notification.card_type;
            paymentLine.card_brand = notification.card_brand;
        }

        if (notification.status === "failed") {
            this._showTapError(
                notification.status_reason?.message ??
                    _t("The payment failed for an unknown reason.")
            );
        }
        if (notification.status === "expired") {
            this._showTapError(_t("The payment has timed out."));
        }

        const resolver = this.paymentLineResolvers?.[paymentLine.uuid];
        if (resolver) {
            this.paymentLineResolvers[paymentLine.uuid] = null;
            resolver(isSuccessful);
        } else {
            paymentLine.handlePaymentResponse(isSuccessful);
        }
    }

    _extractErrorMessage(error) {
        if (typeof error === "string") {
            return error;
        }
        if (error.name === "RPC_ERROR") {
            return error.data.message;
        }
        return error.message;
    }

    _showTapError(error) {
        this.env.services.dialog.add(AlertDialog, {
            title: _t("Tap Error"),
            body: this._extractErrorMessage(error),
        });
    }
}

register_payment_method("tap", PaymentTap);
