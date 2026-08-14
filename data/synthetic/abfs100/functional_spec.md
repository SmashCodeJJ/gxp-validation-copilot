# Functional Specification

System: ABFS-100 Automated Bottle Filling System

Document ID: FS-ABFS-100

## FS-001 — Authentication

Related Requirement: URS-001

The HMI shall display a login screen requiring a valid username
and password before access to protected system functions is granted.

## FS-002 — Role Authorization

Related Requirement: URS-002

The system shall assign permissions according to the user's
configured role: Operator, Supervisor, or Administrator.

## FS-003 — Recipe Management

Related Requirement: URS-003

The HMI shall display only recipes that are in Approved status
for production selection.

## FS-004 — Bottle Presence Detection

Related Requirement: URS-004

A bottle presence sensor shall confirm that a bottle is positioned
at the filling station before the filling sequence begins.

If no bottle is detected, the filling sequence shall not start.

## FS-005 — Tablet Count Verification

Related Requirement: URS-005

The tablet counting system shall compare the actual tablet count
against the configured recipe target.

## FS-006 — Automatic Rejection

Related Requirement: URS-006

When the verified tablet count does not equal the recipe target,
the PLC shall mark the bottle for automatic rejection.

## FS-007 — Critical Alarm Handling

Related Requirement: URS-007

Critical equipment faults shall:

1. generate an alarm
2. display the alarm on the HMI
3. stop the affected production operation when required

## FS-008 — Audit Trail

Related Requirement: URS-008

The system shall record GxP-relevant events including:

- user login
- user logout
- recipe changes
- parameter changes
- administrative changes
- alarm acknowledgements

Audit trail records shall contain the user identity, event,
date, and time.

## FS-009 — Batch Data Recording

Related Requirement: URS-009

The system shall store:

- batch identifier
- recipe identifier
- production start time
- production end time
- quantity processed
- quantity rejected
- relevant alarms

## FS-010 — Backup and Restore

Related Requirement: URS-010

The system shall provide a mechanism for backing up stored
GxP-relevant electronic records and restoring the records
following a system recovery event.

## FS-011 — System Timestamp

Related Requirement: URS-011

The system shall automatically associate system date and time
with electronic GxP records.

## FS-012 — Recovery

Related Requirement: URS-012

Following an unexpected interruption, the application shall restart
in a controlled state and preserve previously committed electronic
records.