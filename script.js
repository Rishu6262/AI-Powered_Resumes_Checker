async function analyzeResume() {

    const resumeText =
        document.getElementById("resumeText").value;

    const jobRole =
        document.getElementById("jobRole").value;

    const formData = new FormData();

    formData.append("resume_text", resumeText);
    formData.append("job_role", jobRole);

    const response = await fetch("/analyze", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("result").innerHTML = `
        <h2>Analysis Result</h2>

        <p><b>Shortlisted:</b> ${data.shortlisted}</p>

        <p><b>Confidence:</b>
        ${data.confidence}%</p>

        <p><b>Skills Found:</b>
        ${data.nlp_analysis.extracted_skills.join(", ")}</p>

        <p><b>Skill Match:</b>
        ${data.match_metrics.skill_match_score}%</p>

        <p><b>Missing Skills:</b>
        ${data.match_metrics.missing_skills.join(", ")}</p>

        <p><b>Recommendations:</b></p>

        <ul>
            ${data.recommendations
                .map(r => `<li>${r}</li>`)
                .join("")}
        </ul>
    `;
}