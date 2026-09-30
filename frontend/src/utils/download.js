/**
 * Save a blob to disk.
 *
 * The object URL is released a few seconds later rather than immediately: releasing
 * it in the same tick can cancel the download in some browsers.
 */
export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.rel = "noopener";
  link.style.display = "none";
  document.body.appendChild(link);
  link.click();
  setTimeout(() => {
    link.remove();
    URL.revokeObjectURL(url);
  }, 4000);
}

/** Where a notification should take the reader when it is clicked. */
export function notificationTarget(notificationType) {
  switch (notificationType) {
    case "LOAN":
      return "/loans";
    case "TRANSACTION":
      return "/transactions";
    case "SUMMARY":
      return "/dashboard";
    case "SECURITY":
      return "/profile";
    default:
      return "/notifications";
  }
}

export function notificationIconLabel(notificationType) {
  return String(notificationType || "SYSTEM").toLowerCase();
}
