import { useCallback, useEffect, useState } from "react";
import {
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
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useNavigate, useParams } from "react-router-dom";

import { ErrorAlert, Loader, PageHeader, SectionCard, StatusChip } from "../components/Common.jsx";
import bankingService from "../services/bankingService";
import { getErrorMessage } from "../services/api";
import { formatCurrency, formatDate } from "../utils/formatCurrency.js";

export default function TransactionDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [transaction, setTransaction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setTransaction(await bankingService.getTransaction(id));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading transaction..." />;

  if (error) {
    return (
      <>
        <PageHeader title="Transaction details" />
        <ErrorAlert message={error} onRetry={load} />
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/transactions")}>
          Back to transactions
        </Button>
      </>
    );
  }

  const isCredit = transaction.transaction_type === "CREDIT";

  return (
    <Box>
      <PageHeader
        title="Transaction details"
        subtitle={transaction.transaction_id}
        action={
          <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/transactions")}>
            Back
          </Button>
        }
      />

      <Grid container spacing={2.5}>
        <Grid item xs={12} md={5}>
          <Card
            sx={{
              borderRadius: 4,
              background: isCredit
                ? "linear-gradient(135deg, #0f5132 0%, #16a34a 100%)"
                : "linear-gradient(135deg, #12295e 0%, #1b3a8f 100%)",
              color: "#fff",
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Typography variant="caption" sx={{ color: "rgba(255,255,255,.8)" }}>
                {isCredit ? "Amount credited" : "Amount debited"}
              </Typography>
              <Typography variant="h3" sx={{ fontWeight: 800, mt: 1 }}>
                {isCredit ? "+" : "-"}
                {formatCurrency(transaction.amount)}
              </Typography>
              <Typography variant="body2" sx={{ mt: 1, color: "rgba(255,255,255,.85)" }}>
                {transaction.description}
              </Typography>
              <Stack direction="row" spacing={1} sx={{ mt: 3 }}>
                <Chip size="small" label={transaction.category} sx={{ bgcolor: "rgba(255,255,255,.22)", color: "#fff" }} />
                <Chip size="small" label={transaction.type_display} sx={{ bgcolor: "rgba(255,255,255,.22)", color: "#fff" }} />
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={7}>
          <SectionCard title="Transaction information">
            {[
              ["Transaction ID", transaction.transaction_id],
              ["Date & time", formatDate(transaction.date, { withTime: true })],
              ["Category", transaction.category_display || transaction.category],
              ["Type", transaction.type_display],
              ["Amount", formatCurrency(transaction.amount)],
              ["Balance after transaction", formatCurrency(transaction.balance_after)],
              ["Account number", transaction.account_number],
            ].map(([label, value]) => (
              <Box key={label}>
                <Stack direction="row" justifyContent="space-between" sx={{ py: 1.25 }}>
                  <Typography variant="body2" color="text.secondary">
                    {label}
                  </Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {value}
                  </Typography>
                </Stack>
                <Divider />
              </Box>
            ))}
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ pt: 1.5 }}>
              <Typography variant="body2" color="text.secondary">
                Status
              </Typography>
              <StatusChip status={transaction.status} />
            </Stack>
          </SectionCard>
        </Grid>
      </Grid>
    </Box>
  );
}
