import { Box, Stack, Typography } from "@mui/material";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";

import { BRAND } from "../branding.js";

/**
 * The BankFlow mark and wordmark. `tone="light"` is for dark surfaces such as the footer.
 */
export default function BrandLogo({
  size = 40,
  showText = true,
  subtitle = BRAND.tagline,
  tone = "default",
  onClick,
}) {
  const onDark = tone === "light";

  return (
    <Stack
      direction="row"
      spacing={1.25}
      alignItems="center"
      onClick={onClick}
      sx={{ cursor: onClick ? "pointer" : "default" }}
    >
      <Box
        sx={{
          position: "relative",
          display: "grid",
          placeItems: "center",
          width: size,
          height: size,
          borderRadius: `${Math.round(size * 0.3)}px`,
          background: BRAND.gradient,
          color: "#fff",
          boxShadow: "0 8px 20px rgba(19, 45, 110, 0.28)",
          "&::after": {
            content: '""',
            position: "absolute",
            inset: 0,
            borderRadius: "inherit",
            border: "1px solid rgba(255,255,255,.24)",
          },
        }}
      >
        <AccountBalanceIcon sx={{ fontSize: size * 0.5 }} />
      </Box>

      {showText && (
        <Box>
          <Typography
            variant="subtitle1"
            sx={{
              fontWeight: 800,
              letterSpacing: "-0.01em",
              lineHeight: 1.15,
              color: onDark ? "#ffffff" : "text.primary",
            }}
          >
            {BRAND.name}
          </Typography>
          {subtitle && (
            <Typography
              variant="caption"
              sx={{
                display: "block",
                letterSpacing: "0.03em",
                textTransform: "uppercase",
                fontSize: 10,
                color: onDark ? "rgba(255,255,255,.65)" : "text.secondary",
              }}
            >
              {subtitle}
            </Typography>
          )}
        </Box>
      )}
    </Stack>
  );
}
