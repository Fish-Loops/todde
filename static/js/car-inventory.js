(function () {
  const ready = (callback) => {
    if (document.readyState === "complete" || document.readyState === "interactive") {
      setTimeout(callback, 0);
    } else {
      document.addEventListener("DOMContentLoaded", callback);
    }
  };

  const buildOption = (value, label) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    return option;
  };

  const setFeedback = (element, message) => {
    if (!element) return;
    if (message) {
      element.textContent = message;
      element.classList.remove("hidden");
    } else {
      element.textContent = "";
      element.classList.add("hidden");
    }
  };

  const resetSelect = (select, placeholder, disable = true) => {
    if (!select) return;
    select.innerHTML = "";
    select.appendChild(buildOption("", placeholder));
    select.disabled = disable;
  };

  ready(() => {
    const form = document.querySelector("#car-filter-form");
    if (!form) return;

    const manufacturerSelect = form.querySelector('[data-role="car-manufacturer"]');
    const modelSelect = form.querySelector('[data-role="car-model"]');
    const yearSelect = form.querySelector('[data-role="car-year"]');
    const priceOutput = form.querySelector('[data-role="car-price"]');
    const trimOutput = form.querySelector('[data-role="car-trim"]');
    const feedback = form.querySelector('[data-role="car-feedback"]');

    const modelsUrl = form.dataset.modelsUrl;
    const variantsUrl = form.dataset.variantsUrl;

    if (!manufacturerSelect || !modelSelect || !yearSelect || !modelsUrl || !variantsUrl) {
      return;
    }

    const state = {
      variants: [],
    };

    const updatePrice = (variant) => {
      if (!priceOutput || !trimOutput) return;
      if (!variant) {
        priceOutput.textContent = "Choose a year to view price";
        trimOutput.textContent = "";
        return;
      }
      priceOutput.textContent = variant.formatted_price;
      trimOutput.textContent = variant.trim ? variant.trim : "";
    };

    resetSelect(modelSelect, "Select a manufacturer first");
    resetSelect(yearSelect, "Select a model first");
    updatePrice(null);

    const fetchWithParams = async (url, params) => {
      const requestUrl = new URL(url, window.location.origin);
      params.forEach(([key, value]) => requestUrl.searchParams.append(key, value));
      const response = await fetch(requestUrl.toString(), {
        credentials: "same-origin",
        headers: {
          "Accept": "application/json",
        },
      });
      if (!response.ok) {
        const errorPayload = await response.json().catch(() => ({}));
        const message = errorPayload.error || `Request failed with status ${response.status}`;
        throw new Error(message);
      }
      return response.json();
    };

    manufacturerSelect.addEventListener("change", async (event) => {
      const manufacturerId = event.target.value;
      setFeedback(feedback, "");
      updatePrice(null);
      resetSelect(yearSelect, "Select a model first");

      if (!manufacturerId) {
        resetSelect(modelSelect, "Select a manufacturer first");
        return;
      }

      modelSelect.disabled = true;
      resetSelect(modelSelect, "Loading models…", true);

      try {
        const payload = await fetchWithParams(modelsUrl, [["manufacturer", manufacturerId]]);
        const models = payload.models || [];
        resetSelect(modelSelect, models.length ? "Select model" : "No models found", !models.length);
        models.forEach((model) => {
          modelSelect.appendChild(buildOption(model.id, model.name));
        });
      } catch (error) {
        resetSelect(modelSelect, "Select a manufacturer first");
        setFeedback(feedback, error.message);
      }
    });

    modelSelect.addEventListener("change", async (event) => {
      const modelId = event.target.value;
      setFeedback(feedback, "");
      updatePrice(null);
      resetSelect(yearSelect, modelId ? "Loading years…" : "Select a model first", true);

      if (!modelId) {
        resetSelect(yearSelect, "Select a model first");
        state.variants = [];
        return;
      }

      try {
        const payload = await fetchWithParams(variantsUrl, [["model", modelId]]);
        state.variants = payload.variants || [];
        if (!state.variants.length) {
          resetSelect(yearSelect, "No years found", true);
          return;
        }
        resetSelect(yearSelect, "Select year", false);
        state.variants.forEach((variant) => {
          const label = variant.trim ? `${variant.year} · ${variant.trim}` : `${variant.year}`;
          const option = buildOption(String(variant.id), label);
          option.dataset.year = variant.year;
          yearSelect.appendChild(option);
        });
      } catch (error) {
        state.variants = [];
        resetSelect(yearSelect, "Select a model first");
        setFeedback(feedback, error.message);
      }
    });

    yearSelect.addEventListener("change", (event) => {
      const variantId = event.target.value;
      if (!variantId) {
        updatePrice(null);
        return;
      }
      const variant = state.variants.find((item) => String(item.id) === String(variantId));
      if (!variant) {
        updatePrice(null);
        return;
      }
      updatePrice(variant);
    });
  });
})();
