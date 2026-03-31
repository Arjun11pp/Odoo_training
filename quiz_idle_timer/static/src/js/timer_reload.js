import { patch } from "@web/core/utils/patch";
import { SurveyForm } from "@survey/interactions/survey_form"
import { patchDynamicContent } from "@web/public/utils";
let timer;
patch(SurveyForm.prototype, {
    setup(){
        super.setup()
        this.idleTimer();
        patchDynamicContent(this.dynamicContent, {
        _document: {
            "t-on-keydown": this.onKeydown.bind(this),
            "t-on-mousemove":this.onMouseMove.bind(this),
            "t-on-mousedown":this.onMouseMove.bind(this),
            },
        })
    },
    submitForm() {
        super.submitForm();
        this.idleTimer();
    },
    resetTimer() {
        /*
        Resets the timer and calls the timer function
         */
         clearInterval(timer);
         this.idleTimer();
    },
    onKeydown() {
        /*
        On key press this function will call resetTimer function
         */
        this.resetTimer();
    },
    onMouseMove() {
        /*
        on any mouse movement or click this function will execute
         */
        this.resetTimer()
    },
    idleTimer(){
        /*
        Gets the timer data from model and create a timer according to the limit
         */
        const timerDataEl = this.el.querySelector(".o_survey_form_content_data_idle");
         const timerData = timerDataEl.dataset;
        let sec = timerData.idleTimer_limit;
        let seconds = timerData.idleTimer_limit;
         timer = setInterval(function (message) {
            document.getElementById('safeTimerDisplay').innerHTML = '00:' + sec;
            sec--;
            if (sec < 0) {
                // alert("You have been ide for : "+ seconds + " seconds");
                clearInterval(timer);
                document.querySelector(".o_survey_navigation_submit[value='next']")?.click();
                const finish=document.querySelector(".o_survey_navigation_submit[value='next']")
                if (finish == null){

                    document.querySelector(".o_survey_navigation_submit[value='finish']")?.click();
                }
            }
        }, 1000);
    }
});