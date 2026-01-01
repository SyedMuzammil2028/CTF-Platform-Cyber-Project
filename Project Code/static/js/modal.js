document.addEventListener("DOMContentLoaded", () => {
  const modalBackdrop = document.getElementById("challenge-modal");
  const modalTitle = document.getElementById("modal-title");
  const modalMeta = document.getElementById("modal-meta");
  const modalDescription = document.getElementById("modal-description");
  const modalFlagForm = document.getElementById("flag-form");
  const modalFlagInput = document.getElementById("flag-input");
  const modalFlagMsg = document.getElementById("flag-message");
  const openChallengeBtn = document.getElementById("open-challenge-btn");

  let currentChallengeId = null;
  let currentRoute = null;
  let currentFile = null;
  let currentCategory = null;

  document.querySelectorAll(".challenge-card").forEach(card => {
    card.addEventListener("click", async () => {
      const challengeId = card.dataset.challengeId;

      try {
        const resp = await fetch(`/api/challenge/${challengeId}`);
        const data = await resp.json();

        if (data.error) {
          alert(data.error);
          return;
        }

        currentChallengeId = data.id;
        currentRoute = data.route;
        currentFile = data.file;        // ← added
        currentCategory = data.category; // ← added

        modalTitle.textContent = data.title;
        modalMeta.textContent = `${data.category} • ${data.difficulty} • Author: ${data.author}`;
        // modalMeta.textContent = `${data.category} • ${data.difficulty} • ${data.points} pts • Author: ${data.author}`;
        modalDescription.textContent = data.description;

        modalFlagInput.value = "";
        modalFlagMsg.textContent = "";
        modalFlagMsg.style.color = "#ccc";

        // 🔥 Change button label based on category
        if (data.category === "Forensics") {
          openChallengeBtn.textContent = "Download Evidence File";
        } else if (data.category === "OSINT") {
          openChallengeBtn.textContent = "Download File";
        } else if (data.category === "Crypto") {
          openChallengeBtn.textContent = "Download Crypto File";
        } else if (data.category === "Special") {
          openChallengeBtn.textContent = "Download Special File";
        } 
        else {
          openChallengeBtn.textContent = "Open Challenge";
        }

        modalBackdrop.classList.add("show");
      } catch (e) {
        alert("Failed to load challenge data.");
      }
    });
  });

  document.getElementById("modal-close").addEventListener("click", () => {
    modalBackdrop.classList.remove("show");
  });

  modalBackdrop.addEventListener("click", (e) => {
    if (e.target === modalBackdrop) {
      modalBackdrop.classList.remove("show");
    }
  });

  openChallengeBtn.addEventListener("click", () => {

    // -------------------------------
    //     Forensics → Download file
    // -------------------------------
    if (currentCategory === "Forensics" && currentFile) {
      window.location.href = "/forensics/files/" + currentFile;
      return;
    }

    // -------------------------------
    //     OSINT → Download file
    // -------------------------------
    if (currentCategory === "OSINT" && currentFile) {
      window.location.href = "/osint/files/" + currentFile;
      return;
    }

    // -------------------------------
    //     CRYPTO → Download file
    // -------------------------------
    if (currentCategory === "Crypto" && currentFile) {
      window.location.href = "/crypto/files/" + currentFile;
      return;
    }

    // -------------------------------
    //     CRYPTO → Download file
    // -------------------------------
    if (currentCategory === "Special" && currentFile) {
      window.location.href = "/special/files/" + currentFile;
      return;
    }

    // -------------------------------
    //     Web → Open route normally
    // -------------------------------
    if (currentRoute) {
      window.open(currentRoute, "_blank");
    }
  });

  modalFlagForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!currentChallengeId) return;

    const flag = modalFlagInput.value.trim();
    if (!flag) return;

    try {
      const resp = await fetch("/api/submit_flag", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id: currentChallengeId, flag })
      });

      const data = await resp.json();

      modalFlagMsg.textContent = data.message;
      modalFlagMsg.style.color = data.correct ? "#00c853" : "#ff5252";

      if (data.correct) {
        const card = document.querySelector(`.challenge-card[data-challenge-id="${currentChallengeId}"]`);
        if (card) card.classList.add("solved");

        setTimeout(() => {
          modalBackdrop.classList.remove("show");
        }, 1200);
      }

    } catch (e) {
      modalFlagMsg.textContent = "Error submitting flag.";
      modalFlagMsg.style.color = "#ff5252";
    }
  });
});
