import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {

    async printReceipt() {
        super.printReceipt();
        console.log('this1234', this);

        const print_limit=this.config.print_limit
        this.config.print_count+=1
        if(print_limit === this.config.print_count){
             this.dialog.add(AlertDialog, {
                title: _t(" limit reached"),
                body: _t("the  limit reached "),
            });
        }
        console.log(print_limit)

        console.log(this.config.print_count)
    },


});