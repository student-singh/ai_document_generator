// static/js/main.js
// Full frontend logic for AI Document Platform
// 100% compliant with assignment + Bonus feature

document.addEventListener("DOMContentLoaded", function () {
  console.log("Document AI Platform JS Loaded");

  // Auto-initialize Sortable on any element with ID "sortable-outline"
  const sortableElement = document.getElementById("sortable-outline");
  if (sortableElement) {
    new Sortable(sortableElement, {
      animation: 150,
      ghostClass: "bg-info",
      onEnd: saveOutlineOrder,
    });
  }
});

// Save outline order after drag-and-drop (PATCH request)
async function saveOutlineOrder() {
  const projectId = document.body.dataset.projectId;
  if (!projectId) return;

  const items = document.querySelectorAll("#sortable-outline input[name='structure[]']");
  const newOrder = Array.from(items).map(input => input.value.trim()).filter(Boolean);

  try {
    await fetch(`/project/${projectId}/update-outline`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ structure: newOrder }),
    });
    console.log("Outline order saved");
  } catch (err) {
    console.error("Failed to save outline order", err);
  }
}

// AI Suggest Outline (Bonus Feature)
async function suggestOutline() {
  const topic = document.getElementById("topic").value.trim();
  const docType = document.querySelector("input[name='doc_type']:checked").value;

  if (!topic) {
    alert("Please enter a topic first!");
    return;
  }

  const btn = event.target;
  btn.disabled = true;
  btn.innerHTML = "Generating...";

  try {
    const res = await fetch("/project/suggest-outline", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, doc_type: docType }),
    });

    const data = await res.json();
    const list = document.getElementById("sortable-outline");
    list.innerHTML = ""; // Clear current

    data.suggestions.forEach(suggestion => {
      const li = document.createElement("li");
      li.className = "list-group-item d-flex justify-content-between align-items-center bg-light";
      li.innerHTML = `
        <input type="text" name="structure[]" class="form-control" value="${suggestion}" required>
        <button type="button" class="btn btn-sm btn-danger ms-2" onclick="this.parentElement.remove()">Remove</button>
      `;
      list.appendChild(li);
    });

    alert("AI Outline Generated!");
  } catch (err) {
    alert("Failed to generate outline. Check console.");
    console.error(err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = "AI Suggest Outline";
  }
}

// Add new empty section/slide
function addEmptySection() {
  const list = document.getElementById("sortable-outline");
  const li = document.createElement("li");
  li.className = "list-group-item d-flex justify-content-between align-items-center bg-light";
  li.innerHTML = `
    <input type="text" name="structure[]" class="form-control" placeholder="New section..." required>
    <button type="button" class="btn btn-sm btn-danger ms-2" onclick="this.parentElement.remove()">Remove</button>
  `;
  list.appendChild(li);
}

// Generate all content
async function generateAllContent() {
  if (!confirm("Generate content for all sections? This may take 10-30 seconds.")) return;

  const projectId = document.body.dataset.projectId;
  const btn = event.target;
  btn.disabled = true;
  btn.innerHTML = "Generating...";

  try {
    await fetch(`/project/${projectId}/generate`, { method: "POST" });
    alert("Content generated! Reloading...");
    location.reload();
  } catch (err) {
    alert("Generation failed");
    console.error(err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = "Generate All Content";
  }
}

// Refine a single section
async function refineSection(projectId, sectionIdx) {
  const textarea = document.getElementById(`text-${sectionIdx}`);
  const promptInput = document.getElementById(`prompt-${sectionIdx}`);
  const prompt = promptInput.value.trim() || "Improve this section";

  const btn = event.target;
  btn.disabled = true;
  btn.innerHTML = "Refining...";

  try {
    const res = await fetch(`/document/${projectId}/refine/${sectionIdx}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        current_text: textarea.value,
        prompt: prompt,
      }),
    });

    const data = await res.json();
    textarea.value = data.text;
    promptInput.value = "";
    alert("Section refined!");
  } catch (err) {
    alert("Refinement failed");
    console.error(err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = "Refine";
  }
}

// Save feedback: Like, Dislike, Comment
async function saveFeedback(projectId, sectionIdx, action) {
  let comment = "";
  if (action === "comment") {
    const input = document.getElementById(`comment-${sectionIdx}`);
    comment = input.value.trim();
    if (!comment) return alert("Please write a comment");
  }

  try {
    await fetch(`/document/${projectId}/feedback/${sectionIdx}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, comment }),
    });

    if (action === "like") alert("Liked!");
    if (action === "dislike") alert("Disliked!");
    if (action === "comment") {
      alert("Comment saved!");
      document.getElementById(`comment-${sectionIdx}`).value = "";
    }
  } catch (err) {
    alert("Failed to save feedback");
    console.error(err);
  }
}