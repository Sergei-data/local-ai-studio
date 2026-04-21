let lastPayload = null;
let lastDraft = null;

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || `Request failed: ${response.status}`);
  }

  return data;
}

function getCheckedValues(name) {
  return [...document.querySelectorAll(`input[name="${name}"]:checked`)].map(
    (item) => item.value
  );
}

function setList(elementId, items) {
  const container = document.getElementById(elementId);
  container.innerHTML = "";

  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item;
    container.appendChild(li);
  }
}

function setText(id, value) {
  document.getElementById(id).textContent = value || "—";
}

function renderContracts(contracts) {
  const container = document.getElementById("contracts-output");
  container.innerHTML = "";

  if (!contracts || !contracts.length) {
    container.innerHTML = "<div class='muted'>Контракты пока не сформированы</div>";
    return;
  }

  for (const contract of contracts) {
    const card = document.createElement("div");
    card.className = "contract-card";

    card.innerHTML = `
      <h4>${contract.module_name}</h4>
      <p>${contract.purpose}</p>
      <div><strong>Files:</strong><br>${contract.files.join("<br>")}</div>
      <div><strong>Inputs:</strong><br>${contract.inputs.join("<br>") || "—"}</div>
      <div><strong>Outputs:</strong><br>${contract.outputs.join("<br>") || "—"}</div>
      <div><strong>Dependencies:</strong><br>${contract.dependencies.join("<br>") || "—"}</div>
      <div><strong>Tests:</strong><br>${contract.tests.join("<br>") || "—"}</div>
    `;

    container.appendChild(card);
  }
}

function renderDraft(draft) {
  setText("summary-output", draft.summary);
  setText("tree-output", draft.directory_tree.join("\n"));
  setText("prompt-output", draft.prompt_template);
  setList("modules-output", draft.selected_modules);
  setList("infra-output", draft.infra_files);
  setList("steps-output", draft.generation_steps);
  setList("tests-output", draft.test_strategy);
  renderContracts(draft.module_contracts);
}

function buildPayload(form) {
  const formData = new FormData(form);

  return {
    project_name: formData.get("project_name"),
    project_type: formData.get("project_type"),
    backend_framework: formData.get("backend_framework"),
    architecture_style: formData.get("architecture_style"),
    database: formData.get("database"),
    storage: formData.get("storage"),
    object_storage: formData.get("object_storage"),
    auth: formData.get("auth"),
    queue: formData.get("queue"),
    cache: formData.get("cache"),
    monitoring: getCheckedValues("monitoring"),
    migrations: formData.get("migrations"),
    testing: getCheckedValues("testing"),
    containerization: formData.get("containerization"),
    gateway: formData.get("gateway"),
    docs_mode: formData.get("docs_mode"),
    description: formData.get("description"),
  };
}

async function loadDrafts() {
  const drafts = await requestJson("/api/architecture/drafts");
  const container = document.getElementById("drafts-list");
  container.innerHTML = "";

  if (!drafts.length) {
    container.innerHTML = "<div class='muted'>Сохранённых архитектур пока нет</div>";
    return;
  }

  for (const item of drafts) {
    const card = document.createElement("div");
    card.className = "draft-card";

    const title = document.createElement("strong");
    title.textContent = item.request.project_name;

    const meta = document.createElement("div");
    meta.className = "draft-meta";
    meta.textContent = `${item.request.backend_framework} / ${item.request.architecture_style}`;

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = "Открыть";
    button.addEventListener("click", () => {
      lastDraft = item.draft;
      renderDraft(item.draft);
      document.getElementById("architecture-status").textContent =
        `Открыт сохранённый draft: ${item.request.project_name}`;
    });

    card.appendChild(title);
    card.appendChild(meta);
    card.appendChild(button);

    container.appendChild(card);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("architecture-form");
  const buildButton = document.getElementById("build-architecture-btn");
  const saveButton = document.getElementById("save-architecture-btn");
  const status = document.getElementById("architecture-status");

  loadDrafts().catch((error) => {
    status.textContent = `Ошибка загрузки draft'ов: ${String(error)}`;
  });

  buildButton.addEventListener("click", async (event) => {
    event.preventDefault();
    status.textContent = "Строим архитектуру...";

    try {
      lastPayload = buildPayload(form);
      lastDraft = await requestJson("/api/architecture/construct", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(lastPayload),
      });

      renderDraft(lastDraft);
      status.textContent = "Архитектура построена";
    } catch (error) {
      status.textContent = `Ошибка: ${String(error)}`;
    }
  });

  saveButton.addEventListener("click", async (event) => {
    event.preventDefault();

    if (!lastPayload) {
      status.textContent = "Сначала построй архитектуру";
      return;
    }

    status.textContent = "Сохраняем архитектуру...";

    try {
      await requestJson("/api/architecture/save", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(lastPayload),
      });

      status.textContent = "Архитектура сохранена";
      await loadDrafts();
    } catch (error) {
      status.textContent = `Ошибка сохранения: ${String(error)}`;
    }
  });
});