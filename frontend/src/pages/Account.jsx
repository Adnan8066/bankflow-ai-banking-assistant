import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import CalculateIcon from "@mui/icons-material/Calculate";
import { useNavigate } from "react-router-dom";

import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { formatCurrency, formatDate } from "../utils/formatCurrency.js";

function DetailRow({ label, value, copyable }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(String(value));
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  };

  return (
    <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ py: 1.25 }}>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Stack direction="row" spacing={1} alignItems="center">
        <Typography variant="body2" fontWeight={700}>
          {value}
        </Typography>
        {copyable && (
          <Button size="small" onClick={handleCopy} startIcon={<ContentCopyIcon fontSize="small" />}>
            {copied ? "Copied" : "Copy"}
          </Button>
        )}
      </Stack>
    </Stack>
  );
}

export default function Account() {
  const navigate = useNavigate();
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setAccount(await bankingService.getAccount());
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading account details..." />;

  return (
    <Box>
      <PageHeader
        title="My Account"
        subtitle="A simulated savings account with masked identifiers for the demo."
      />
      <ErrorAlert message={error} onRetry={load} />

      {account && (
        <Grid container spacing={2.5}>
          <Grid item xs={12} md={5}>
            <Card
              sx={{
                color: "#fff",
                background: "linear-gradient(135deg, #12295e 0%, #1b3a8f 55%, #4361ee 100%)",
                borderRadius: 4,
              }}
            >
              <CardContent sx={{ p: 3 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography variant="caption" sx={{ color: "rgba(255,255,255,.75)" }}>
                      Available balance
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 800, mt: 0.5 }}>
                      {formatCurrency(account.balance)}
                    </Typography>
                  </Box>
                  <AccountBalanceIcon sx={{ fontSize: 34, opacity: 0.9 }} />
                </Stack>

                <Typography variant="body1" sx={{ letterSpacing: 3, mt: 4, fontSize: 18 }}>
                  {account.masked_account_number}
                </Typography>
                <Stack direction="row" justifyContent="space-between" sx={{ mt: 3 }}>
                  <Box>
                    <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                      Account holder
                    </Typography>
                    <Typography variant="body2" fontWeight={700}>
                      {account.customer_name}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" sx={{ color: "rgba(255,255,255,.7)" }}>
                      IFSC (demo)
                    </Typography>
                    <Typography variant="body2" fontWeight={700}>
                      {account.ifsc_code}
                    </Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>

            <Stack direction="row" spacing={1.5} sx={{ mt: 2 }}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<ReceiptLongIcon />}
                onClick={() => navigate("/transactions")}
              >
                Transactions
              </Button>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<CalculateIcon />}
                onClick={() => navigate("/emi-calculator")}
              >
                EMI calculator
              </Button>
            </Stack>
          </Grid>

          <Grid item xs={12} md={7}>
            <SectionCard title="Account information" subtitle="Simulated details - safe to share">
              <DetailRow label="Customer name" value={account.customer_name} />
              <Divider />
              <DetailRow label="Email" value={account.customer_email} />
              <Divider />
              <DetailRow label="Account number (masked)" value={account.masked_account_number} />
              <Divider />
              <DetailRow label="Account type" value={account.account_type_display} />
              <Divider />
              <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ py: 1.25 }}>
                <Typography variant="body2" color="text.secondary">
                  Account status
                </Typography>
                <StatusChip status={account.status} />
              </Stack>
              <Divider />
              <DetailRow label="Available balance" value={formatCurrency(account.balance)} />
              <Divider />
              <DetailRow label="IFSC-like demo identifier" value={account.ifsc_code} copyable />
              <Divider />
              <DetailRow label="Branch" value={account.branch} />
              <Divider />
              <DetailRow label="Date created" value={formatDate(account.created_at)} />
            </SectionCard>

            <Alert severity="info" sx={{ mt: 2.5, borderRadius: 3 }}>
              For privacy, the full account number is never displayed or exposed by the API. All
              identifiers and balances in BankFlow are fictional demo values.
            </Alert>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}
