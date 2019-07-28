<template>
    <div class="document">
        <!-- eslint-disable -->
        <h3 align="center">
            Summarization Highlight
        </h3>
        <p>You are being invited to take part in a research project. Before you decide whether or not to participate, <strong>it is important for you to understand why the research is being done and what it will involve</strong>.</p>
        <p>Please take time to read the following information carefully and discuss it with others if you wish. Ask us if there is anything that is not clear or if you would like more information. Take time to decide whether or not you wish to take part. All information provided will be anonymous and will be used for academic purposes only.</p>
        <p>This task requires two steps:</p>
        <p><strong>Step 1: Highlighting Informative Phrases in the Document</strong></p>
        <p>Your first task is <strong>to select important phrases </strong> from the document by highlighting them.</p>
        <p>You should first read the document and select phrases that are the most informative. <strong>Use the 5W1H principle (who, what, when, where, why and how)</strong> to determine the informativeness of a phrase: <br/></p>
            <blockquote>
            Who was involved? <br/>
            What happened? <br/>
            Where did it take place? <br/>
            When did it take place? <br/>
            Why did that happen? <br/>
            How did it happen? <br/>
            </blockquote>
        <p>An example of highlights:</p>
        <blockquote>
            <em><a class="highlight">Juan David Ortiz, a 35-year-old</a> supervisory <a class="highlight">Border Patrol agent </a>, has been <a class="highlight">charged</a> with <a class="highlight">four counts of murder</a>, <a class="highlight">aggravated assault</a> and <a class="highlight">unlawful restraint</a>. All of <a class="highlight">his victims were sex workers</a>, but <a class="highlight">one woman</a>, who managed to escape, <a class="highlight">helped law enforcement find him</a>.</em>
        </blockquote>

        <p>The maximum combined length of all highlighted phrases is 30 words. If you feel that 30 words is not enough to highlight all important information, then highlight only the most important parts that fit within this limit. The task should be possible to complete in less than 10 minutes.</p>
        <hr/>
        <p><strong>Step 2: Sanity Check</strong></p>
        <p><strong>Please read the whole document before you do the highlighting</strong>. After you have submitted the evaluation, there will be one simple True/False question where we will verify whether you have read the document or not. Failure to answer the question correctly will invalidate the evaluation that the participant has done.</p>
        <hr/>
        <p>We will draw one lucky winner from the participants to win a £15 Amazon voucher. <strong>You have to complete this task at least twice to be eligible for the lucky draw</strong>. Simply refresh the link to restart the task after you have submitted the result. You are welcome to do the task more than twice but please avoid doing it more than 5 times. We will ignore any excess submission.</p>
        <hr/>
        <p>It is up to you to decide whether or not to take part. If you do decide to take part you will be asked to click a consent button at the end of this section, of which you can still withdraw at any time before we processed the data (3 days after the closing date) without any consequences.</p>
        <p>You do not have to give a reason. If you wish to withdraw from this research, please contact <a href="mailto:hhardy2@sheffield.ac.uk">the organizer</a></p>
        <p></p>

        <p>All the information that we collect about you during the course of the research will be kept strictly confidential and will only be accessible to members of the research team. It will not be possible to be identified in any reports or publications unless you have given us your explicit consent for this. We will not share any of your information to other parties.</p>

        <p>According to data protection legislation, we are required to inform you that the legal basis we are applying in order to process your personal data is that ‘processing is necessary for the performance of a task carried out in the public interest’ (Article 6(1)(e)).</p>
        <p>Further information can be found in the <a target="_blank" href="https://www.sheffield.ac.uk/govern/data-protection/privacy/general.">University’s Privacy Notice</a>
        </p>


        <p>Thank you for reading this</p>

        <p>
Contact details of organizer:<br/><br/>

Hardy<br/>
PhD Student<br/>
The University of Sheffield<br/>
hhardy2@sheffield.ac.uk<br/>
        </p>

        <p>
            Do you consent for all the information that you have submitted to be used
            anonymously for research purposes only?
        </p>
        <!-- eslint-enable -->
    </div>
</template>

<script>
export default {
  name: 'LandingHighlight',
};
</script>
<style scoped lang="scss">
h3 {
    margin-top: 2rem;
    margin-bottom: 3rem;
}
.document {
  font-family: 'Lora', serif;
  font-size: 1.1rem;
  line-height: 1.5rem;
  padding-left: 2rem;
  padding-right: 2rem;
  padding-bottom: 2rem;
}
.highlight{
  background-color: greenyellow;
}
</style>
