# Lab 3 – Component Modelling & Architectural Pattern Selection

## Project

**Student Club Event Ticketing & Budget Portal (SCETBP)** — Problem Statement #10

## Objective

Evaluate the candidate architectural styles for SCETBP, select the most appropriate one,
justify the decision, and model the system as a UML Component Diagram showing components,
provided/required interfaces, ports and dependencies.

## Architecture Selected

**Microservices Architecture.**

The system carries two workloads of opposite shape — a slow, low-volume budget approval chain
(Faculty Coordinator → Finance Office → Dean) and a short, high-volume QR check-in burst at
event start. Microservices lets each scale, fail and release independently, which is what
NFR-001 (< 100 ms QR validation at peak) and NFR-002 (role-restricted operations) require.

Layered and Client-Server were both considered and rejected — see the justification document.

## Components (9)

| # | Component | Stereotype | Responsibility |
|---|-----------|------------|----------------|
| 1 | Portal Web Client | «component» | Role-based UI for Club Lead, Faculty Coordinator, Finance Office, Dean and Campus Admin |
| 2 | API Gateway & Authentication Service | «component» | Single entry point, RBAC, JWT issue and verification |
| 3 | Event Proposal Manager | «component» | Proposal lifecycle and status — the *Order Manager* component from the handout |
| 4 | Budget Approval Service | «component» | Three-stage approval workflow — the *Payment Service* component from the handout |
| 5 | Ticketing Service | «component» | QR ticket generation, reissue and revocation |
| 6 | Check-In Validation Service | «component» | Stateless QR verification at the gate; admit / reject |
| 7 | Notification Service | «component» | Email and push on every status change |
| 8 | Proposal & Budget Store | «datastore» | Proposals, budget lines, approval audit trail |
| 9 | Ticket Store | «datastore» | Tickets and check-in log (read-optimised replica) |

External device modelled: **Check-In Scanner Device** «device».

## Interfaces (7 assembly connectors + 3 usage dependencies)

| Interface | Provided by | Required by | Protocol |
|-----------|-------------|-------------|----------|
| `IPortalAPI` | API Gateway & Auth Service | Portal Web Client | HTTPS / REST + JWT |
| `IProposalMgmt` | Event Proposal Manager | API Gateway & Auth Service | REST / JSON |
| `IBudgetApproval` | Budget Approval Service | Event Proposal Manager | REST / JSON — *given interface* |
| `ITicketIssue` | Ticketing Service | Budget Approval Service | AMQP async event |
| `ITicketValidate` | Check-In Validation Service | Check-In Scanner Device | HTTPS / REST, < 100 ms |
| `ITicketLookup` | Ticket Store | Check-In Validation Service | Cache read / SQL |
| `INotify` | Notification Service | Budget Approval Service | SMTP / Push |

Usage dependencies («use»): Event Proposal Manager → Proposal & Budget Store (JDBC/SQL),
Budget Approval Service → Proposal & Budget Store (budget rows),
Ticketing Service → Ticket Store (SQL insert).

Ball notation marks provided interfaces, socket notation marks required interfaces, and small
squares on component boundaries mark ports.

## Deliverables

| File | Description |
|------|-------------|
| `Component_Diagram.pdf` | UML component diagram (vector, for submission) |
| `Component_Diagram.png` | Same diagram as a raster image |
| `Component_Diagram.svg` | Editable source of the diagram |
| `Architecture_Justification.docx` | One-page written justification (Word) |
| `Architecture_Justification.pdf` | Same justification as PDF |

## Student Details

**Name:** Aarush Muralidhara
**SRN:** PES1UG24CS010
**Class:** 5A
