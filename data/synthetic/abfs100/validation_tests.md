# ABFS-100 Validation Test Specification

Document ID: VAL-ABFS-100

## TEST-001 — Invalid Login

Related Requirement:
URS-001

Objective:
Verify that an unauthorized user cannot access protected system
functions.

Test Steps:

1. Open the ABFS-100 login screen.
2. Enter an invalid username or password.
3. Attempt to log in.

Expected Result:

Access is denied and protected system functions remain unavailable.

---

## TEST-002 — Operator Access Control

Related Requirement:
URS-002

Objective:
Verify that an Operator cannot access Administrator functions.

Test Steps:

1. Log in using an Operator account.
2. Navigate to user administration.
3. Attempt to create a new user.

Expected Result:

The Operator is prevented from accessing user administration
functions.

---

## TEST-003 — Bottle Presence Interlock

Related Requirement:
URS-004

Objective:
Verify that filling cannot start when no bottle is detected.

Test Steps:

1. Start the production sequence.
2. Remove the bottle from the filling position.
3. Request a filling cycle.

Expected Result:

The filling operation does not start.

---

## TEST-004 — Incorrect Tablet Count

Related Requirements:
URS-005
URS-006

Objective:
Verify that a bottle with an incorrect tablet count is rejected.

Test Steps:

1. Configure an approved production recipe.
2. Simulate an incorrect tablet count.
3. Allow the bottle to reach the reject station.

Expected Result:

The system identifies the count discrepancy and rejects the bottle.

---

## TEST-005 — Audit Trail Recording

Related Requirement:
URS-008

Objective:
Verify that a GxP-relevant parameter change creates an audit trail
record.

Test Steps:

1. Log in as an authorized Supervisor.
2. Modify an allowed production parameter.
3. Save the change.
4. Open the audit trail.

Expected Result:

An audit trail entry contains the user identity, changed action,
date, and time.

---

## TEST-006 — Backup and Restore

Related Requirements:
URS-010
URS-012

Objective:
Verify that stored electronic records can be restored from backup.

Test Steps:

1. Create a system backup.
2. Simulate loss of the active data set.
3. Perform the approved restore procedure.
4. Review restored records.

Expected Result:

Previously backed-up electronic records are successfully restored
and remain readable.