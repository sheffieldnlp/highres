<template>
    <div class="document">
        <!-- eslint-disable -->
        <h1 align="center">
            Please Read This Thoroughly Before You Consent!
        </h1>
        <h3>This task requires two steps:</h3>
        <h4><strong>Step 1: Informativeness Assessment</strong></h4>
        <p>Your task is to assess the <strong>informativeness</strong> of a single summary sentence given one reference sentence. The task should be possible to complete in less than <strong>1 minutes</strong>.</p>
        <hr/>
        <p><strong>You have to assess the summary on two metrics:</strong></p>
        <blockquote>
            <strong>All important</strong> information is present in the summary
        </blockquote>
        <p><strong>Meaning:</strong> The summary has all the important information of the sentence.</p>
        <blockquote>
            <strong>Only important</strong> information is in the summary.
        </blockquote>
        <p><strong>Meaning:</strong> All information in the summary is important (in accordance to reference).</p>
        <p><strong>Note:</strong>You should treat that all words in the reference sentence as important, and words that don't appear in reference as not important.</p>
        <p>An example assessment of one reference sentence and two summaries:</p>
        <blockquote>
            <strong>Reference</strong><br/>
            David Robert Joseph Beckham is an English retired professional footballer and current President of Inter Miami CF.
        </blockquote>
        <blockquote>
            <strong>Summary A</strong><br />
            As <a class="highlight">the President of Inter Miami CF</a>, <a class="highlight">David Beckham</a>, <a class="highlight">a retired English footballer</a>, is known for his crossing ability.
            <br/>
            <strong>Summary B</strong><br />
            <a class="highlight">David Beckham is a retired English footballer</a>
        </blockquote>
        <strong>All important information in the reference sentence is in Summary A, while Summary B has only important information.</strong><br/>
        Alternatively, <strong>not all information in Summary A is important, while Summary B doesn't have all the important information from the reference sentence</strong>.
        <p>You will be scoring each summary sentence by stating how strongly you agree or disagree using a slider from scale 1 (strong disagreement) to 100 (strong agreement).</p>
        <hr />
        <h4><strong>Step 2: Sanity Check</strong></h4>
        <p><strong>Please read the reference sentence first before assessing the summary</strong>. After you have submitted the evaluation, there will be one simple True/False question where we will verify whether you have read the reference sentence or not. <strong>Any submission that failed the True/False question will be rejected.</strong></p>
        <hr/>
        <p>There is a <strong>code</strong> that you have to copy and paste to Amazon platform at the end of the task.</p>

        <p>Thank you for reading this</p>
        <p>
            Do you consent for this information to be used
            anonymously for research purposes only?
        </p>
        <!-- eslint-enable -->
    </div>
</template>

<script>
export default {
  name: 'LandingInfRefMTurk',
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
</style>
