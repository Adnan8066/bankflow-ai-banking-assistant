import {
  Alert,
  Box,
  Chip,
  CircularProgress,
  Paper,
  Stack,
  Typography,
} from "@mui/material";

/** Small shared building blocks used by every page. */

export function PageHeader({ title, subtitle, action }) {
  return (
    <Stack
      direction={{ xs: "column", sm: "row" }}
      justifyContent="space-between"
      alignItems={{ xs: "flex-start", sm: "center" }}
      spacing={2}
      sx={{ mb: 3 }}
    >
      <Box>
        <Typography variant="h5">{title}</Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            {subtitle}
          </Typography>
        )}
      </Box>
      {action}
    </Stack>
  );
}

export function Loader({ label = "Loading demo data...", minHeight = 240 }) {
  return (
    <Box sx={{ display: "grid", placeItems: "center", minHeight, gap: 2 }}>
      <CircularProgress size={32} />
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
    </Box>
  );
}

export function ErrorAlert({ message, onRetry }) {
  if (!message) return null;
  return (
    <Alert
      severity="error"
      sx={{ mb: 2, borderRadius: 2 }}
      action={
        onRetry ? (
          <Typography
            variant="button"
            sx={{ cursor: "pointer", textDecoration: "underline" }}
            onClick={onRetry}
          >
            Retry
          </Typography>
        ) : null
      }
    >
      {message}
    </Alert>
  );
}

export function EmptyState({ title, description, icon, action }) {
  return (
    <Paper
      variant="outlined"
      sx={{
        p: 4,
        textAlign: "center",
        borderRadius: 3,
        borderStyle: "dashed",
        backgroundColor: "#fbfcff",
      }}
    >
      {icon && <Box sx={{ fontSize: 40, color: "text.secondary", mb: 1 }}>{icon}</Box>}
      <Typography variant="subtitle1" fontWeight={700}>
        {title}
      </Typography>
      {description && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
          {description}
        </Typography>
      )}
      {action && <Box sx={{ mt: 2 }}>{action}</Box>}
    </Paper>
  );
}

const STATUS_STYLES = {
  COMPLETED: { color: "success", label: "Completed" },
  PENDING: { color: "warning", label: "Pending" },
  FAILED: { color: "error", label: "Failed" },
  ACTIVE: { color: "success", label: "Active" },
  APPROVED: { color: "info", label: "Approved" },
  REJECTED: { color: "error", label: "Rejected" },
  DORMANT: { color: "warning", label: "Dormant" },
  CLOSED: { color: "default", label: "Closed" },
};

export function StatusChip({ status, size = "small" }) {
  const style = STATUS_STYLES[status] || { color: "default", label: status };
  return (
    <Chip
      size={size}
      color={style.color}
      variant={style.color === "default" ? "outlined" : "filled"}
      label={style.label}
      sx={{ fontWeight: 600 }}
    />
  );
}

export function SectionCard({ title, subtitle, action, children, sx }) {
  return (
    <Paper
      variant="outlined"
      sx={{ p: { xs: 2, md: 2.5 }, borderRadius: 3, height: "100%", ...sx }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
        <Box>
          <Typography variant="h6">{title}</Typography>
          {subtitle && (
            <Typography variant="body2" color="text.secondary">
              {subtitle}
            </Typography>
          )}
        </Box>
        {action}
      </Stack>
      {children}
    </Paper>
  );
}
