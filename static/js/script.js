/**
 * script.js
 * ─────────
 * Client-side logic for AI Health Risk Prediction System.
 *
 * Features:
 *  1. Live BMI calculation as user types height/weight
 *  2. Form validation with helpful error messages
 *  3. Loading spinner on form submit
 */

// ─────────────────────────────────────────────────────
// 1. BMI Calculation
// ─────────────────────────────────────────────────────

/**
 * Calculate BMI from height (cm) and weight (kg).
 * Returns null if inputs are invalid.
 */
function calculateBMI(heightCm, weightKg) {
  if (!heightCm || !weightKg || heightCm <= 0 || weightKg <= 0) return null;
  const heightM = heightCm / 100;
  return weightKg / (heightM * heightM);
}

/**
 * Return the BMI category string for a given BMI value.
 */
function getBMICategory(bmi) {
  if (bmi < 18.5) return "Underweight";
  if (bmi < 25)   return "Normal";
  if (bmi < 30)   return "Overweight";
  return "Obese";
}

/**
 * Return a CSS colour for the BMI category (used for the display text).
 */
function getBMIColor(category) {
  switch (category) {
    case "Underweight": return "#17a2b8";
    case "Normal":      return "#28a745";
    case "Overweight":  return "#ffc107";
    case "Obese":       return "#dc3545";
    default:            return "#3b82d4";
  }
}

/**
 * Update the live BMI display card whenever height or weight changes.
 */
function updateBMIDisplay() {
  const heightInput = document.getElementById("height");
  const weightInput = document.getElementById("weight");
  const bmiDisplay  = document.getElementById("bmiDisplay");

  if (!heightInput || !weightInput || !bmiDisplay) return;

  const height = parseFloat(heightInput.value);
  const weight = parseFloat(weightInput.value);
  const bmi    = calculateBMI(height, weight);

  if (bmi === null || isNaN(bmi)) {
    bmiDisplay.style.display = "none";
    return;
  }

  const roundedBMI = bmi.toFixed(1);
  const category   = getBMICategory(bmi);
  const color      = getBMIColor(category);

  // Update values in the card
  const bmiValueEl    = document.getElementById("bmiValue");
  const bmiCategoryEl = document.getElementById("bmiCategory");

  if (bmiValueEl)    { bmiValueEl.textContent = roundedBMI; bmiValueEl.style.color = color; }
  if (bmiCategoryEl) { bmiCategoryEl.textContent = category; bmiCategoryEl.style.background = getBMIBadgeBg(category); }

  bmiDisplay.style.display = "block";
}

function getBMIBadgeBg(category) {
  switch (category) {
    case "Underweight": return "#cce5ff";
    case "Normal":      return "#d4edda";
    case "Overweight":  return "#fff3cd";
    case "Obese":       return "#f8d7da";
    default:            return "#e9f2ff";
  }
}

// ─────────────────────────────────────────────────────
// 2. Form Validation
// ─────────────────────────────────────────────────────

/**
 * Validate all form fields before submission.
 * Returns true if valid, false if any error found.
 */
function validateForm() {
  const fields = [
    { id: "age",            label: "Age",              min: 1,   max: 120 },
    { id: "height",         label: "Height",           min: 100, max: 250 },
    { id: "weight",         label: "Weight",           min: 20,  max: 300 },
    { id: "blood_pressure", label: "Blood Pressure",   min: 60,  max: 250 },
    { id: "glucose",        label: "Blood Glucose",    min: 40,  max: 500 },
    { id: "cholesterol",    label: "Cholesterol",      min: 50,  max: 600 },
    { id: "heart_rate",     label: "Heart Rate",       min: 30,  max: 220 }
  ];

  const dropdowns = ["gender", "smoking", "activity", "family_history"];

  // Clear previous errors
  document.querySelectorAll(".form-error").forEach(el => el.remove());
  document.querySelectorAll(".field-error").forEach(el =>
    el.classList.remove("field-error")
  );

  let isValid  = true;
  let firstErr = null;

  // Check numeric inputs
  for (const f of fields) {
    const el  = document.getElementById(f.id);
    const val = parseFloat(el.value);

    if (el.value.trim() === "" || isNaN(val) || val < f.min || val > f.max) {
      showFieldError(el, `${f.label} must be between ${f.min} and ${f.max}.`);
      if (!firstErr) firstErr = el;
      isValid = false;
    }
  }

  // Check dropdowns
  for (const id of dropdowns) {
    const el = document.getElementById(id);
    if (!el) continue;
    if (el.value === "" || el.value === null) {
      showFieldError(el, "Please select a value.");
      if (!firstErr) firstErr = el;
      isValid = false;
    }
  }

  // Scroll to first error
  if (firstErr) firstErr.scrollIntoView({ behavior: "smooth", block: "center" });

  return isValid;
}

/**
 * Show an inline error message below a form field.
 */
function showFieldError(element, message) {
  element.classList.add("field-error");

  const errorEl = document.createElement("span");
  errorEl.className = "form-error";
  errorEl.textContent = message;
  errorEl.style.cssText = "color:#dc3545; font-size:0.78rem; margin-top:2px;";

  element.parentNode.appendChild(errorEl);
}

// ─────────────────────────────────────────────────────
// 3. Loading Spinner on Submit
// ─────────────────────────────────────────────────────

function showLoading() {
  const btn = document.getElementById("submitBtn");
  if (!btn) return;
  btn.textContent = "⏳ Analysing...";
  btn.disabled = true;
}

// ─────────────────────────────────────────────────────
// 4. Reset BMI Display
// ─────────────────────────────────────────────────────

function resetBMI() {
  const bmiDisplay = document.getElementById("bmiDisplay");
  if (bmiDisplay) bmiDisplay.style.display = "none";
}

// ─────────────────────────────────────────────────────
// 5. Wire up event listeners on DOM ready
// ─────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", function () {

  // Live BMI update
  const heightInput = document.getElementById("height");
  const weightInput = document.getElementById("weight");
  if (heightInput) heightInput.addEventListener("input", updateBMIDisplay);
  if (weightInput) weightInput.addEventListener("input", updateBMIDisplay);

  // Form submission with validation + loading indicator
  const form = document.getElementById("healthForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      if (!validateForm()) {
        e.preventDefault();  // stop form if validation fails
        return;
      }
      showLoading();
      // Form submits normally (no e.preventDefault here)
    });
  }

  // Add field-error CSS inline (small addition so we don't need an extra rule in CSS)
  const style = document.createElement("style");
  style.textContent = `
    .field-error {
      border-color: #dc3545 !important;
      box-shadow: 0 0 0 3px rgba(220,53,69,0.12) !important;
    }
  `;
  document.head.appendChild(style);
});
