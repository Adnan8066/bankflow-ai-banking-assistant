import {
  Box,
  Chip,
  IconButton,
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Typography,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { useNavigate } from "react-router-dom";

import { formatCurrency, formatDate } from "../utils/formatCurrency.js";
import { EmptyState, StatusChip } from "./Common.jsx";

/**
 * Reusable transaction table. `showCustomer` and `basePath` let the admin pages
 * reuse exactly the same component as the customer page.
 */
export default function TransactionTable({
  transactions = [],
  loading = false,
  showCustomer = false,
  basePath = "/transactions",
  emptyTitle = "No transactions found",
  emptyDescription = "Try clearing the filters or searching for something else.",
}) {
  const navigate = useNavigate();

  if (loading) {
    return (
      <Box>
        {[0, 1, 2, 3, 4].map((row) => (
          <Skeleton key={row} height={48} sx={{ borderRadius: 1 }} />
        ))}
      </Box>
    );
  }

  if (!transactions.length) {
    return <EmptyState title={emptyTitle} description={emptyDescription} />;
  }

  return (
    <TableContainer>
      <Table size="small" sx={{ minWidth: 720 }}>
        <TableHead>
          <TableRow>
            <TableCell>Transaction ID</TableCell>
            <TableCell>Date</TableCell>
            {showCustomer && <TableCell>Customer</TableCell>}
            <TableCell>Description</TableCell>
            <TableCell>Category</TableCell>
            <TableCell>Type</TableCell>
            <TableCell align="right">Amount</TableCell>
            <TableCell>Status</TableCell>
            <TableCell align="right">Details</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {transactions.map((txn) => (
            <TableRow
              key={txn.id}
              hover
              sx={{ cursor: basePath === "/admin/transactions" ? "default" : "pointer" }}
              onClick={() => basePath !== "/admin/transactions" && navigate(`${basePath}/${txn.id}`)}
            >
              <TableCell>
                <Typography variant="caption" fontWeight={700}>
                  {txn.transaction_id}
                </Typography>
              </TableCell>
              <TableCell>{formatDate(txn.date)}</TableCell>
              {showCustomer && <TableCell>{txn.customer_name || txn.account_number}</TableCell>}
              <TableCell sx={{ maxWidth: 260 }}>{txn.description}</TableCell>
              <TableCell>
                <Chip size="small" variant="outlined" label={txn.category} />
              </TableCell>
              <TableCell>
                <Chip
                  size="small"
                  label={txn.transaction_type === "CREDIT" ? "Credit" : "Debit"}
                  color={txn.transaction_type === "CREDIT" ? "success" : "default"}
                  variant={txn.transaction_type === "CREDIT" ? "filled" : "outlined"}
                />
              </TableCell>
              <TableCell align="right">
                <Typography
                  fontWeight={700}
                  color={txn.transaction_type === "CREDIT" ? "success.main" : "text.primary"}
                >
                  {txn.transaction_type === "CREDIT" ? "+" : "-"}
                  {formatCurrency(txn.amount)}
                </Typography>
              </TableCell>
              <TableCell>
                <StatusChip status={txn.status} />
              </TableCell>
              <TableCell align="right">
                {basePath !== "/admin/transactions" && (
                  <Tooltip title="Open transaction details">
                    <IconButton size="small" onClick={(e) => {
                      e.stopPropagation();
                      navigate(`${basePath}/${txn.id}`);
                    }}>
                      <VisibilityIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
