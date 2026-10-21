# Google Sheets Compatibility Test Report

**Related issue:** #11
**Workbook:** `cf-kit/dist/cf-kit.xlsx`
**Test environment:** Google Sheets (including a native Google Sheets copy)
**Test data:** Fictional records only

## Summary

The cf-kit workbook was tested in Google Sheets to verify its dropdowns, date validation, calculated columns, conditional formatting, and Dashboard functionality.

Most tested features worked correctly. One issue was identified: missing formulas in the Residences tab caused address gaps to be incorrectly reported on the Dashboard.

## Tab-by-Tab Results

| Tab | Result | Findings |
|---|---|---|
| Start Here | PASS | Instructions and formatting displayed correctly. |
| Dashboard | PARTIAL | Counts, warning colors, and review dates worked, except the residence-gap count. |
| Residences | FAIL | Gap calculation formulas were missing in the tested Google Sheets copy. |
| Employment | PASS | Dropdowns, date gaps, and red explanation warnings worked. |
| Education | PASS | School records, dropdowns, and Dashboard count worked. |
| Legal Matters | PASS | Dropdowns and Dashboard count worked. |
| Financial | PASS | Resolved and unresolved item counts updated correctly. |
| Licenses | PASS | Dropdowns, date entry, and date validation worked during testing. |
| References | PASS | Yes/No dropdown updated the Dashboard count. |
| Law School App Check | PASS | Amend triggered a red warning and updated the Dashboard count. |
| Documents | PASS | Requested, Received, and Overdue statuses worked, including amber highlighting. |
| Change Log | PASS | Dashboard review dates calculated correctly. |

## Confirmed Finding: Missing Residence-Gap Formulas

### Steps to Reproduce

1. Upload `cf-kit/dist/cf-kit.xlsx` to Google Drive.
2. Open it in Google Sheets and save a native Google Sheets copy.
3. Open the Residences tab.
4. Enter two fictional records:
   - Row 2: From `2023-01-01`, To `2023-06-30`.
   - Row 3: From `2023-08-15`, To `2024-02-28`.
5. Inspect cell `L3` and the Dashboard.

### Expected Behavior

- Cell `L3` displays `45` days.
- The cell is highlighted red because the gap exceeds 30 days.
- Dashboard reports one residence gap over 30 days.

### Actual Behavior

- Cell `L3` is blank and its formula bar is empty.
- No red warning appears.
- Dashboard reports zero residence gaps.

The original Excel workbook contains this formula in `L3`:

`=IF(AND(A3<>"",B2<>""),A3-B2-1,"")`

The finding suggests the formula was not retained in the tested Google Sheets copy. The exact cause has not been established.

## Other Verified Results

**Employment:** A 45-day gap was calculated and highlighted red. Both Terminated and Asked to resign triggered red explanation warnings.

**Documents:** Overdue requests displayed amber warnings. Received and Requested statuses updated correctly.

**Dashboard:** Employment gaps, explanation warnings, document counts, financial items, references, schools, legal matters, and amendment counts updated correctly.

**Change Log:** Entering `2026-10-21` set the next review date to `2027-02-18`, as specified.

## Evidence

Screenshots showing the blank Residences formula cell and incorrect Dashboard gap count are provided in the discussion of Issue #11.

## Conclusion

The workbook is largely compatible with Google Sheets. The primary issue discovered was the missing Residences gap formulas in the tested copy.

No changes to the spreadsheet generator or workbook were made during this testing contribution.
