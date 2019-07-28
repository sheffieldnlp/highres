<template>
    <div class="document">
        <!-- eslint-disable -->
        <h3 align="center">
            Summarization Highlight
        </h3>
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
        <p>There is a <strong>code</strong> that you have to copy and paste to Amazon platform at the end of the task. Only submissions that correctly answer the True/False question will be deemed as a valid HIT.</p>
        <hr/>
        <p>Thank you for reading this</p>

        <p>
            Do you consent for all the information that you have submitted to be used
            anonymously for research purposes only?
        </p>
        <!-- eslint-enable -->
    </div>
</template>

<script>
export default {
  name: 'LandingHighlightMTurk',
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
