const ACCESS_KEY = "misasa_demo_access";
const ACCESS_VALUE = "granted-2026";
const PASSWORD_HASH = "8736d6aaaa41933ad6f2623285e8ec7a686c1851f619f8b65f264a8cc8d84b2d";

const toHex = (buffer) =>
  [...new Uint8Array(buffer)].map((value) => value.toString(16).padStart(2, "0")).join("");

async function digest(value) {
  const data = new TextEncoder().encode(value);
  return toHex(await crypto.subtle.digest("SHA-256", data));
}

function hasAccess() {
  return sessionStorage.getItem(ACCESS_KEY) === ACCESS_VALUE;
}

function showEntryContent() {
  document.querySelector("[data-gate]")?.setAttribute("hidden", "");
  document.querySelector("[data-entry]")?.removeAttribute("hidden");
  document.body.classList.add("is-unlocked");
}

function setupAuth() {
  const page = document.body.dataset.page;

  if (page === "entry") {
    if (hasAccess()) showEntryContent();

    const form = document.querySelector("[data-login-form]");
    const input = document.querySelector("[data-password]");
    const error = document.querySelector("[data-login-error]");

    form?.addEventListener("submit", async (event) => {
      event.preventDefault();
      const value = input.value.trim();
      const button = form.querySelector("button");
      button.disabled = true;
      button.textContent = "確認中…";

      if ((await digest(value)) === PASSWORD_HASH) {
        sessionStorage.setItem(ACCESS_KEY, ACCESS_VALUE);
        form.reset();
        error.textContent = "";
        showEntryContent();
        window.scrollTo({ top: 0, behavior: "smooth" });
      } else {
        error.textContent = "パスワードが違います。もう一度お試しください。";
        input.focus();
        input.select();
      }

      button.disabled = false;
      button.textContent = "デモを見る";
    });
    return;
  }

  const isLocalPreview = ["localhost", "127.0.0.1"].includes(window.location.hostname);
  if (!hasAccess() && !isLocalPreview) {
    window.location.replace(new URL("../", window.location.href));
  } else {
    document.documentElement.classList.add("access-ok");
  }
}

function setupInteractions() {
  document.querySelectorAll("[data-logout]").forEach((button) => {
    button.addEventListener("click", () => {
      sessionStorage.removeItem(ACCESS_KEY);
      window.location.href = new URL(button.dataset.logout || "./", window.location.href);
    });
  });

  document.querySelectorAll("[data-tabs]").forEach((tabs) => {
    const buttons = [...tabs.querySelectorAll("[role='tab']")];
    const panels = [...tabs.querySelectorAll("[role='tabpanel']")];
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        buttons.forEach((item) => item.setAttribute("aria-selected", String(item === button)));
        panels.forEach((panel) => {
          panel.hidden = panel.id !== button.getAttribute("aria-controls");
        });
      });
    });
  });

  document.querySelectorAll("[data-accordion-button]").forEach((button) => {
    button.addEventListener("click", () => {
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      document.getElementById(button.getAttribute("aria-controls")).hidden = expanded;
    });
  });

  document.querySelectorAll("[data-font-size]").forEach((button) => {
    button.addEventListener("click", () => {
      document.documentElement.classList.toggle("large-text");
      button.setAttribute("aria-pressed", String(document.documentElement.classList.contains("large-text")));
    });
  });

  const conceptRoot = document.querySelector("[data-top-concepts]");
  if (conceptRoot) {
    const buttons = [...conceptRoot.querySelectorAll("[data-concept]")];
    const panels = [...conceptRoot.querySelectorAll("[data-concept-panel]")];
    const validConcepts = buttons.map((button) => button.dataset.concept);
    const themeColors = { blue: "#0d5e91", orange: "#dd6f2e", green: "#173f35" };

    const activateConcept = (concept, { updateUrl = false, scroll = false } = {}) => {
      if (!validConcepts.includes(concept)) return;
      buttons.forEach((button) => {
        button.setAttribute("aria-selected", String(button.dataset.concept === concept));
      });
      panels.forEach((panel) => {
        panel.hidden = panel.dataset.conceptPanel !== concept;
      });
      document.body.dataset.activeConcept = concept;
      document.querySelector("meta[name='theme-color']")?.setAttribute("content", themeColors[concept]);
      localStorage.setItem("misasa_top_concept", concept);

      if (updateUrl) {
        const url = new URL(window.location.href);
        url.searchParams.set("design", concept);
        url.hash = "";
        history.replaceState(null, "", url);
      }
      if (scroll) window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const requested = new URLSearchParams(window.location.search).get("design");
    const stored = localStorage.getItem("misasa_top_concept");
    activateConcept(validConcepts.includes(requested) ? requested : validConcepts.includes(stored) ? stored : "blue");

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        activateConcept(button.dataset.concept, { updateUrl: true, scroll: true });
      });
    });
  }

  const revealItems = [...document.querySelectorAll("[data-reveal]")];
  if (revealItems.length && "IntersectionObserver" in window) {
    document.documentElement.classList.add("reveal-ready");
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-revealed");
          revealObserver.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8%", threshold: 0.08 },
    );
    revealItems.forEach((item) => revealObserver.observe(item));
  }

  const toast = document.querySelector("[data-toast]");
  document.querySelectorAll("[data-demo-action]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      if (!toast) return;
      toast.textContent = button.dataset.demoAction || "本番では詳細ページや予約システムへ接続できます。";
      toast.classList.add("is-visible");
      clearTimeout(window.demoToastTimer);
      window.demoToastTimer = setTimeout(() => toast.classList.remove("is-visible"), 3200);
    });
  });
}

setupAuth();
document.addEventListener("DOMContentLoaded", setupInteractions);
