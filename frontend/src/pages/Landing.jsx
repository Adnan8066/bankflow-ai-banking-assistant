import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Container,
  Divider,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import {
  FiArrowRight,
  FiBarChart2,
  FiBell,
  FiCheckCircle,
  FiLock,
  FiPieChart,
  FiSmartphone,
  FiTrendingUp,
  FiUserCheck,
  FiZap,
} from "react-icons/fi";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import { Link as RouterLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { BRAND } from "../branding.js";
import PublicHeader from "../components/PublicHeader.jsx";
import SiteFooter from "../components/SiteFooter.jsx";

const FEATURES = [
  {
    icon: <FiZap size={22} />,
    title: "Smart Dashboard",
    text: "Balances, income, expenses and loans in one clean, glanceable view.",
  },
  {
    icon: <SmartToyIcon sx={{ fontSize: 22 }} />,
    title: "AI Banking Assistant",
    text: "Ask natural questions about your money and get grounded answers instantly.",
  },
  {
    icon: <FiBarChart2 size={22} />,
    title: "Transaction Analytics",
    text: "Monthly trends, category splits and income vs expense charts.",
  },
  {
    icon: <FiTrendingUp size={22} />,
    title: "Loan Management",
    text: "Apply for demo loans, track EMI, outstanding amount and status.",
  },
  {
    icon: <FiLock size={22} />,
    title: "Secure Authentication",
    text: "JWT login, protected APIs and role based access for bank staff.",
  },
  {
    icon: <FiPieChart size={22} />,
    title: "Financial Insights",
    text: "Understand spending patterns with AI generated summaries.",
  },
];

const DEMO_CHAT = [
  { role: "user", text: "What is my current balance?" },
  { role: "ai", text: "Your current available balance is ₹85,450." },
  { role: "user", text: "How much did I spend this month?" },
  { role: "ai", text: "You spent ₹18,450 this month." },
  { role: "user", text: "What was my biggest expense?" },
  { role: "ai", text: "Your largest expense this month was Shopping at ₹7,200." },
];

export default function Landing() {
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin } = useAuth();

  const goToApp = () => navigate(isAuthenticated ? (isAdmin ? "/admin" : "/dashboard") : "/login");

  return (
    <Box id="home" sx={{ backgroundColor: "#ffffff" }}>
      <PublicHeader />

      {/* -------------------------------------------------------------- hero */}
      <Box
        sx={{
          position: "relative",
          overflow: "hidden",
          background:
            "radial-gradient(1100px 480px at 12% -5%, var(--bf-glow) 0%, var(--bf-shell) 58%), linear-gradient(180deg, var(--bf-panel) 0%, var(--bf-shell) 100%)",
          py: { xs: 6, md: 10 },
        }}
      >
        <Box
          aria-hidden
          sx={{
            position: "absolute",
            top: -140,
            right: -120,
            width: 420,
            height: 420,
            borderRadius: "50%",
            background: BRAND.gradient,
            opacity: 0.12,
            filter: "blur(10px)",
          }}
        />
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <Chip
                label="Demo application • simulated data only"
                color="primary"
                variant="outlined"
                sx={{ mb: 2 }}
              />
              <Typography variant="h2" sx={{ fontSize: { xs: 32, md: 46 }, lineHeight: 1.15 }}>
                Your Smarter Digital Banking Experience
              </Typography>
              <Typography variant="h6" color="text.secondary" sx={{ mt: 2, fontWeight: 400 }}>
                Manage your finances, understand your spending and get instant assistance with our
                AI-powered banking assistant.
              </Typography>
              <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mt: 4 }}>
                <Button
                  variant="contained"
                  size="large"
                  endIcon={<FiArrowRight />}
                  onClick={goToApp}
                >
                  Get Started
                </Button>
                <Button
                  size="large"
                  variant="outlined"
                  component="a"
                  href="#features"
                >
                  Explore Features
                </Button>
              </Stack>
              <Stack direction="row" spacing={3} sx={{ mt: 4, flexWrap: "wrap", gap: 1 }}>
                {["JWT secured", "Role based access", "Works offline"].map((item) => (
                  <Stack key={item} direction="row" spacing={0.75} alignItems="center">
                    <FiCheckCircle color="#16a34a" />
                    <Typography variant="body2" color="text.secondary">
                      {item}
                    </Typography>
                  </Stack>
                ))}
              </Stack>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ borderRadius: 4 }}>
                <CardContent sx={{ p: 3 }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Stack direction="row" spacing={1.5} alignItems="center">
                      <Box
                        sx={{
                          display: "grid",
                          placeItems: "center",
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          backgroundColor: "#eef2fd",
                          color: "primary.main",
                        }}
                      >
                        <SmartToyIcon fontSize="small" />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" fontWeight={700}>
                          BankFlow AI
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Always-on demo assistant
                        </Typography>
                      </Box>
                    </Stack>
                    <Chip size="small" color="success" label="online" />
                  </Stack>

                  <Divider sx={{ my: 2 }} />

                  {DEMO_CHAT.map((line) => (
                    <Box
                      key={line.text}
                      sx={{
                        display: "flex",
                        justifyContent: line.role === "user" ? "flex-end" : "flex-start",
                        mb: 1.25,
                      }}
                    >
                      <Box
                        sx={{
                          px: 1.75,
                          py: 1,
                          borderRadius: 3,
                          maxWidth: "85%",
                          fontSize: 14,
                          backgroundColor: line.role === "user" ? "primary.main" : "#f4f6fb",
                          color: line.role === "user" ? "#fff" : "text.primary",
                        }}
                      >
                        {line.text}
                      </Box>
                    </Box>
                  ))}

                  <Button fullWidth variant="contained" sx={{ mt: 2 }} onClick={goToApp}>
                    Try the assistant
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* ---------------------------------------------------------- features */}
      <Container maxWidth="lg" id="features" sx={{ py: { xs: 6, md: 9 } }}>
        <Stack alignItems="center" sx={{ textAlign: "center", mb: 5 }}>
          <Typography variant="h3" sx={{ fontSize: { xs: 26, md: 34 } }}>
            Everything a modern banking demo needs
          </Typography>
          <Typography color="text.secondary" sx={{ mt: 1.5, maxWidth: 620 }}>
            BankFlow demonstrates React, Django REST Framework, JWT, charts and an AI assistant
            working together on completely fictional data.
          </Typography>
        </Stack>

        <Grid container spacing={3}>
          {FEATURES.map((feature) => (
            <Grid item xs={12} sm={6} md={4} key={feature.title}>
              <Card sx={{ height: "100%", transition: "transform .18s ease", "&:hover": { transform: "translateY(-4px)" } }}>
                <CardContent>
                  <Box
                    sx={{
                      display: "grid",
                      placeItems: "center",
                      width: 46,
                      height: 46,
                      borderRadius: 2,
                      color: "primary.main",
                      backgroundColor: "#eef2fd",
                      mb: 2,
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" sx={{ mb: 0.5 }}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.text}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* --------------------------------------------------------- assistant */}
      <Box id="assistant" sx={{ backgroundColor: "#f7f9ff", py: { xs: 6, md: 9 } }}>
        <Container maxWidth="lg">
          <Grid container spacing={5} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h3" sx={{ fontSize: { xs: 26, md: 32 } }}>
                An assistant that actually understands your data
              </Typography>
              <Typography color="text.secondary" sx={{ mt: 2 }}>
                Questions are mapped to an intent, the relevant demo banking data is retrieved, and
                the answer is generated from that data — never invented. If no external AI key is
                configured, the built-in rule based engine answers anyway.
              </Typography>
              <Stack spacing={1.5} sx={{ mt: 3 }}>
                {[
                  "What is my balance?",
                  "How much did I spend on food?",
                  "What loans do I have?",
                  "Explain EMI / KYC / credit score",
                ].map((q) => (
                  <Stack key={q} direction="row" spacing={1.25} alignItems="center">
                    <FiCheckCircle color="#16357f" />
                    <Typography variant="body2">{q}</Typography>
                  </Stack>
                ))}
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card sx={{ backgroundColor: "#0b1531", color: "#fff", borderRadius: 4 }}>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    Example AI session
                  </Typography>
                  {[
                    ["You", "What was my biggest expense?"],
                    ["BankFlow AI", "Your largest expense this month was Shopping at ₹7,200."],
                    ["You", "What loans do I have?"],
                    ["BankFlow AI", "You currently have 2 active demo loans: Home Loan and Vehicle Loan."],
                  ].map(([who, text]) => (
                    <Box key={text} sx={{ mb: 1.5 }}>
                      <Typography variant="caption" sx={{ color: "rgba(255,255,255,.6)" }}>
                        {who}
                      </Typography>
                      <Typography variant="body2">{text}</Typography>
                    </Box>
                  ))}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* ---------------------------------------------------------- security */}
      <Container maxWidth="lg" id="security" sx={{ py: { xs: 6, md: 9 } }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Typography variant="h4" sx={{ fontSize: { xs: 24, md: 30 } }}>
              Built with security basics from day one
            </Typography>
            <Typography color="text.secondary" sx={{ mt: 1.5 }}>
              This is a demonstration project, but it still shows the patterns a real banking
              application would follow.
            </Typography>
          </Grid>
          <Grid item xs={12} md={8}>
            <Grid container spacing={2}>
              {[
                { icon: <FiLock />, title: "JWT authentication", text: "Access + refresh tokens with automatic refresh on 401." },
                { icon: <FiUserCheck />, title: "Role based access", text: "Customer routes and bank employee routes are separated." },
                { icon: <FiSmartphone />, title: "Responsive by default", text: "Desktop, laptop, tablet and mobile layouts." },
                { icon: <FiBell />, title: "Simulated notifications", text: "Salary, security and loan updates with read state." },
              ].map((item) => (
                <Grid item xs={12} sm={6} key={item.title}>
                  <Box sx={{ p: 2.5, borderRadius: 3, border: "1px solid #e6e9f2", height: "100%" }}>
                    <Stack direction="row" spacing={1.5} alignItems="center" sx={{ mb: 1 }}>
                      <Box sx={{ color: "primary.main" }}>{item.icon}</Box>
                      <Typography variant="subtitle2">{item.title}</Typography>
                    </Stack>
                    <Typography variant="body2" color="text.secondary">
                      {item.text}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </Container>

      {/* ------------------------------------------------------------- about */}
      <Box id="about" sx={{ backgroundColor: "#f7f9ff", py: { xs: 6, md: 8 } }}>
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Typography variant="h4" sx={{ fontSize: { xs: 24, md: 30 } }}>
                BankFlow - AI Banking Assistant
              </Typography>
              <Typography color="text.secondary" sx={{ mt: 1.5 }}>
                A full-stack reference project: React + Vite + Material UI on the frontend,
                Django REST Framework with JWT on the backend, Recharts for analytics and a modular
                AI service that can run rule based or be pointed at an LLM.
              </Typography>
              <Typography color="text.secondary" sx={{ mt: 1.5 }}>
                <strong>Important:</strong> every account, transaction and loan in this application
                is fictional. No real money movement, payments or banking operations are performed.
              </Typography>
            </Grid>
            <Grid item xs={12} md={5}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 1.5 }}>
                    Demo logins
                  </Typography>
                  {[
                    ["Customer", "mohammed@bankflow.com", "Demo@12345"],
                    ["Bank employee", "admin@bankflow.com", "Admin@12345"],
                  ].map(([role, email, password]) => (
                    <Box key={email} sx={{ mb: 1.5 }}>
                      <Typography variant="caption" color="text.secondary">
                        {role}
                      </Typography>
                      <Stack direction="row" spacing={1} alignItems="center" sx={{ flexWrap: "wrap" }}>
                        <Chip size="small" label={email} variant="outlined" />
                        <Chip size="small" label={password} variant="outlined" />
                      </Stack>
                    </Box>
                  ))}
                  <Button fullWidth variant="contained" sx={{ mt: 1 }} onClick={() => navigate("/login")}>
                    Login to the demo
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      <SiteFooter />
    </Box>
  );
}
