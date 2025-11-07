(function () {
  const ready = (callback) => {
    if (document.readyState === "complete" || document.readyState === "interactive") {
      setTimeout(callback, 0);
    } else {
      document.addEventListener("DOMContentLoaded", callback, { once: true });
    }
  };

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

  const parseNumber = (value, fallback) => {
    const parsed = typeof value === "number" ? value : parseFloat(String(value).replace(/,/g, ""));
    return Number.isFinite(parsed) ? parsed : fallback;
  };

  const formatCurrency = (value, currency) => {
    if (!Number.isFinite(value)) {
      return "—";
    }
    const formatter = new Intl.NumberFormat("en-NG", {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    });
    return formatter.format(Math.round(value));
  };

  const quantize = (value) => Math.round(value || 0);

  let renderLoanSummary = null;

  const initVehicleGallery = () => {
    const galleryFrame = document.querySelector("[data-vehicle-gallery]");
    if (!galleryFrame) {
      if (window.console && typeof window.console.warn === "function") {
        console.warn("[Todde] Vehicle gallery: frame not found");
      }
      return;
    }

    const mainImage = galleryFrame.querySelector("[data-gallery-image]");
    if (!mainImage) {
      if (window.console && typeof window.console.warn === "function") {
        console.warn("[Todde] Vehicle gallery: main image not found");
      }
      return;
    }

    const prevButton = galleryFrame.querySelector("[data-gallery-prev]");
    const nextButton = galleryFrame.querySelector("[data-gallery-next]");
    const thumbScope = galleryFrame.parentElement || document;
    const thumbnailElements = Array.from(thumbScope.querySelectorAll("[data-gallery-thumb]"));

    if (window.console && typeof window.console.debug === "function") {
      console.debug("[Todde] Vehicle gallery init", {
        hasPrev: Boolean(prevButton),
        hasNext: Boolean(nextButton),
        thumbnailCount: thumbnailElements.length,
      });
    }

    const images = [];
    const normalizeText = (value, fallback = "") => {
      if (typeof value !== "string") return fallback;
      const trimmed = value.trim();
      return trimmed.length ? trimmed : fallback;
    };

    const registerImage = (src, alt) => {
      const normalizedSrc = normalizeText(src);
      if (!normalizedSrc) return;
      images.push({
        src: normalizedSrc,
        alt: normalizeText(alt, mainImage.getAttribute("alt") || ""),
      });
    };

    registerImage(mainImage.dataset.initialSrc || mainImage.getAttribute("src"), mainImage.dataset.initialAlt || mainImage.getAttribute("alt"));

    thumbnailElements.forEach((thumb) => {
      const thumbImg = thumb.querySelector("img");
      const source = thumb.dataset.src || thumb.getAttribute("href") || (thumbImg ? thumbImg.getAttribute("src") : "");
      const alt = thumb.dataset.alt || (thumbImg ? thumbImg.getAttribute("alt") : "");
      registerImage(source, alt);
    });

    if (images.length === 0) {
      if (window.console && typeof window.console.warn === "function") {
        console.warn("[Todde] Vehicle gallery: no images registered");
      }
      return;
    }

    let currentIndex = 0;

    const updateActiveThumb = () => {
      thumbnailElements.forEach((thumb, index) => {
        const isActive = index + 1 === currentIndex;
        thumb.classList.toggle("ring-2", isActive);
        thumb.classList.toggle("ring-todde-blue", isActive);
        thumb.classList.toggle("ring-offset-2", isActive);
        thumb.setAttribute("aria-current", isActive ? "true" : "false");
      });
    };

    const showImage = (index) => {
      if (images.length === 0) return;
      const normalizedIndex = (index + images.length) % images.length;
      const target = images[normalizedIndex];
      if (!target) return;
      currentIndex = normalizedIndex;
      if (mainImage.getAttribute("src") !== target.src) {
        mainImage.setAttribute("src", target.src);
      }
      mainImage.setAttribute("alt", target.alt || mainImage.getAttribute("alt") || "");
      mainImage.dataset.galleryIndex = String(currentIndex);
      if (window.console && typeof window.console.debug === "function") {
        console.debug("[Todde] Vehicle gallery show", { index: currentIndex, src: target.src });
      }
      updateActiveThumb();
    };

    if (prevButton) {
      prevButton.addEventListener("click", (event) => {
        event.preventDefault();
        if (window.console && typeof window.console.debug === "function") {
          console.debug("[Todde] Vehicle gallery prev", { from: currentIndex, to: currentIndex - 1 });
        }
        showImage(currentIndex - 1);
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", (event) => {
        event.preventDefault();
        if (window.console && typeof window.console.debug === "function") {
          console.debug("[Todde] Vehicle gallery next", { from: currentIndex, to: currentIndex + 1 });
        }
        showImage(currentIndex + 1);
      });
    }

    thumbnailElements.forEach((thumb, index) => {
      const targetIndex = index + 1;
      thumb.dataset.galleryIndex = String(targetIndex);
      thumb.addEventListener("click", (event) => {
        event.preventDefault();
        if (window.console && typeof window.console.debug === "function") {
          console.debug("[Todde] Vehicle gallery thumb", { targetIndex });
        }
        showImage(targetIndex);
      });
      thumb.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          if (window.console && typeof window.console.debug === "function") {
            console.debug("[Todde] Vehicle gallery thumb key", { targetIndex, key: event.key });
          }
          showImage(targetIndex);
        }
      });
    });

    if (window.console && typeof window.console.debug === "function") {
      console.debug("[Todde] Vehicle gallery ready", { imageCount: images.length });
    }
    showImage(0);
  };

  const initLoanCalculator = () => {
    const form = document.getElementById("loan-calculator");
    if (!form) return;

    const price = parseNumber(form.dataset.price, 0);
    const currency = (form.dataset.currency || "NGN").toUpperCase();
    const defaultDeposit = parseNumber(form.dataset.defaultDeposit, 30);
    const defaultRate = parseNumber(form.dataset.defaultRate, 18);
    const defaultPeriod = parseNumber(form.dataset.defaultPeriod, 24);

    const depositInput = form.querySelector("#loan-deposit-percent");
    const depositRange = form.querySelector("#loan-deposit-range");
    const periodInput = form.querySelector("#loan-period");
    const depositAmountLabel = form.querySelector("#loan-deposit-amount");
    const depositDisplay = form.querySelector("#loan-deposit");
    const loanAmountDisplay = form.querySelector("#loan-amount");
    const monthlyDisplay = form.querySelector("#loan-monthly");
    const feedback = form.querySelector("#loan-calculator-feedback");

    if (!depositInput || !depositRange || !periodInput || !depositAmountLabel || !depositDisplay || !loanAmountDisplay || !monthlyDisplay) {
      return;
    }

    const depositMin = parseNumber(depositInput.getAttribute("min"), 10);
    const depositMax = parseNumber(depositInput.getAttribute("max"), 80);
    const periodMin = parseNumber(periodInput.getAttribute("min"), 12);
    const periodMax = parseNumber(periodInput.getAttribute("max"), 48);

    const updateDisplays = (summary) => {
      const depositFormatted = summary.depositFormatted ?? "—";
      const loanFormatted = summary.loanFormatted ?? "—";
      const monthlyFormatted = summary.monthlyFormatted ?? "—";
      depositAmountLabel.textContent = depositFormatted;
      depositDisplay.textContent = depositFormatted;
      loanAmountDisplay.textContent = loanFormatted;
      monthlyDisplay.textContent = monthlyFormatted;
    };

    const computeSummary = ({ priceValue, depositPercent, ratePercent, periodMonths }) => {
      const depositAmount = quantize(priceValue * (depositPercent / 100));
      const loanAmount = Math.max(quantize(priceValue - depositAmount), 0);
      const months = Math.max(Math.round(periodMonths), 1);
      const annualRate = Math.max(ratePercent, 0);
      const monthlyRate = annualRate > 0 ? annualRate / 100 / 12 : 0;
      let monthlyPayment;
      if (monthlyRate <= 0) {
        monthlyPayment = months > 0 ? loanAmount / months : loanAmount;
      } else {
        const factor = Math.pow(1 + monthlyRate, months);
        monthlyPayment = loanAmount * monthlyRate * factor / (factor - 1);
      }
      monthlyPayment = quantize(monthlyPayment);
      return {
        depositAmount,
        loanAmount,
        monthlyPayment,
        depositFormatted: formatCurrency(depositAmount, currency),
        loanFormatted: formatCurrency(loanAmount, currency),
        monthlyFormatted: formatCurrency(monthlyPayment, currency),
      };
    };

    const syncDepositControls = (value) => {
      const normalized = clamp(parseNumber(value, defaultDeposit), depositMin, depositMax);
      depositInput.value = normalized.toFixed(0);
      depositRange.value = normalized;
      return normalized;
    };

    const validateInputs = () => {
      const depositPercent = clamp(parseNumber(depositInput.value, defaultDeposit), depositMin, depositMax);
      const periodMonths = clamp(parseNumber(periodInput.value, defaultPeriod), periodMin, periodMax);

      if (price <= 0) {
        return { error: "Vehicle price unavailable. Please contact Todde to continue." };
      }
      if (depositPercent < depositMin || depositPercent > depositMax) {
        return { error: `Deposit percentage must be between ${depositMin}% and ${depositMax}%.` };
      }
      if (periodMonths < periodMin || periodMonths > periodMax) {
        return { error: `Tenor should be between ${periodMin} and ${periodMax} months.` };
      }
      return {
        depositPercent,
        periodMonths,
      };
    };

    const render = () => {
      const validation = validateInputs();
      if (validation.error) {
        feedback.textContent = validation.error;
        feedback.classList.remove("hidden");
        updateDisplays({
          depositFormatted: "—",
          loanFormatted: "—",
          monthlyFormatted: "—",
        });
        return;
      }
      feedback.textContent = "";
      feedback.classList.add("hidden");
      const summary = computeSummary({
        priceValue: price,
        depositPercent: validation.depositPercent,
        ratePercent: defaultRate,
        periodMonths: validation.periodMonths,
      });
      updateDisplays(summary);
    };

    renderLoanSummary = render;

    depositInput.addEventListener("input", (event) => {
      syncDepositControls(event.target.value);
      render();
    });

    depositRange.addEventListener("input", (event) => {
      syncDepositControls(event.target.value);
      render();
    });

    periodInput.addEventListener("input", render);

    syncDepositControls(defaultDeposit);
    periodInput.value = clamp(defaultPeriod, periodMin, periodMax).toFixed(0);
    render();
  };

  const initLoanTabs = () => {
    const container = document.querySelector("[data-loan-tabs]");
    if (!container) return;

    const triggers = Array.from(container.querySelectorAll("[data-loan-tab]"));
    const panels = Array.from(container.querySelectorAll("[data-loan-panel]"));

    if (triggers.length === 0 || panels.length === 0) {
      return;
    }

    const findTriggerIndex = (name) => triggers.findIndex((trigger) => trigger.dataset.loanTab === name);

    const setActive = (name) => {
      if (!name) return;

      triggers.forEach((trigger) => {
        const isActive = trigger.dataset.loanTab === name;
        trigger.classList.toggle("loan-tab-trigger--active", isActive);
        trigger.setAttribute("aria-selected", String(isActive));
        trigger.setAttribute("tabindex", isActive ? "0" : "-1");
      });

      panels.forEach((panel) => {
        const isActive = panel.dataset.loanPanel === name;
        panel.hidden = !isActive;
        panel.setAttribute("aria-hidden", String(!isActive));
      });

      if (name === "finance" && typeof renderLoanSummary === "function") {
        window.requestAnimationFrame(() => {
          if (typeof renderLoanSummary === "function") {
            renderLoanSummary();
          }
        });
      }
    };

    const focusByIndex = (index) => {
      const clampedIndex = (index + triggers.length) % triggers.length;
      const trigger = triggers[clampedIndex];
      if (trigger) {
        trigger.focus();
        setActive(trigger.dataset.loanTab);
      }
    };

    triggers.forEach((trigger, index) => {
      trigger.addEventListener("click", () => {
        setActive(trigger.dataset.loanTab);
      });

      trigger.addEventListener("keydown", (event) => {
        if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
          event.preventDefault();
          const direction = event.key === "ArrowRight" ? 1 : -1;
          focusByIndex(index + direction);
        } else if (event.key === "Home") {
          event.preventDefault();
          focusByIndex(0);
        } else if (event.key === "End") {
          event.preventDefault();
          focusByIndex(triggers.length - 1);
        }
      });
    });

    const defaultTrigger = triggers.find((trigger) => trigger.classList.contains("loan-tab-trigger--active")) || triggers[0];
    const defaultName = defaultTrigger ? defaultTrigger.dataset.loanTab : null;
    setActive(defaultName);
  };

  ready(() => {
    initVehicleGallery();
    initLoanCalculator();
    initLoanTabs();
  });
})();
