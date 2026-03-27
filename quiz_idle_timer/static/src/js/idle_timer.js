import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { onMounted} from "@odoo/owl";

let timer;
export class SurveyFormIdle extends Interaction {
    static selector  = ".o_survey_form";
    // dynamicContent = {
    // _document: {
    //         "t-on-keydown": this.onKeydown,
    //         "t-on-mousemove":this.onMouseMove,
    //         "t-on-mousedown":this.onMouseMove,
    //     },
    // }
    setup(){
        onMounted(() =>{
            this.idleTimer()
        })
    }
    start() {
        // console.log('sirst')
        this.idleTimer();
    }
    resetTimer() {
         clearInterval(timer);
         this.idleTimer();
        }
        onKeydown() {
            // console.log('keyy')
            this.resetTimer();
    }
    onMouseMove() {
        // console.log('mouse')

        this.resetTimer()
    }


    idleTimer(){
        const timerDataEl = this.el.querySelector(".o_survey_form_content_data_idle");
         const timerData = timerDataEl.dataset;
        const idleTime=timerData.idleTimer_limit
        // console.log('time',idleTime)
        let sec = idleTime;
         timer = setInterval(function () {
            document.getElementById('safeTimerDisplay').innerHTML = '00:' + sec;
            sec--;
            if (sec < 0) {
                clearInterval(timer);
                document.querySelector(".o_survey_navigation_submit[value='next']")?.click();
                    // this.nextPageTimer();
            }

        }, 1000);
         // this.nextPageTimer()
}
            nextPageTimer(){
                    this.idleTimer()
            }

}
registry.category("public.interactions").add("survey.SurveyFormIdle", SurveyFormIdle);