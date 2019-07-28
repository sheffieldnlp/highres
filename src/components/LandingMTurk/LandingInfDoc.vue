<template>
    <div>
        <!-- eslint-disable -->
        <h1 align="center">
            Please Read This Thoroughly Before You Consent!
        </h1>
        <hr/>
        <h3>This task requires two steps:</h3>
        <h4><strong>Step 1: Informativeness Assessment</strong></h4>
        <p>Assess the <strong>informativeness</strong> of a single summary sentence. The task should be possible to complete in less than <strong>3 minutes</strong>.</p>
        <hr/>
        <p><strong>You have to assess the summary on two metrics:</strong></p>
        <blockquote>
            <strong>All important</strong> information is present in the summary
        </blockquote>
        <p><strong>Meaning:</strong> The summary has all the important information of the document.</p>
        <blockquote>
            <strong>Only important</strong> information is in the summary.
        </blockquote>
        <p><strong>Meaning:</strong> All information in the summary is important</p>
        <p>An example assessment of one document where the highlights are important words and two summaries:</p>
        <blockquote>
            <strong>Document</strong><br/>
            <a class="highlight">David Robert Joseph Beckham</a> is an <a class="highlight">English retired professional footballer</a> and current President of Inter Miami CF. He <a class="highlight">played for Manchester United, Preston North End, Real Madrid, Milan, LA Galaxy, Paris Saint-Germain and the England national team</a> (the rest is redacted)
        </blockquote>
        <blockquote>
            <strong>Summary A</strong><br />
            <a class="highlight">David Beckham</a>, <a class="highlight">a retired English footballer</a>, has <a class="highlight">played for 6 clubs and the England national team</a> and is known for his crossing ability.
            <br/>
            <strong>Summary B</strong><br />
            <a class="highlight">David Beckham is a retired English footballer</a>
        </blockquote>
        <strong>All important information in document is in Summary A, while Summary B has only important information.</strong><br/>
        Alternatively, <strong>not all information in Summary A is important, while Summary B doesn't have all the important information from the document</strong>.
        <p>You will be scoring each summary sentence by stating how strongly you agree or disagree using a slider from scale 1 (strong disagreement) to 100 (strong agreement).</p>
        <hr />
        <h4><strong>Step 2: Sanity Check</strong></h4>
        <p><strong>Please read the document (averagely 450 words) first before assessing the summary</strong>. After you have submitted the evaluation, there will be one simple True/False question where we will verify whether you have read the document or not. <strong>Any submission that failed the True/False question will be rejected.</strong></p>
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
  name: 'LandingInfDocMTurk',
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
