import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { patchDynamicContent } from "@web/public/utils";
let timer;
console.log('ready')
export class SurveyFormIdle extends Interaction {
    static selector  = ".o_survey_form";
    dynamicContent = {
    _document: {
            "t-on-keydown": this.onKeydown,
            "t-on-mousemove":this.onMouseMove,
            "t-on-mousedown":this.onMouseMove,
        },
    }
     setup() {
     }
    start() {
        console.log('start2')
        this.idleTimer();
    }

    resetTimer() {
        /*
        Resets the timer and calls the timer function
         */
         clearInterval(timer);
         this.idleTimer();
    }
    onKeydown() {
        /*
        On key press this function will call resetTimer function
         */
        this.resetTimer();
    }
    onMouseMove() {
        /*
        on any mouse movement or click this function will execute
         */
        this.resetTimer()
    }

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
                    console.log('submit')
                    document.querySelector(".o_survey_navigation_submit[value='finish']")?.click();
                }
            }
        }, 1000);
    }
}
registry.category("public.interactions").add("survey.SurveyFormIdle", SurveyFormIdle);