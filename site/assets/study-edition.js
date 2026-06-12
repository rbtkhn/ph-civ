(function () {
  function clearActive() {
    document.querySelectorAll(".outline-btn.active").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll(".claim-card.active").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll(".transcript-section.highlight").forEach((el) => el.classList.remove("highlight"));
  }

  function scrollToSlug(slug) {
    const target = document.getElementById(slug);
    if (!target) return;
    clearActive();
    target.classList.add("highlight");
    const btn = document.querySelector(`.outline-btn[data-slug="${slug}"]`);
    if (btn) btn.classList.add("active");
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function scrollToClaim(n) {
    const claim = document.getElementById(`claim-${n}`);
    if (!claim) return;
    clearActive();
    claim.classList.add("active");
    claim.scrollIntoView({ behavior: "smooth", block: "nearest" });
    const anchor = claim.getAttribute("data-anchor");
    if (anchor) scrollToSlug(anchor);
  }

  document.querySelectorAll(".outline-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const slug = btn.getAttribute("data-slug");
      if (slug) scrollToSlug(slug);
    });
  });

  document.querySelectorAll(".claim-marker, .claim-jump").forEach((btn) => {
    btn.addEventListener("click", (event) => {
      event.stopPropagation();
      const anchor = btn.getAttribute("data-anchor");
      const claim = btn.getAttribute("data-claim");
      if (claim) {
        scrollToClaim(claim);
        return;
      }
      if (anchor) scrollToSlug(anchor);
    });
  });

  document.querySelectorAll(".claim-card").forEach((card) => {
    card.addEventListener("click", () => {
      const n = card.getAttribute("data-claim");
      if (n) scrollToClaim(n);
    });
  });
})();
