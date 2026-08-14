# ABFS-100 Risk Assessment

Document ID: RA-ABFS-100

## RISK-001 — Incorrect Tablet Count

Related Requirements:
- URS-005
- URS-006

Hazard:
A bottle may contain an incorrect number of tablets.

Potential Impact:
Incorrect product quantity may be released.

Risk Level:
High

Control:
The system verifies tablet count and automatically rejects bottles
that fail count verification.

---

## RISK-002 — Unauthorized System Access

Related Requirements:
- URS-001
- URS-002

Hazard:
An unauthorized individual may modify GxP-relevant system settings.

Potential Impact:
Unauthorized changes could affect system operation or data integrity.

Risk Level:
High

Control:
Authentication and role-based authorization are required.

---

## RISK-003 — Missing Audit Trail Record

Related Requirement:
- URS-008

Hazard:
A GxP-relevant user action may not be recorded.

Potential Impact:
Loss of traceability and data integrity.

Risk Level:
High

Control:
The system automatically records defined GxP-relevant events in
the audit trail.

---

## RISK-004 — Loss of Electronic Records

Related Requirements:
- URS-009
- URS-010
- URS-012

Hazard:
Electronic manufacturing records may become unavailable following
a system failure.

Potential Impact:
Loss of manufacturing evidence and traceability.

Risk Level:
High

Control:
Electronic records are stored persistently and protected through
backup and recovery functions.

---

## RISK-005 — Filling Without Bottle

Related Requirement:
- URS-004

Hazard:
The filling mechanism may activate when no bottle is present.

Potential Impact:
Material loss or equipment contamination.

Risk Level:
Medium

Control:
Bottle presence must be confirmed before the filling sequence starts.