const form = document.querySelector(".delete-post");

form.addEventListener("submit", handleDelete);

function handleDelete(e) {
  e.preventDefault();
  shouldSubmit = confirm("Confirm to delete post");

  if (shouldSubmit) {
    e.target.submit();
  }
}
