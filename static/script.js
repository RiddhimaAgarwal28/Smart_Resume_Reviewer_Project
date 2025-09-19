document.getElementById("resumeForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const loading = document.getElementById("loading");
  const results = document.getElementById("results");
  loading.classList.remove("hidden");
  results.classList.add("hidden");

  const role = document.getElementById("role").value;
  const jd = document.getElementById("jd").value;
  const resumeFile = document.getElementById("resumeFile").files[0];
  const resumeText = document.getElementById("resumeText").value;

  let formData = new FormData();
  formData.append("role", role);
  formData.append("jd", jd);

  if (resumeFile) {
    formData.append("resumeFile", resumeFile);
  } else if (resumeText.trim()) {
    formData.append("resumeText", resumeText);
  } else {
    alert("Please upload a resume file or paste text.");
    loading.classList.add("hidden");
    return;
  }

  try {
    const response = await fetch("/api/review", {
      method: "POST",
      body: formData
    });
    const data = await response.json();

    document.getElementById("feedback").innerText =
      data.feedback || "No feedback returned";

    document.getElementById("present").innerText =
      Array.isArray(data.present) ? data.present.join(", ") : (data.present || "—");

    document.getElementById("missing").innerText =
      Array.isArray(data.missing) ? data.missing.join(", ") : (data.missing || "—");

    document.getElementById("improved").textContent =
      data.improved_resume || "—";

    loading.classList.add("hidden");
    results.classList.remove("hidden");
  } catch (err) {
    alert("Error connecting to backend: " + err.message);
    loading.classList.add("hidden");
  }
});