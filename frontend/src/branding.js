/** Brand tokens used by the header, the footer, the logo and the hero sections. */
export const BRAND = {
  name: "BankFlow",
  tagline: "AI Banking Assistant",
  version: "1.0",
  github: "https://github.com/Adnan8066/bankflow-ai-banking-assistant",
  brief:
    "https://github.com/Adnan8066/bankflow-ai-banking-assistant/blob/main/PROJECT_BRIEF.md",
  fullCode:
    "https://github.com/Adnan8066/bankflow-ai-banking-assistant/blob/main/FULL_CODE.md",
  readme: "https://github.com/Adnan8066/bankflow-ai-banking-assistant#readme",
  gradient: "linear-gradient(135deg, #0f2a6b 0%, #274bb0 55%, #3f74ff 100%)",
  gradientDeep: "linear-gradient(135deg, #0b1f52 0%, #16357f 55%, #2f57c9 100%)",
  footerGradient: "linear-gradient(180deg, #0b1531 0%, #080f24 100%)",
  accent: "#12b1a0",
};

export const FOOTER_LINKS = {
  product: [
    { label: "Features", href: "/#features" },
    { label: "AI Assistant", href: "/#assistant" },
    { label: "Security", href: "/#security" },
    { label: "About", href: "/#about" },
  ],
  project: [
    { label: "Project brief", href: BRAND.brief },
    { label: "Full source code", href: BRAND.fullCode },
    { label: "README", href: BRAND.readme },
    { label: "GitHub repository", href: BRAND.github },
  ],
};

export const DEMO_ACCOUNTS = [
  { role: "Customer", email: "mohammed@bankflow.com", password: "Demo@12345" },
  { role: "Bank employee", email: "admin@bankflow.com", password: "Admin@12345" },
];
