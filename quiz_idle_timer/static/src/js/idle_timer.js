import { patch } from "@web/core/utils/patch";
import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
// import { SurveyForm} from "../../../../../addons/survey/static/src/interactions/survey_form";
// console.log('132');
// patch(MainComponentsContainer.prototype,{
//     setup(){
//         console.log('this',this);
//     }
// })

 let timer, currSeconds = 0;
export class SurveyFormIdle extends Interaction {
    static selector = ".o_survey_form";

    setup() {
        console.log('123')
    }
    start() {
        console.log('sirst')
        this.idleTimer();
    }
    resetTimer() {
            console.log('moved')
            document.querySelector(".o_survey_idle_timer_container")
                    .style.display = 'none';
            clearInterval(timer);
            currSeconds = 0;
        }

    idleTimer(){
    const timerDataEl = this.el.querySelector(".o_survey_form_content_data_idle");
    const timerData = timerDataEl.dataset;
    const idleTime=timerData.idleTimer
    console.log('timerdata1332',timerData)
     this.timerEl = document.createElement("span");
    console.log("testing",this.timerEl)
            this.timerEl.classList.add("o_survey_idle_timer");
            this.insert(this.timerEl, this.el.querySelector(".o_survey_idle_timer_container"));
            // this.addListener(this.timerEl, "time_up", async () => {
            //     if (this.showingCorrectAnswers) {
            //         await this.nextScreen(this.nextScreenPromise, this.nextScreenOptions);
            //     }
            //     this.submitForm({
            //         skipValidation: true,
            //         isFinish: !this.options.sessionInProgress,
            //     });
            // });
    }
}
registry.category("public.interactions").add("survey.SurveyFormIdle", SurveyFormIdle);