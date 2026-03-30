import { patch } from "@web/core/utils/patch";
import { SurveyForm } from "@survey/interactions/survey_form"

patch(SurveyForm.prototype, {
    submitForm() {
        console.log('patching')
        super.submitForm();

    },
});