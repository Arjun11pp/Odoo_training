// import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
// console.log('132');
// patch(MainComponentsContainer.prototype,{
//     setup(){
//         console.log('this',this);
//     }
// })
    let timer, currSeconds = 0;
export class SurveyForm2 extends Interaction {
    static selector = ".o_survey_form";

    setup() {
        console.log('123')
        this.idleTimer()
    }
    resetTimer() {
            /* Hide the timer text */
            document.querySelector(".o_survey_idle_timer_container")
                    .style.display = 'none';
            /* Clear the previous interval */
            clearInterval(timer);
            /* Reset the seconds of the timer */
            currSeconds = 0;
            /* Set a new interval */
            timer =
                setInterval(startIdleTimer, 1000);
        }
    //     // Define the events that
    //     // would reset the timer

    //     window.onload = this.resetTimer();
    //     window.onmousemove = resetTimer;
    //     window.onmousedown = resetTimer;
    //     window.ontouchstart = resetTimer;
    //     window.onclick = resetTimer;
    //     window.onkeypress = resetTimer;
    //     function startIdleTimer() {
    //         currSeconds++;
    //         /* Set the timer text to the new value */
    //         document.querySelector(".secs")
    //             .textContent = currSeconds;
    //         /* Display the timer text */
    //         document.querySelector(".timertext")
    //             .style.display = 'block';
    //     }
    idleTimer(){
    const timerDataEl = this.el.querySelector(".o_survey_form_content_data");
    const timerData = timerDataEl.dataset;
     this.timerEl = document.createElement("span");
                    console.log("testing",this.timerEl)
            this.timerEl.classList.add("o_survey_idle_timer");
            this.insert(this.timerEl, this.el.querySelector(".o_survey_idle_timer_container"));
    }
}
registry.category("public.interactions").add("survey.SurveyForm2", SurveyForm2);