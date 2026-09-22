import { Box, Card, CardContent, Stack, Typography } from "@mui/material";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";

/**
 * The four KPI cards on the dashboard (balance, income, expenses, loans).
 */
export default function DashboardCard({
  title,
  value,
  icon,
  caption,
  trend,
  color = "primary.main",
  gradient,
}) {
  return (
    <Card
      sx={{
        height: "100%",
        background: gradient || "#ffffff",
        color: gradient ? "#ffffff" : "inherit",
        transition: "transform 0.18s ease, box-shadow 0.18s ease",
        "&:hover": { transform: "translateY(-3px)", boxShadow: "0 14px 30px rgba(17,26,46,.12)" },
      }}
    >
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
          <Typography
            variant="body2"
            sx={{ fontWeight: 600, color: gradient ? "rgba(255,255,255,.85)" : "text.secondary" }}
          >
            {title}
          </Typography>
          <Box
            sx={{
              display: "grid",
              placeItems: "center",
              width: 42,
              height: 42,
              borderRadius: 2,
              backgroundColor: gradient ? "rgba(255,255,255,.18)" : "#eef2fd",
              color: gradient ? "#ffffff" : color,
            }}
          >
            {icon}
          </Box>
        </Stack>
        <Typography variant="h5" sx={{ mt: 1.5, fontWeight: 800 }}>
          {value}
        </Typography>
        {(caption || trend !== undefined) && (
          <Stack direction="row" spacing={1} alignItems="center" sx={{ mt: 1 }}>
            {trend !== undefined && (
              <Stack
                direction="row"
                alignItems="center"
                spacing={0.5}
                sx={{
                  color: gradient
                    ? "#ffffff"
                    : trend > 0
                      ? "success.main"
                      : trend < 0
                        ? "error.main"
                        : "text.secondary",
                  fontWeight: 700,
                }}
              >
                {trend > 0 ? <TrendingUpIcon fontSize="small" /> : <TrendingDownIcon fontSize="small" />}
                <Typography variant="caption" fontWeight={700}>
                  {trend > 0 ? "+" : ""}
                  {trend}%
                </Typography>
              </Stack>
            )}
            {caption && (
              <Typography
                variant="caption"
                sx={{ color: gradient ? "rgba(255,255,255,.8)" : "text.secondary" }}
              >
                {caption}
              </Typography>
            )}
          </Stack>
        )}
      </CardContent>
    </Card>
  );
}
