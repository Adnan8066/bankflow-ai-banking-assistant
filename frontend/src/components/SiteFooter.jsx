import { Box, Chip, Container, Divider, Grid, Link, Stack, Typography } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import ShieldOutlinedIcon from "@mui/icons-material/ShieldOutlined";

import { BRAND, DEMO_ACCOUNTS, FOOTER_LINKS } from "../branding.js";
import { Link as RouterLink } from "react-router-dom";
import BrandLogo from "./BrandLogo.jsx";

const muted = "rgba(255,255,255,.68)";

function FooterColumn({ title, children }) {
  return (
    <Grid item xs={12} sm={6} md={3}>
      <Typography
        variant="caption"
        sx={{ color: "#fff", fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase" }}
      >
        {title}
      </Typography>
      <Stack spacing={1} sx={{ mt: 1.5 }}>
        {children}
      </Stack>
    </Grid>
  );
}

function FooterLink({ href, children, external }) {
  return (
    <Link
      href={href}
      underline="none"
      {...(external ? { target: "_blank", rel: "noreferrer" } : {})}
      sx={{
        color: muted,
        fontSize: 14,
        width: "fit-content",
        transition: "color .18s ease",
        "&:hover": { color: "#fff" },
      }}
    >
      {children}
    </Link>
  );
}

/**
 * variant="full" is used on the public landing page, "slim" inside the application.
 */
export default function SiteFooter({ variant = "full" }) {
  if (variant === "slim") {
    return (
      <Box
        component="footer"
        sx={{
          borderTop: "1px solid",
          borderColor: "divider",
          backgroundColor: "background.paper",
          mt: 4,
          py: 2,
        }}
      >
        <Container maxWidth="xl" sx={{ px: { xs: 2, md: 3 } }}>
          <Stack
            direction={{ xs: "column", sm: "row" }}
            spacing={1.5}
            justifyContent="space-between"
            alignItems={{ xs: "flex-start", sm: "center" }}
          >
            <Stack direction="row" spacing={1.25} alignItems="center">
              <BrandLogo size={26} showText={false} />
              <Typography variant="caption" color="text.secondary">
                {BRAND.name} demo application. All figures are fictional and no real money moves.
              </Typography>
            </Stack>
            <Stack direction="row" spacing={2.5} alignItems="center">
              <Link
                href={BRAND.github}
                target="_blank"
                rel="noreferrer"
                underline="none"
                sx={{ display: "flex", alignItems: "center", gap: 0.75, color: "text.secondary", "&:hover": { color: "primary.main" } }}
              >
                <GitHubIcon sx={{ fontSize: 16 }} />
                <Typography variant="caption">Source code</Typography>
              </Link>
              <Chip size="small" variant="outlined" label={`v${BRAND.version}`} />
            </Stack>
          </Stack>
        </Container>
      </Box>
    );
  }

  return (
    <Box component="footer" sx={{ background: BRAND.footerGradient, color: "#fff", pt: { xs: 5, md: 7 } }}>
      <Container maxWidth="lg">
        <Grid container spacing={{ xs: 4, md: 5 }}>
          <Grid item xs={12} md={4}>
            <BrandLogo size={42} tone="light" subtitle="Demo banking platform" />
            <Typography variant="body2" sx={{ color: muted, mt: 2, maxWidth: 330 }}>
              A full stack demo bank built with React, Django REST Framework and JWT authentication,
              with an AI assistant that answers questions from your own simulated data.
            </Typography>
            <Stack direction="row" spacing={1} sx={{ mt: 2, flexWrap: "wrap", gap: 1 }}>
              <Chip
                size="small"
                icon={<ShieldOutlinedIcon sx={{ fontSize: 16, color: "#fff !important" }} />}
                label="Fictional data only"
                sx={{ backgroundColor: "rgba(255,255,255,.12)", color: "#fff" }}
              />
              <Chip
                size="small"
                label="No real money movement"
                sx={{ backgroundColor: "rgba(255,255,255,.12)", color: "#fff" }}
              />
            </Stack>
          </Grid>

          <FooterColumn title="Product">
            {FOOTER_LINKS.product.map((link) => (
              <FooterLink key={link.label} href={link.href}>
                {link.label}
              </FooterLink>
            ))}
          </FooterColumn>

          <FooterColumn title="Project">
            {FOOTER_LINKS.project.map((link) => (
              <FooterLink key={link.label} href={link.href} external>
                {link.label}
              </FooterLink>
            ))}
          </FooterColumn>

          <FooterColumn title="Demo accounts">
            {DEMO_ACCOUNTS.map((account) => (
              <Box
                key={account.email}
                component={RouterLink}
                to={`/login?demo=${account.role === "Bank employee" ? "admin" : "customer"}`}
                sx={{ display: "block", textDecoration: "none", "&:hover p": { color: "#fff" } }}
              >
                <Typography variant="caption" sx={{ color: "rgba(255,255,255,.5)" }}>
                  {account.role} - click to sign in
                </Typography>
                <Typography variant="body2" sx={{ color: muted, fontSize: 13 }}>
                  {account.email}
                </Typography>
                <Typography variant="caption" sx={{ color: BRAND.accent }}>
                  {account.password}
                </Typography>
              </Box>
            ))}
          </FooterColumn>
        </Grid>

        <Divider sx={{ mt: { xs: 4, md: 5 }, borderColor: "rgba(255,255,255,.12)" }} />

        <Stack
          direction={{ xs: "column", sm: "row" }}
          spacing={1.5}
          justifyContent="space-between"
          alignItems={{ xs: "flex-start", sm: "center" }}
          sx={{ py: 3 }}
        >
          <Typography variant="caption" sx={{ color: "rgba(255,255,255,.55)" }}>
            © {new Date().getFullYear()} {BRAND.name} demo. Built with React, Material UI, Django REST
            Framework and JWT.
          </Typography>
          <Stack direction="row" spacing={2} alignItems="center">
            <Typography variant="caption" sx={{ color: "rgba(255,255,255,.55)" }}>
              Version {BRAND.version}
            </Typography>
            <Link
              href={BRAND.github}
              target="_blank"
              rel="noreferrer"
              underline="none"
              sx={{ display: "flex", alignItems: "center", gap: 0.75, color: muted, "&:hover": { color: "#fff" } }}
            >
              <GitHubIcon sx={{ fontSize: 16 }} />
              <Typography variant="caption">github.com/Adnan8066</Typography>
            </Link>
          </Stack>
        </Stack>
      </Container>
    </Box>
  );
}
