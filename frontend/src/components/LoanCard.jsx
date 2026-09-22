import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  LinearProgress,
  Stack,
  Typography,
} from "@mui/material";
import HomeWorkIcon from "@mui/icons-material/HomeWork";
import SchoolIcon from "@mui/icons-material/School";
import DirectionsCarIcon from "@mui/icons-material/DirectionsCar";
import PaidIcon from "@mui/icons-material/Paid";
import { useNavigate } from "react-router-dom";

import { formatCurrency, formatDate } from "../utils/formatCurrency.js";
import { StatusChip } from "./Common.jsx";

const ICONS = {
  HOME: <HomeWorkIcon />,
  EDUCATION: <SchoolIcon />,
  VEHICLE: <DirectionsCarIcon />,
  PERSONAL: <PaidIcon />,
};

export default function LoanCard({ loan, detailPath = "/loans" }) {
  const navigate = useNavigate();

  return (
    <Card sx={{ height: "100%" }}>
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
          <Stack direction="row" spacing={1.5} alignItems="center">
            <Box
              sx={{
                display: "grid",
                placeItems: "center",
                width: 44,
                height: 44,
                borderRadius: 2,
                backgroundColor: "#eef2fd",
                color: "primary.main",
              }}
            >
              {ICONS[loan.loan_type] || <PaidIcon />}
            </Box>
            <Box>
              <Typography variant="subtitle1" fontWeight={700}>
                {loan.loan_type_display}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {loan.loan_id} • applied {formatDate(loan.applied_at)}
              </Typography>
            </Box>
          </Stack>
          <StatusChip status={loan.status} />
        </Stack>

        <Stack direction="row" spacing={3} sx={{ mt: 2.5 }}>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Loan amount
            </Typography>
            <Typography variant="h6">{formatCurrency(loan.amount, { compact: true })}</Typography>
          </Box>
          <Box>
            <Typography variant="caption" color="text.secondary">
              EMI
            </Typography>
            <Typography variant="h6">{formatCurrency(loan.emi)}</Typography>
          </Box>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Interest
            </Typography>
            <Typography variant="h6">{loan.interest_rate}%</Typography>
          </Box>
        </Stack>

        <Divider sx={{ my: 2 }} />

        <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
          <Typography variant="caption" color="text.secondary">
            Repaid {formatCurrency(loan.paid_amount)}
          </Typography>
          <Typography variant="caption" fontWeight={700}>
            {loan.progress_percent}%
          </Typography>
        </Stack>
        <LinearProgress
          variant="determinate"
          value={Math.min(loan.progress_percent, 100)}
          sx={{ height: 8, borderRadius: 4 }}
        />

        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mt: 2 }}>
          <Chip
            size="small"
            variant="outlined"
            label={`${loan.tenure_months} months`}
          />
          <Button size="small" onClick={() => navigate(`${detailPath}/${loan.id}`)}>
            View details
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}
