/** @odoo-module **/

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
    });
},
onClickTest(amount) {
    const is_clicked=true
    let price=0;
    console.log("Clicked Test Button",this);
    console.log("amount",amount.props.paymentLines);
    amount.props.paymentLines.forEach(line => {
        if(line.payment_method_id.name === 'Tap'){
            price=line.amount;
            console.log('price',price)
        }
        console.log('lines',line.payment_method_id)
    })
    this.sendPaymentRequest(this.pos.selectedOrder.uuid,price)

},
    async sendPaymentRequest(uuid,price) {
        console.log('1',this.pos.getOrder())
        console.log('2',uuid)

        return this._createTapPayment(uuid,price);
    },
    async _createTapPayment(uuid,price) {
        let method_id
        try {
            console.log('this',this)
            console.log('pay',this.pos.session.id)
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
             this.state.methods=method_id
            console.log('ddd',data)
            if (!["CREATED"].includes(data.status)) {
                this._showTapError(_t("Failed to initiate payment: %s", data.status));
                return false;
            }

            await this.pos.data.synchronizeLocalDataInIndexedDB();
            const { promise, resolve } = Promise.withResolvers();
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
     async onClickCheck(line){
        console.log('check',this)
        try {

            console.log('payyy', this.state.datas.id)
            const pay_details=await this.orm.call("pos.payment.method", "tap_get_payment", [this.state.methods,this.state.datas.id],{});

                 console.log('payyys', pay_details)
            if (pay_details.status === 'CREATED'){
                console.log('else')

                 this._showTapError('payment pending');
            }
            else {
                console.log('tap')
                 line.setPaymentStatus('done')
            }

        }  catch (error) {
            console.log('catch')
            this._showTapError(error);
            return false;
        }

    }
});
