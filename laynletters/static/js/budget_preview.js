// Update total live when user edits qty/unit on a budget form.
// Requires rows to have [data-brow], and inputs [data-bqty], [data-bunit],
// and a total display element with id="budget-total".
(function () {
  function recalc() {
    var total = 0;
    var rows = document.querySelectorAll("[data-brow]");
    rows.forEach(function (row) {
      var qEl = row.querySelector("[data-bqty]");
      var uEl = row.querySelector("[data-bunit]");
      var q = parseFloat((qEl && qEl.value) || 0);
      var u = parseFloat((uEl && uEl.value) || 0);
      total += q * u;
    });
    var totalEl = document.getElementById("budget-total");
    if (totalEl) totalEl.innerText = total.toFixed(2);
  }

  document.addEventListener("input", function (e) {
    if (e.target.matches("[data-bqty]") || e.target.matches("[data-bunit]")) {
      recalc();
    }
  });

  // Initial calculation on load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", recalc);
  } else {
    recalc();
  }
})();
