import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
        this.data.connectWebSocket("TAP_PAYMENT_STATUS", (payload) => {
           console.log('payload',payload)
            if (payload.session_id === this.session.id) {
                const paymentLine = this.models["pos.payment"].find(
                    (line) => line.transaction_id === payload.payment_id
                );
                console.log('paymentline',paymentLine);
                if (
                    paymentLine &&
                    !paymentLine.isDone()

                ) {
                    paymentLine.payment_method_id.payment_terminal.handleTapStatusResponse(
                        paymentLine,
                        payload
                    );
                }
            }
        });
    },
});
