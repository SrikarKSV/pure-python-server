const form = document.querySelector(".delete-post");
const modal = document.querySelector(".modal");

form.addEventListener("submit", openModal);

modal.addEventListener("click", handleDelete);

function handleDelete(e) {
  // If clicked outise modal, exit
  const isOutside = !e.target.closest(".modal-inner");
  if (isOutside) return closeModal();

  // Choose action for deleting post
  const element = e.target;
  if (element.classList.contains("modal-cancel")) return closeModal();
  if (element.classList.contains("modal-delete")) return form.submit();
}

function openModal(e) {
  e.preventDefault();
  modal.classList.add("open");
}

function closeModal() {
  modal.classList.remove("open");
}

// Press escape to exit modal
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeModal();
  }
});
